#!/usr/bin/env bash

source venv/bin/activate

#get assembly name for file naming from arg1
export ASSEMBLY=$1

#download gff3 file from arg 2 url 
wget $2 -O /fastdata/zlab-genomes/gff3/${ASSEMBLY}.gff3.gz
gunzip /fastdata/zlab-genomes/gff3/${ASSEMBLY}.gff3.gz

echo $ASSEMBLY
cfront/scripts/init_gffutils.py $ASSEMBLY
cfront/scripts/download_refseq.py -g $ASSEMBLY
cfront/scripts/install_bowtie.py -g $ASSEMBLY

#build bow tie indexes
#bowtie-build /fastdata/refseq/${ASSEMBLY}.refseq.fa /fastdata/bowtie/${ASSEMBLY}.bowtie.1 
#bowtie-build /fastdata/refseq/mrnas/${ASSEMBLY}.refseq.fa /fastdata/bowtie/${ASSEMBLY}.bowtie.mrna.1 



#db = gffutils.create_db("hg38.ucsc.gtex.gtf", dbfn='hg38.ucsc.gtex.db', force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)
