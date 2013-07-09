#!/usr/bin/env python

import psycopg2
from scipy import sparse
import argparse
import os, numpy as np, pickle
import datetime
utcnow = datetime.datetime.utcnow


RD_DATAROOT = "/tmp/ramdisk/crispr"
if not os.path.isdir(RD_DATAROOT):
    os.makedirs(RD_DATAROOT)

def save_flatfile(table, nlines):
    global cur
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


def load_flatfile(table, nlines):
    pass

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
    global conn, cur, locsfile
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()

    if args.program == "sim":
        compute_similarities(args.table, args.nlines)
    elif args.program == "save":
        save_flatfile(args.table, args.nlines)
    elif args.program == "load":
        load_flatfile(args.table, args.nlines)

if __name__ == "__main__":
    main()
