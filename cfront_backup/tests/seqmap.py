#!/usr/bin/env python
import os, re
from pyramid.paster import bootstrap
from cfront.models import Session, Job, Spacer
from Bio import  SeqRecord, Seq
sr = SeqRecord.SeqRecord
seq = Seq.Seq

#variables used later
ABC = Seq.Alphabet.DNAAlphabet()
OJOIN = os.path.join
ROOT = "/tmp/ramdisk/seqmap"

def setup_all():
    setup_bm0_files()
    setup_bm0_fasta()

def setup_bm0_files():
    locs_file = OJOIN(ROOT,"alllocs.txt")
    locs_ngg_file = OJOIN(ROOT,"locs_ngg.txt")
    with open(locs_file) as lf:
        with open(locs_ngg_file,"w") as lnf:
            for i,l in enumerate(lf):
                if l.strip()[-2:] == "GG":
                    lnf.write(l)
                if i %10000000 == 0:
                    print "L - {0}, ({1})".format(i, l.strip())

def setup_bm0_fasta():
    locs_ngg_file = OJOIN(ROOT,"locs_ngg.txt")
    locs_ngg_fa_file = OJOIN(ROOT, "locs_ngg.fa")
    with open(locs_ngg_file) as f:
        with open(locs_ngg_fa_file, "w") as f2:
            for i,l in enumerate(f):
                
                fields = re.compile("\s").split(l.strip())
                id = "ngg_l{0:09d}".format(i)
                description="chr"+":".join(fields[:-1])
                f2.write(">{0} {1}\n{2}\n".format(id, description, fields[-1]))
                
                if i %1000000 == 0:
                    print "writing FA line: {0}, ({1})".format(i, description)
def bm():
    #try to run seqmap with 500k spacers.
    #see how long it takes to run over the first 1M bases of the human genome
    queries_fa = OJOIN(ROOT, "locs_ngg_500k.fa")
    

def main():
    env = bootstrap("/home/ben/crispr/cfront/development.ini")

if __name__ == "__main__":
    main()
