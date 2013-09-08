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

def init_library_bytes(nlines):
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_bytes.npy".format(nlines))

    #enter only some lines... change later    
    bytes_array = np.zeros(nlines * 5, dtype = np.dtype("uint8"))
    for i,l in enumerate(open("/tmp/ramdisk/crispr/alllocs.txt")):
        if i >= nlines:
            break
        for j in range(5):
            #translate four characters from the library
            row = l.split("\t")
            seq =  row[3].strip()[:-3]
            bytes_array[5*i + j] = bytes_translation_dict.get(seq[(j)*4:(j)*4+4],0)
        
        if i %1e6 == 0:
            print "millions: {0}".format(i/1e6)



    with open(LIBRARY_BYTES_PATH,'w') as f:
        np.save(f, bytes_array)
    print "saved {0} lines to a bytes array at {1}".format(nlines, LIBRARY_BYTES_PATH)
        
    

def query_library_bytes(nlines):  
    print "starting query, loading lib"
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_bytes.npy".format(nlines))

    with open(LIBRARY_BYTES_PATH) as f:
        library_bytes = np.load(f)

    print "loaded lib, setting up query bytes"
    tests = []
    for e in re.compile(">", re.M).split(ltests.strip()):
        if not e: continue
        match = re.compile( "(?P<id>.*)\n(?P<guide>\S{20})\s*(?P<nrg>\S{3})",re.M).search(e)
        tests.append(match.groupdict())

        
    query_bytes = np.array([bytes_translation_dict[tests[0]["guide"][(j)*4:(j)*4+4]] 
                            for j in range(5)],
                            dtype=np.dtype("uint8"))
    threshold_mismatches = 4
    bits_mismatch_threshold = threshold_mismatches

    f = library_bytes
    g = query_bytes
    h = np.zeros((len(library_bytes)/len(query_bytes),), dtype = np.dtype("uint32"))

    print "running comparison"
    import bc

    times = [utcnow()]
    n_matches = bc.striding_8bit_comparison(f,g,h,bits_mismatch_threshold)
    times+=[utcnow()]
    compare_time = times[1] - times[0]
    print "compared {0} matches in {1} ({2} microsec/ million)".format(len(library_bytes), compare_time,(compare_time.seconds * 1e6 + compare_time.microseconds)/(float(len(library_bytes)/1e6)) )
    matches_list = h[:n_matches]
    
    print "done comparing, computing NZ elts"
    #matches = np.nonzero(h)[0]
    print "python, n_matches: {0}".format(n_matches)
    print "first match: {0}".format(matches_list[0])


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--program', '-p', dest="program",
                        default='save', type=str,
                        help="program to run -- default, save, allowed: [save,load,sim]")
    parser.add_argument('--nlines','-n',dest="nlines",
                        default=1000,type=int,
                        help="number of lines")
    args = parser.parse_args()

    if args.program == "init":
        init_library_bytes(args.nlines)
    elif args.program == "query":
        query_library_bytes(args.nlines)
if __name__ == "__main__":
    main()





