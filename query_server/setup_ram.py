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


def translate(sequence):
    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3,
                   "N":4}
    return np.array([translation.get(let,4) for let in sequence], np.int8)

def save_flatfile(table, nlines):
    RD_PATH = os.path.join(RD_DATAROOT,"{0}_{1}.npy".format(table,nlines))
    
    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3,
                   "N":4}
    letters = 20
    all_seqs = np.zeros((nlines, letters), np.int8)

    #enter only some lines... change later
    for i,l in enumerate(open("/tmp/ramdisk/crispr/alllocs.txt")):
        if i >= nlines:
            break
        row = l.split("\t")
        all_seqs[i] = [translation.get(let,4) for let in row[3].strip()[:-3]]
        if i %1e6 == 0:
            print "millions: {0}".format(i/1e6)


    with open(RD_PATH, 'w') as f:
        np.save(f,all_seqs)
    print "saved {0} lines".format(len(all_seqs))


def init_library_bytes(table, nlines):
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_{1}_bytes.npy".format(table,nlines))

    #enter only some lines... change later    
    bytes_array = np.zeros(nlines * 4, dtype = np.dtype("uint8"))
    for i,l in enumerate(open("/tmp/ramdisk/crispr/alllocs.txt")):
        if i >= nlines:
            break
        for j in range(4):
            #translate four characters from the library
            row = l.split("\t")
            seq =  row[3].strip()[:-3]
            bytes_array[4*i + j] = bytes_translation_dict.get(seq[(1+j)*4:(1+j)*4+4],0)
        
        if i %1e6 == 0:
            print "millions: {0}".format(i/1e6)



    with open(LIBRARY_BYTES_PATH,'w') as f:
        np.save(f, bytes_array)
    print "saved {0} lines to a bytes array at {1}".format(nlines, LIBRARY_BYTES_PATH)
        
    

def query_library_bytes(table, nlines):  
    print "starting query, loading lib"
    LIBRARY_BYTES_PATH =  os.path.join(RD_DATAROOT,"{0}_{1}_bytes.npy".format(table,nlines))

    with open(LIBRARY_BYTES_PATH) as f:
        library_bytes = np.load(f)

    print "loaded lib, setting up query bytes"
    tests = []
    for e in re.compile(">", re.M).split(ltests.strip()):
        if not e: continue
        match = re.compile( "(?P<id>.*)\n(?P<guide>\S{20})\s*(?P<nrg>\S{3})",re.M).search(e)
        tests.append(match.groupdict())

        
    query_bytes = np.array([bytes_translation_dict[tests[0]["guide"][(1+j)*4:(1+j)*4+4]] 
                            for j in range(4)],
                            dtype=np.dtype("uint8"))
    threshold_mismatches = 4
    bits_mismatch_threshold = threshold_mismatches * 2

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

def load_flatfile(table, nlines):
    RD_PATH = os.path.join(RD_DATAROOT,"{0}_{1}.npy".format(table,nlines))

    
    times = [utcnow()]
    with open(RD_PATH) as f:
        all_seqs = np.load(RD_PATH)

    times+=[utcnow()]
    print "loaded {0} records in {1} seconds".format(all_seqs.shape, times[1] - times[0])
    
    tests = []
    for e in re.compile(">", re.M).split(ltests.strip()):
        if not e: continue
        match = re.compile( "(?P<id>.*)\n(?P<guide>\S{20})\s*(?P<nrg>\S{3})",re.M).search(e)
        tests.append(match.groupdict())

    tests_array = np.array([translate(e["guide"]) for e in tests ])
    times +=[utcnow()]
    min_matches = 15
    
    method = "cdist"
    if method=="numpy":
        sims_1 = np.greater_equal(np.sum(np.equal(all_seqs[:,np.newaxis,:]-tests_array[np.newaxis,:,:],0),2),min_matches)
        times +=[utcnow()]
        matches_1 = np.nonzero(sims_1)
        times+= [utcnow()]
    elif method == "cdist":
        from scipy.spatial.distance import cdist
        dists = cdist(all_seqs, tests_array, 'hamming')
        times +=[utcnow()]
        matches_bool = np.less_equal(dists, float((20 - min_matches)) /20)
        print dists[:10]
        matches_1 = np.nonzero(matches_bool)
        times+= [utcnow()]
        
    

    print np.shape(matches_1), np.shape(dists)
    print "n_matches: {0} ({1}queries) (<{2}MM".format(  sum(len(e) for e in matches_1) , len(tests_array), min_matches )
    print "computed one sims (matches) in {0} ({1})".format(times[-2] - times[-3],
                                                            times[-1] - times[-2])


    
def compute_similarities(table, nlines):
    global cur



    RD_PATH = os.path.join(RD_DATAROOT,"{0}_{1}.pickle".format(table,nlines))
    cmd = "select * from {0}_sequence order by id limit {1};".format(table, nlines)

    print "executing: "
    print cmd
    print  

    labels, dts = [], []
    dts.append(utcnow())
    labels.append("start")

    global conn, cur, locsfile
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()

    cur.execute(cmd)

    dts.append(utcnow())
    labels.append("executed")

    lines = cur.fetchall()
    dts.append(utcnow())
    labels.append("fetched")

    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3}
    max_lines = len(lines)
    letters = 20

    all_seqs = np.zeros((max_lines, 20), np.int8)
    dts.append(utcnow())
    labels.append("allocated array")


    #enter only some lines... change later
    for l in lines:
        if l[0] < max_lines:
            all_seqs[l[0] - 1] = [translation[let] for let in l[1]]

    dts.append(utcnow())
    labels.append("populated array")


    min_matches = 15
    ns = len(all_seqs)
    lils = sparse.lil_matrix(( ns ,ns ))
    #for i in range(ns):

    sims_array = np.sum(np.equal(all_seqs[:,np.newaxis,:] - all_seqs[np.newaxis,:,:], 0),2)
    print sims_array.shape
    #nz = np.nonzero(np.greater_equal(sims_array,min_matches))
    #print nz.shape

    lils[0,0] = sims_array[0,0]
    #    if i % (ns/3) == 0:
    #        print "{0:05} ({1}/{2})".format(float(i) / len(all_seqs), i, len(all_seqs))

    dts.append(utcnow())
    labels.append("ran through {0} sims".format(len(all_seqs)))

    with open(RD_PATH, 'w') as f:
        pickle.dump(lils, f)

    dts.append(utcnow())
    labels.append("wrote pickle output")

    for i in range(len(dts) -1):
        print "seconds to {1}: {0}".format((dts[i+1] - dts[i]), labels[i+1])
        
    print "microseconds per item: {0}".format(((dts[5] - dts[4]).seconds * 1e6 +(dts[5] - dts[4]).microseconds)  / len(all_seqs))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--program', '-p', dest="program",
                        default='save', type=str,
                        help="program to run -- default, save, allowed: [save,load,sim]")
    parser.add_argument('--nlines','-n',dest="nlines",
                        default=1000,type=int,
                        help="number of lines")
    parser.add_argument('--table','-t',dest="table",
                        default="locs10mt_ram",type=str,
                        help="table name to query")

    args = parser.parse_args()
 
    if args.program == "sim":
        compute_similarities(args.table, args.nlines)
    elif args.program == "save":
        save_flatfile(args.table, args.nlines)
    elif args.program == "load":
        load_flatfile(args.table, args.nlines)
    elif args.program == "init":
        init_library_bytes(args.table,args.nlines)
    elif args.program == "query":
        query_library_bytes(args.table, args.nlines)
if __name__ == "__main__":
    main()





