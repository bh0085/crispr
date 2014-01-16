#!/usr/bin/env python


"""toplevel interface for this utility
1/16/2014 -- modified to use shared mem arrays.

1. get a pointer to the shm array storing the genome sequence
2. run the query using shmarray as input

EG:
        shm_library_bytes = get_library_bytes_shm(args.genome)
        run_sequence_vs_genome_shm("GGCTGCTGTCAGGGAGCTCA",args.genome, shm_library_bytes)

"""

import psycopg2
from scipy import sparse
import argparse
import os, numpy as np, pickle, re
import datetime, StringIO
utcnow = datetime.datetime.utcnow
import twobitreader
from pyramid.paster import bootstrap
from cfront import genomes_settings

import sharedmem as shm
import numpy as np
import multiprocessing as mp

RD_DATAROOT = "/tmp/ramdisk/crispr"
if not os.path.isdir(RD_DATAROOT):
    os.makedirs(RD_DATAROOT)


bytes_translation_dict = dict([(e,i) for i,e in enumerate([l0+l1+l2+l3 for l0 in "ATGC" for l1 in "ATGC" for l2 in "ATGC" for l3 in "ATGC"])])

open_libraries = {}
open_references = {}


def raw_locs_file(genome):
    if not os.path.isdir(os.path.join(RD_DATAROOT,genome)):
        os.makedirs(os.path.join(RD_DATAROOT,genome))
    return os.path.join(RD_DATAROOT,"{0}/alllocs.txt".format(genome))

def create_locs_file(genome):
    rlf = raw_locs_file(genome)
    twobitfile = "/tmp/ramdisk/genomes/{0}.2bit".format(genome)
    tb = twobitreader.TwoBitFile(twobitfile)
    chr_names = [k for k in tb.keys() if not "_" in k]
    rc_dict ={"A":"T","T":"A","G":"C","C":"G"}
    mask_regex = re.compile("[^ATGC]")
    reverse_complement_fun = lambda x:"".join([rc_dict[e] for e in x][::-1])

    with open(rlf,"w") as f:
        buf = ""
        for k in chr_names:
            c = str(tb[k])
            l = len(c)
            try:
                for i in range(l-2):
                    rng = c[i:i+2]
                    if (rng == "GG" or rng == "AG")  and (i >= 21 and i < l-3):
                        subs = c[i-21:i+2]
                        if mask_regex.search(subs) is None:
                            buf += "\t".join([k[3:],str(i - 21),  "+",subs]) + "\n"
                    if (rng == "CC" or rng == "CT") and (i < l-23):
                        subs = c[i:i+23]
                        if mask_regex.search(subs) is None:
                            buf += "\t".join([k[3:],str(i), "-", reverse_complement_fun(subs)])  + "\n"
                    if i % 1e6 == 0:
                        print "{0} millions of locs written".format(i/1e6)
                        f.write(buf)
                        buf = ""
            except IndexError, e:
                print "error on index {0} out of {1}".format(i, l)
        f.write(buf)

def library_file(genome):
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_bytes.npy".format(genome))
    return LIBRARY_BYTES_PATH

def reference_file(genome):
    REFERENCE_PATH =  os.path.join(RD_DATAROOT,"{0}_reference.pickle".format(genome))
    return REFERENCE_PATH

def init_library_bytes(genome):
    LIBRARY_BYTES_PATH = library_file(genome)
    #enter only some lines... change later    
    
    lc = 0
    for l in open(raw_locs_file(genome)):
        lc += 1
    bytes_array = np.zeros(lc * 5, dtype = np.dtype("uint8"))
    
    for i,l in enumerate(open(raw_locs_file(genome))):
        for j in range(5):
            #translate five characters from the library
            row = l.split("\t")
            seq =  row[3].strip()[:-3]
            bytes_array[5*i + j] = bytes_translation_dict.get(seq[(j)*4:(j)*4+4],0)
        
        if i %1e6 == 0:
            print "{0} millions of lines of library bytes done.".format(i/1e6)

    with open(LIBRARY_BYTES_PATH,'w') as f:
        np.save(f, bytes_array)
    print "saved lines to a bytes array at {0}".format(LIBRARY_BYTES_PATH)
    
