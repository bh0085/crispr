#!/usr/bin/env python

import psycopg2
from scipy import sparse
import argparse
import os, numpy as np, pickle, re
import datetime
utcnow = datetime.datetime.utcnow

global ltests
ltests = """>SpTet1.4
GGCTGCTGTCAGGGAGCTCA TGG
>SpTet2.3
ATGAGATGCGGTACTCTGCA CGG
>SpTet3.2
GGGTAGACCAGAAGCCCGAC TGG
>SaCas9_Tet1.3
GTGTGACTACTGGGCGCTGG GAGAGT
>SaCas9_Tet2.3
AAGGCAGCCAGAGCAGTCAT GAGAGT
>SaCas9_Tet3.4
GAGTTCCGGGGTGTCGCTGG GGGGGT
>SaCas9_Tet3.5
GAGGTACAGGCCAGGAGTTC CGGGGT
>SaCas9_Tet3.6
TAGCTGCTCCAGTTCTGCCA TAGGGT
>SpDnmt3a_1
TTGGCATGGGTCGCTGACGG AGG
>SpDnmt1_1
CGGGCTGGAGCTGTTCGCGC TGG
>SpDnmt3b 
AGAGGGTGCCAGCGGGTATG AGG
>SaDnmt3a_3
TCTCCGAACCACATGACCCA GCGAGT
>SaDnmt1_8
AGAATGGTGTTGTCTACCGA CTGGGT
>SaDnmt3b_2
GCAGGGCCGCCACCATGTGC AGGAGT"""


RD_DATAROOT = "/tmp/ramdisk/crispr"
if not os.path.isdir(RD_DATAROOT):
    os.makedirs(RD_DATAROOT)

bytes_translation_dict = dict([(e,i) for i,e in enumerate([l0+l1+l2+l3 for l0 in "ATGC" for l1 in "ATGC" for l2 in "ATGC" for l3 in "ATGC"])])

open_libraries = {}
open_references = {}

def raw_locs_file(genome):
    return os.path.join(RD_DATAROOT,"{0}/alllocs.txt".format(genome))

def library_file(genome):
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_bytes.npy".format(genome))
    return LIBRARY_BYTES_PATH

def reference_file(genome):
    REFERENCE_PATH =  os.path.join(RD_DATAROOT,"{0}_{1}_reference.pickle".format(genome))
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
    print "saved lines to a bytes array at {1}".format(LIBRARY_BYTES_PATH)
    
def init_reference_dictionary(genome):
    REFERENCE_PATH = reference_file(genome)
    lines = []
    with open(raw_locs_file(genome)) as f:
        for l in f:
            d = dict(zip(["chr","start","strand","sequence"],
                                  [e.strip() for e in l.split("\t")]))
            d["nrg"] = d["sequence"][-3:]
            d["sequence"] = d["sequence"][:-3]

            lines.append(d)
                    
            if i %1e6 == 0:
                print "{0} millions of lines of reference written".format(i/1e6)
    with open(REFERENCE_PATH, 'w') as f:
        pickle.dump(lines, f)
    
def run_sequence_vs_genome(sequence, genome):
    if not genome == "hg19":
        raise Exception("unrecognized genome")
    if not len(sequence) == 20:
        raise Exception("wrong length input sequence")
        
    lfpath  = library_file(genome)
    rfpath  = reference_file(genome)
    
    #inits library if required
    if not lfpath:
        init_library_bytes(genome)
    if not os.path.isfile(rfpath):
        init_reference_dictionary(genome)
        
    #loads and queries the correct genomewide library
    matches = query_library_bytes(genome, sequence)
    
    #retrieve matches from the reference.

def sample_sequence():
    tests = []
    for e in re.compile(">", re.M).split(ltests.strip()):
        if not e: continue
        match = re.compile( "(?P<id>.*)\n(?P<guide>\S{20})\s*(?P<nrg>\S{3})",re.M).search(e)
        tests.append(match.groupdict())
    return tests[0]["guide"]

def query_library_bytes(genome, sequence):  
    if not genome in open_libraries:
        with open(lfpath) as f:
            open_libraries[genome] = np.load(f)
    
    library_bytes = open_libraries[genome]
    query_bytes = np.array([bytes_translation_dict[sequence[(j)*4:(j)*4+4]] 
                            for j in range(5)],
                           dtype=np.dtype("uint8"))
    mismatches_threshold = 4

    f = library_bytes
    g = query_bytes
    h = np.zeros((len(library_bytes)/len(query_bytes),), dtype = np.dtype("uint32"))

    import bc
    n_matches = bc.striding_8bit_comparison(f,g,h,mismatches_threshold)
    matches_list = h[:n_matches]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--program', '-p', dest="program",
                        default='save', type=str,
                        help="program to run -- default, save, allowed: [save,load,sim]")
    parser.add_argument('--genome', '-g', dest = "genome",
                        default="hg19", type = str,
                        help = "target genomic library")

    
    
    args = parser.parse_args()

    if args.program == "init":
        init_library_bytes(args.genome)
        init_library_bytes(args.genome)
    elif args.program == "query":
        query_library_bytes(args.genome, sample_sequence())

if __name__ == "__main__":
    main()





