#!/usr/bin/env python

import gffutils
import sys, os
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from Bio import SeqIO


def main(assembly):
    db= gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)

    
    refseq_root = "/fastdata/refseq/"

    with open(os.path.join(refseq_root,"mrnas/","{0}.refseq.fa".format(assembly)),"w") as fopen:
        mrnas = list( db.features_of_type("mRNA"))
        records =  [SeqRecord(Seq(
            mrna.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly)),
            generic_dna),
                              id = mrna.id,
                              description =  "mrna sequence eid_{0} for gene gid_{1} in assembly_{2}".format(mrna.id,mrna.attributes["gene"][0],assembly))
                
                    for mrna in mrnas]
        SeqIO.write(records, fopen, "fasta")
        
if __name__ =="__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--genome', '-g', dest = "genome", type = str,
                        help = "genome name [...]", required = True)
    args = parser.parse_args()
    assembly = args.genome
    main(assembly)
    
