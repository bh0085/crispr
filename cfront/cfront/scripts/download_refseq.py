#!/usr/bin/env python
from Bio import Entrez, SeqIO
import os
import gffutils
import sys

Entrez.email = 'ben@coolship.io'

root="/fastdata/refseq/"

genomes=["mm10"]



def main(argv=sys.argv):

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--genome', '-g', dest = "genome", type = str,
                        help = "genome name [...]", required = True)

    args = parser.parse_args()
    genome = args.genome
    
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(genome), keep_order=True)
    genes = list(db.features_of_type("gene"))
    accessions = list(set([g.chrom for g in genes]))

    print "downloading accessions from Entres for {0} from genomes {1}".format(len(accessions),genome)
    
    with open(os.path.join(root,"{0}.refseq.fa".format(genome)), 'w') as fopen:
        for i,seq_id in enumerate(accessions):
            print "{0}% for {1}.... ({2})".format(long(10000* i / len(accessions))/100,genome, seq_id)
            handle = Entrez.efetch(db="nucleotide", id=seq_id, rettype="fasta", retmode="text")
            out =handle.read().rstrip()
            
            
            fopen.write("\n".join(out.split("\n"))+"\n")

    print "done!"


if __name__=="__main__":
    main()
