#!/usr/bin/env python
import gffutils
import pprint
import argparse



def install_expression(genome):
    expression_root = "/fastdata/expression"
    input_file = os.path.join(expression_root,"{0}.expression.gtf".format(genome))
    output_file = os.path.join(expression_root,"{0}.expression.gffutils.db".format(genome))
    print "installing expression file at: {0}".format(output_file)
    print "for new expression files, please visit https://genome.ucsc.edu/cgi-bin/hgTables"

    db = gffutils.create_db(input_file, dbfn=output_file, force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True,gtf_subfeature='transcript')

def genome_idspec(d):
    #if not d.attributes.get("",False): return None
    if d.featuretype == "gene": return d["Name"][0]
    else: return "autoincrement:{0}_{1}".format(d.attributes.get("gene",["unk"])[0],d.featuretype)

def install_gff3_genome(genome):
    in_file = "/fastdata/zlab-genomes/gff3/{0}.gff3".format(genome)
    out_file ='/fastdata/zlab-genomes/gffutils/{0}.db'.format(genome)
    db = gffutils.create_db(in_file,
                            dbfn=out_file,
                            force=True,
                            keep_order=True,
                            merge_strategy='merge',
                            sort_attribute_values=True)   


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='process a genome with gffutils')
    parser.add_argument('--genome','-g', dest="genome", type=str, help='genome name',required=True)
    parser.add_argument('--program', '-p', dest="program", type=str, default='install-genome')

    args = parser.parse_args()
    genome = args.genome

    program = args.program
    if program =="install-genome":
        print "initializing gffutils database for {0}".format(genome)
        install_gff3_genome(genome)
        print "complete genome db for {0}".format(genome)

    if program =="install-expression":
        print "initializing expression database for {0}".format(genome)
        install_expression(genome)
        print "completed expression database for {0}".format(genome)
