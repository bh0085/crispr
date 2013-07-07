#!/usr/bin/env python

import psycopg2
from scipy import sparse
import argparse
import os, numpy as np


RD_DATAROOT = "/tmp/ramdisk/crispr"
if not os.path.isdir(RD_DATAROOT):
    os.makedirs(RD_DATAROOT)

def compute_similarities(table, nlines):
    global cur

    RD_PATH = os.path.join(RD_DATAROOT,"{0}_{1}.pickle".format(table,nlines))

    cur.execute("select * from {0}_sequence  order by id limit {1} ;".format(table, nlines))
    lines = cur.fetchall()
    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3}
    all_seqs = np.array( [[translation[let] for let in e[1]] for e in lines])
    min_matches = 15
    lil_sparse = sparse.lil.lil_matrix( len(all_seqs), len(all_seqs) )
    for i in range(1): #len(all_seqs)):
        sims_array = np.sum(np.equal(all_seqs[i][np.newaxis,:] - all_seqs[:,:], 0),1)
        hits_by_spacer = np.nonzero(np.greater_equal(sims_array,min_matches))
    print len(hits_by_spacer)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nlines','-n',dest="nlines",
                        default=10000,type=int,
                        help="number of lines to enter into a sparse similarity matrix")
    parser.add_argument('--table','-t',dest="table",
                        default="all_ram",type=str,
                        help="table name to query")
    args = parser.parse_args()
    global conn, cur, locsfile
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()

    compute_similarities(args.table, args.nlines)

if __name__ == "__main__":
    main()
