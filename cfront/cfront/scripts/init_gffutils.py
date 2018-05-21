#!/usr/bin/env python
import gffutils
import pprint
import argparse


def reset_genome(genome):

    in_file = "/fastdata/zlab-genomes/gff3/{0}.gff3".format(genome)
    db = gffutils.create_db(in_file, dbfn='/fastdata/zlab-genomes/gffutils/{0}.db'.format(genome), force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='process a genome with gffutils')
    parser.add_argument('genome', type=str, help='genome name')

    args = parser.parse_args()
    genome = args.genome

    print "initializing gffutils database for {0}".format(genome)
    reset_genome(genome)
    print "complete genome db for {0}".format(genome)