def init_reference_dictionary(genome):
    REFERENCE_PATH = reference_file(genome)

    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")),
                            cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    
    init_table = """
    DROP TABLE IF EXISTS loc_references_{0};
    CREATE TABLE loc_references_{0} (
    id int PRIMARY KEY,
    strand SMALLINT not null,
    chr  VARCHAR(25) not null,
    sequence VARCHAR(20) not null,
    nrg VARCHAR(3) not null,
    start INT not null
    );""".format(genome)

    cur.execute(init_table);
    buf = StringIO.StringIO()
    cols = ["id","chr", "start", "strand", "sequence", "nrg"] 

    with open(raw_locs_file(genome)) as f:
        for i,l in enumerate(f):
            d = dict(zip(["chr","start","strand","sequence"],
                                  [e.strip() for e in l.split("\t")]))
            d["nrg"] = d["sequence"][-3:]
            d["sequence"] = d["sequence"][:-3]
            d["chr"] = d["chr"] if d["chr"][0:3] == "chr" else "chr" + d["chr"]
            d["strand"] = 1 if d["strand"] == "+" else -1
        
            buffered_row = "\t".join([str(i)] + [str(d[key]) for key in cols[1:]]) + "\n"
            buf.write(buffered_row)
            
            if i %1e6 == 0:
                buf.seek(0)
                cur.copy_from(buf,"loc_references_{0}".format(genome), columns = cols)
                buf.close()
                buf = StringIO.StringIO()
                print "{0} millions of lines of reference written".format(i/1e6)

    buf.seek(0)
    cur.copy_from(buf,"loc_references_{0}".format(genome), columns = cols)
    buf.close()
    conn.commit()
            



class TooManyHits(Exception):
    pass

    
def run_sequence_vs_genome_shm(sequence, genome, shm_genome_bytes):
    if not len(sequence) == 20:
        raise Exception("wrong length input sequence")
    
    lfpath  = library_file(genome)
    rfpath  = reference_file(genome)
    
    #inits library if required
    if not lfpath:
        raise Exception("genome has no library set: {0} ({1})".format(genome, lfpath))
                        
    #loads and queries the correct genomewide library
    matches = query_library_bytes_shm(genome, sequence, shm_genome_bytes)
    
    if len(matches) > 5000:
        raise TooManyHits()

    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")),
                            cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()


    print "found {0} matches, scanning for loci in postgres".format(len(matches))
    #retrieve matches from the reference.
    cur.execute("SELECT * FROM loc_references_{0} WHERE id = ANY(%s);".format(genome), ([long(m) for m in matches],))
    results = cur.fetchall()
    print "done scanning for matches in postgres!"
    
    conn.close()
    return results

def sample_sequence():
    tests = []
    for e in re.compile(">", re.M).split(ltests.strip()):
        if not e: continue
        match = re.compile( "(?P<id>.*)\n(?P<guide>\S{20})\s*(?P<nrg>\S{3})",re.M).search(e)
        tests.append(match.groupdict())
    return tests[0]["guide"]


## NEW CODE RETURNING SHARED MEM ARRAYS PER GENOME
def needs_init_library_bytes_shm(genome):
    return not genome in open_libraries

def init_library_bytes_shm(genome):
    global open_libraries
    lfpath  = library_file(genome)
    with open(lfpath) as f:
        open_libraries[genome] = shm.fromfile(f,dtype = np.dtype("uint8"))
    
def get_library_bytes_shm(genome):
    if needs_init_library_bytes_shm(genome):
        init_library_bytes_shm(genome)
    return open_libraries[genome]

## NOW TAKES THE SHM ARRAY AS INPUT
def query_library_bytes_shm(genome, sequence, shm_genome_bytes):
    library_bytes = shm_genome_bytes
    query_bytes = np.array([ bytes_translation_dict.get(sequence[(j)*4:(j)*4+4],0) 
                           for j in range(5)],
                           dtype=np.dtype("uint8"))
    mismatches_threshold = 5

    f = library_bytes
    g = query_bytes
    h = np.zeros((len(library_bytes)/len(query_bytes),), dtype = np.dtype("uint32"))

    import bc
    n_matches = bc.striding_8bit_comparison(f,g,h,mismatches_threshold)

    matches_list = h[:n_matches]
    print "N MATCHES: ", len(matches_list)
    #return matches_list[:100]
    return matches_list

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--program', '-p', dest="program",
                        default='save', type=str,
                        help="program to run -- default, save, allowed: [create, init, test, query]")
    parser.add_argument('--genome', '-g', dest = "genome",
                        default="mm9", type = str,
                        help = "target genomic library")

    parser.add_argument('inifile')
    
    args = parser.parse_args()
    env = bootstrap(args.inifile)

    if args.program == "all":
        create_locs_file(args.genome)
        init_library_bytes(args.genome)
        init_reference_dictionary(args.genome)
    if args.program == "ref":
        init_reference_dictionary(args.genome)
    if args.program == "create":
        create_locs_file(args.genome)
    if args.program == "test":
        shm_library_bytes = get_library_bytes_shm(args.genome)
        run_sequence_vs_genome_shm("GGCTGCTGTCAGGGAGCTCA",args.genome, shm_library_bytes)
    if args.program == "init":
        init_library_bytes(args.genome)
        init_reference_dictionary(args.genome)
    elif args.program == "query":
        query_library_bytes(args.genome, sample_sequence())

if __name__ == "__main__":
    main()





