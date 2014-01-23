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


def create_packed_locs_file(genome):
    LIBRARY_BYTES_PATH = library_file(genome)
    #enter only some lines... change later    


    bytepack_file_template = "/tmp/ramdisk/crispr/{0}_loci_bytes.dat"
    fpath = bytepack_file_template.format(genome)
    twobitfile = "/tmp/ramdisk/genomes/{0}.2bit".format(genome)
    tb = twobitreader.TwoBitFile(twobitfile)
    chr_names = [k for k in tb.keys() if not "_" in k]
    rc_dict ={"A":"T","T":"A","G":"C","C":"G"}
    mask_regex = re.compile("[^ATGC]")
    reverse_complement_fun = lambda x:"".join([rc_dict[e] for e in x][::-1])

    print "opening file"
    count = 0
    loops = 0
    with open(fpath,"w") as f:
        #buf = ""
        for k in sorted(chr_names):
            print "loading the chromosome {0}".format(k)
            c = str(tb[k])
            l = len(c)
            try:
                for i in range(l-2):
                    rng = c[i:i+2]
                    if (rng == "GG" or rng == "AG")  and (i >= 21 and i < l-3):
                        subs = c[i-21:i+2]
                        if mask_regex.search(subs) is None:
                            f.write( 
                                pack_flatfile_bytes(**{"chr":k[3:],
                                                        "strand":1,
                                                        "start":i-21,
                                                        "nrg":c[i-1:i+2]}))
                            count+=1
                            #"\t".join([k[3:],str(i - 21),  "+",subs]) + "\n"

                    if (rng == "CC" or rng == "CT") and (i < l-23):
                        subs = c[i:i+23]
                        if mask_regex.search(subs) is None:
                            f.write(
                                pack_flatfile_bytes(**{"chr":k[3:],
                                                       "strand":-1,
                                                       "start":i,
                                                       "nrg":reverse_complement_fun(c[i:i+3])}))
                            count+=1

                    loops += 1
                    if loops % 1000000 == 0:  print "{0} millions of locs written".format(count/1e6)
                    #if count > 100: break
                    #count +=1 
                    #if count % 1e6 == 0:
                    #   print "{0} millions of locs written".format(count/1e6)
                    #   f.write(buf)
                    #   buf = ""
            except IndexError, e:
                print "error on index {0} out of {1}".format(i, l)

    
    bytes_array = np.zeros(count * 5, dtype = np.dtype("uint8"))
    count_2 = 0
    for k in sorted(chr_names):
         print "loading the chromosome {0} for the second time".format(k)
         c = str(tb[k])
         l = len(c)
         for i in range(l-2):
                 rng = c[i:i+2]
                 if (rng == "GG" or rng == "AG")  and (i >= 21 and i < l-3):
                     subs = c[i-21:i+2]
                     if mask_regex.search(subs) is None:                         
                         for j in range(5):
                             bytes_array[5*count_2 + j] = bytes_translation_dict.get(subs[j*4:j*4+4],0)
                         count_2+=1

                 if (rng == "CC" or rng == "CT") and (i < l-23):
                     subs = c[i:i+23]
                     if mask_regex.search(subs) is None:                         
                         for j in range(5):
                             bytes_array[5*count_2 + j] = bytes_translation_dict.get(reverse_complement_fun(subs)[j*4:j*4+4],0)
                         count_2+=1

                 loops += 1
                 if loops % 1000000 == 0: print "byte array {0}% written".format(float(count_2)/count)

    print count, count_2
    
    LIBRARY_BYTES_PATH = library_file(genome)
    with open(LIBRARY_BYTES_PATH + ".tmp",'w') as f:
        bytes_array.tofile(f)
    print "saved lines to a bytes array at {0}".format(LIBRARY_BYTES_PATH)


def library_file(genome):
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_bytes.npy.tmp".format(genome))
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
        bytes_array.tofile(f)
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
            if len(d["chr"])> 23 : continue
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




#max value in the chr translation dict is 46656 in binary ... fits in 2 bytes
chr_translation_dict = dict([ (e,"{0:016b}".format(i)) 
                              for i,e in enumerate([ l1 + l2 + l3
                                                     for l1 in " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                                                     for l2 in " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                                                     for l3 in " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"])

                        ])
nt_bits_dict = {
    
    "A":"00",
    "T":"01",
    "G":"10",
    "C":"11"
}
nt_rev_bits_dict = dict([(v,k) for k,v in nt_bits_dict.iteritems()])
nrg_rev_bits_dict = dict([(k1 + k2 + k3 ,v1 + v2 + v3) 
                          for k1,v1 in nt_rev_bits_dict.iteritems()
                          for k2,v2 in nt_rev_bits_dict.iteritems()
                          for k3,v3 in nt_rev_bits_dict.iteritems()])
