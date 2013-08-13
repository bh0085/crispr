#!/usr/bin/env python
import os, subprocess as spc

lfiles = [ f for f in os.listdir(".") if ".loci" in f ]

for lf in lfiles:
    spacer_id = lf[:-5]
    with open(lf) as f:
        f.seek(0)
        sam_loci = " ".join([e.strip() for e in f.readlines()])
        samtools_string = "samtools faidx /tmp/ramdisk/genomes/mm9.fa {0} > {1}.regions".format(sam_loci,spacer_id)
        print samtools_string
        prc = spc.Popen(samtools_string, shell = True)
        prc.communicate()
        
        