chr_rev_translation_dict = dict([(v,k) for k,v in chr_translation_dict.iteritems()])

def pack_flatfile_bytes(nrg = None,chr = None,start = None,strand = None):
    '''
    nrg: 6 bits    
    strand = +1 : 1, -1: 0z
    strart = 32 bit rep
    
    '''
    cchars = chr[3:6].upper() if chr[0:3] == "chr" else chr[0:3].upper()
    chr_bits = chr_translation_dict[(cchars + "   ")[:3]]
    nrg_bits = nt_bits_dict[nrg[0]] + nt_bits_dict[nrg[1]] + nt_bits_dict[nrg[2]]
    start_bits = "{0:032b}".format(start)
    line = start_bits + {1:"01",-1:"00"}.get(strand) + nrg_bits + chr_bits
    
    assert len(line) == 16 + 32 + 8
    bytes = np.array([np.packbits(np.uint8([e=="1" for e in line[i*8:i*8+8]]))[0] for i in range(7)], dtype = np.byte).tostring()
    return bytes
    


def unpack_flatfile_bytes(bytes_line):
    bits_string = ''.join(["{0:08b}".format(np.fromstring(bytes_line,dtype="uint8")[i]) for i in range(7)])
    import struct
    start, = struct.unpack('<I',bytes_line[:4][::-1])
    strand = 1 if bits_string[32:34] == "01" else -1
    nrg_bits = bits_string[34:40]
    nrg_letters = nrg_rev_bits_dict[nrg_bits]
    chr_letters = "chr" + chr_rev_translation_dict[bits_string[40:56]].strip()
    
    return {"start":start,
            "strand":strand,
            "nrg":nrg_letters,
            "chr":chr_letters}
    
def extract_bytes_by_line(line_no, bytes_file_pointer):
    bytes_file_pointer.seek(line_no * 7)
    line = bytes_file_pointer.read(7)
    return line

bytepack_file_template = "/tmp/ramdisk/crispr/{0}_loci_bytes.dat"
def pack_whole_genome_to_flatfile(genome):
        
    fpath = bytepack_file_template.format(genome)
    with open(fpath, 'w') as f:
        if genome == "fake":
            hits = [{"chr":"1",
                     "start":100,
                     "strand":-1,
                     "nrg":"ATG"},
                    {"chr":"chrX",
                     "start":20000000l,
                     "strand":1,
                     "nrg":"ATG"}]
            for h in hits:
                f.write(pack_flatfile_bytes(**h))
        else:
            
            conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                                    .format(genomes_settings.get("postgres_database"),
                                            genomes_settings.get("postgres_user"),
                                            genomes_settings.get("postgres_password")),
                                    cursor_factory=psycopg2.extras.RealDictCursor)
            cur = conn.cursor()
            cur.execute("SELECT * FROM loc_references_{0} limit 10;".format(genome))
            results = cur.fetchall()
            for r in results:
                f.write(pack_flatfile_bytes(r))
    
            conn.close()
    
            raise Exception()
        
    
def retrieve_lines_from_flatfile(genome, lines):
    fpath = bytepack_file_template.format(genome)
    with open(fpath) as f:
        lines = [unpack_flatfile_bytes(extract_bytes_by_line(e,f)) for e in lines]
    return lines
    

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
    sequences =[ bytes_to_sequence(shm_genome_bytes[5*m:5*m+5]) for m in matches]
    results = retrieve_lines_from_flatfile(genome, matches)
    for i,r in enumerate(results):
        results[i]["sequence"] = sequences[i]
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

bytes_rev_translation_dict = dict([(v,k) for k,v in bytes_translation_dict.iteritems()])

def bytes_to_sequence(inp_bytes):
    assert len(inp_bytes) == 5
    out_str = ""
    for b in inp_bytes:
        out_str +=bytes_rev_translation_dict[b]
    return out_str
        

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
    print "GENOME: {0}".format(genome)
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
    if args.program == "flatfile":
        #print "creating the packed locus file"
        #create_packed_locs_file(args.genome)
        #print retrieve_lines_from_flatfile(args.genome,[0,1])
        shm_genome_bytes = get_library_bytes_shm(args.genome)
        matches = [0,1,2]
        sequences =[ bytes_to_sequence(shm_genome_bytes[5*m:5*m+5]) for m in matches]
        results = retrieve_lines_from_flatfile(args.genome, matches)
        print results
        print sequences

    if args.program == "ref":
        init_reference_dictionary(args.genome)
    if args.program == "create":
        create_locs_file(args.genome)
    if args.program == "convert":
        convert_library_bytes_shm(args.genome)
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





