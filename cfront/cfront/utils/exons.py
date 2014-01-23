#!/usr/bin/env python
''' 
Configures exon databases used by the CRISPR server to get labels for offtarget hits. 
'''

import os, StringIO, argparse
import psycopg2    
import random
from pyramid.paster import bootstrap
from cfront import genomes_settings

def genes_file(genome_name):
    path = genomes_settings.get("ucsc_tsv_template").format(genome_name)
    if not os.path.isfile(path):
        raise Exception("unsupported genome (file ucsc file does not exist) at\n {0}"\
                        .format(path))
    return path


def genes_file_gtf(genome_name):
    path = genomes_settings.get("ensemble_gtf_template").format(genome_name)
    if not os.path.isfile(path):
        raise Exception("unsupported genome (file ENSEMBL file does not exist) at\n {0}"\
                        .format(path))
    return path

#simple code takes every one of a list of hits and runs a SQL query on an indexed
#database containing all UCSC exons.
def get_hit_genes(hits, genome_name):
    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")))
    cur = conn.cursor()


    updates = ",".join( ["({0},'{1}',{2})".format(h.id,h.chr,h.start) 
                                        for h in hits]
    )

    cmd = """
    CREATE TEMP TABLE {0} (
    id int, chr text, start int);
    INSERT INTO {0} VALUES {2};
    
    SELECT 
    {0}.id as exon_id, 
    {1}.gene_name as gene_name,
    {1}.chr as c1,
    {1}.exon_start as s1,
    {1}.exon_end as e1
    FROM {0}, {1}
    WHERE  ({0}.start+20+100) > {1}.exon_start
    AND ({0}.start-100 - 5000) < {1}.exon_start
    """\
        .format("hits_{0}".format(int(random.random() * 10000000 )),
                "exon_{0}".format(genome_name),
                updates,
        )    
    
    cur.execute(cmd)
    results = cur.fetchall()
    conn.close()
      
    hits_by_id = dict([(h.id, h) for h in hits])
    genes_by_hitid = dict([(h.id, None) for h in hits])
    for r in results:
        h = hits_by_id[r[0]]
        if h.chr == r[2]:
            #print "accepted {0}".format(h.gene)
            if h.start > r[3] - 100:
                if h.start < r[4] + 100 + 20:
                    genes_by_hitid[h.id] = r[1]
    return genes_by_hitid


def populate_exons(genome_name):
    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")))
    cur = conn.cursor()

    init_table = """
    DROP TABLE IF EXISTS exon_{0};
    CREATE TABLE exon_{0} (
    id int PRIMARY KEY,
    gene_name VARCHAR(50) not null,
    exon_number SMALLINT not null,
    chr  VARCHAR(25) not null,
    strand SMALLINT not null,
    exon_start INT NOT NULL,
    exon_end INT NOT NULL,
    protein_id VARCHAR(50),
    cds_start INT NOT NULL,
    cds_end INT NOT NULL
    );
    
    """.format(genome_name)
    cur.execute(init_table);
    buf = StringIO.StringIO()
    exon_cols_rs = ['bin',
                    'name',
                    'chrom',
                    'strand',
                    'txStart',
                    'txEnd',
                    'cdsStart',
                    'cdsEnd',
                    'exonCount',
                    'exonStarts',
                    'exonEnds',
                    'score',
                    'name2',
                    'cdsStartStat',
                    'cdsEndStat',
                    'exonFrames']
    #exon_cols = ["id","gene_name","exon_number","chr","strand","start","end","protein_id","cds_start","cds_end"]
    id_counter = 1
    with open(genes_file(genome_name)) as f:
        for exon_id,l in enumerate(f):
            if exon_id==0:
                cols = [e.strip() for e in l[1:].split("\t")]
                continue
            row = dict( [(cols[i],e.strip()) for i,e in enumerate( l.split("\t")) ])
            estarts,eends = row["exonStarts"].split(",")[:-1],row["exonEnds"].split(",")[:-1]

            for j,pair in enumerate(zip(estarts, eends)):
                buffered_row = "\t".join([str(e) for e in [id_counter,
                                                           row["name"],
                                                           j,
                                                           row["chrom"],
                                                           1 if row["strand"] == "+" else -1,
                                                           pair[0],
                                                           pair[1],
                                                           None,
                                                           row["cdsStart"],
                                                           row["cdsEnd"]]]) + "\n"
                id_counter+=1
                buf.write(buffered_row)
    

    buf.seek(0)
    buf.seek(0)
    cur.copy_from(buf,"exon_{0}".format(genome_name))
    buf.close()
    conn.commit()
    print "populated exons for {0}".format(genome_name)


def populate_exons_ensembl(genome_name):
    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")))
    cur = conn.cursor()

    init_table = """
    DROP TABLE IF EXISTS exon_{0};
    CREATE TABLE exon_{0} (
    id int PRIMARY KEY,
    gene_name VARCHAR(50) not null,
    gene_common_name VARCHAR(50),
    exon_number SMALLINT not null,
    chr  VARCHAR(25) not null,
    strand SMALLINT not null,
    exon_start INT NOT NULL,
    exon_end INT NOT NULL,
    protein_id VARCHAR(50),
    cds_start INT NOT NULL,
    cds_end INT NOT NULL
    );
    
    """.format(genome_name)
    cur.execute(init_table);
    buf = StringIO.StringIO()
    cols = ['chrom_num',
            'source',
            'feature',
            'start',
            'end',
            'score',
            'strand',
            'frame',
            'attribute']
    #attribute_cols = ["id","gene_name","exon_number","chr","strand","start","end","protein_id","cds_start","cds_end"]
    attribute_sample_string = '''gene_id "ATMG00160"; transcript_id "ATMG00160.1"; exon_number "1"; gene_name "COX2"; transcript_name "COX2-201"; seqedit "false";'''
    id_counter = 1

    with open(genes_file_gtf(genome_name)) as f:
        for l in f:
            row = dict( [(cols[i],e.strip()) for i,e in enumerate( l.split("\t")) ])
            if row["feature"] != "exon":
                continue
            print row["attribute"]

            attribute = dict([[e.strip().split(" ")[0],
                               " ".join( e.strip().split(" ")[1:] )] 
                              for e in (row["attribute"]+" ").split("; ") if e.strip() != ""])
            

            buffered_row = "\t".join([str(e) for e in [id_counter,
                                                       attribute["gene_id"],
                                                       attribute["gene_name"] if "gene_name" in attribute else "unnamed",
                                                       int(attribute["exon_number"].replace('"',"")),
                                                       "chr" + row["chrom_num"],
                                                       1 if row["strand"] == "+" else -1,
                                                       row["start"],
                                                       row["end"],
                                                       None,
                                                       row["start"],
                                                       row["end"]]]) + "\n"

            id_counter+=1
            buf.write(buffered_row)
    

    buf.seek(0)
    buf.seek(0)
    cur.copy_from(buf,"exon_{0}".format(genome_name))
    buf.close()
    conn.commit()
    print "populated exons for {0}".format(genome_name)


def populate_exons_blank(genome_name):
    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")))
    cur = conn.cursor()

    init_table = """
    DROP TABLE IF EXISTS exon_{0};
    CREATE TABLE exon_{0} (
    id int PRIMARY KEY,
    gene_name VARCHAR(50) not null,
    gene_common_name VARCHAR(50),
    exon_number SMALLINT not null,
    chr  VARCHAR(25) not null,
    strand SMALLINT not null,
    exon_start INT NOT NULL,
    exon_end INT NOT NULL,
    protein_id VARCHAR(50),
    cds_start INT NOT NULL,
    cds_end INT NOT NULL
    );
    
    """.format(genome_name)
    cur.execute(init_table);
    conn.commit()
    print "populated fake exons table for {0}".format(genome_name)

def create_indexes(genome_name):
    conn = psycopg2.connect("dbname={0} user={1} password={2}"\
                            .format(genomes_settings.get("postgres_database"),
                                    genomes_settings.get("postgres_user"),
                                    genomes_settings.get("postgres_password")))
    cur = conn.cursor()
    cur.execute("""
    CREATE INDEX {0}_exon_start_idx ON exon_{0}(exon_start);
    CREATE INDEX {0}_cds_start_idx ON exon_{0}(cds_start);
    CREATE INDEX {0}_exon_end_idx ON exon_{0}(exon_end);
    CREATE INDEX {0}_cds_end_idx ON exon_{0}(cds_end);
    CREATE INDEX {0}_chr_idx ON exon_{0}(chr);
    CREATE INDEX {0}_strand_idx ON exon_{0}(strand);
    """.format(genome_name))
    conn.commit()
    print "created indexes for {0}".format(genome_name)

    return
                
if __name__ =="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--genome', '-g', dest = "genome_name",
                        default="hg19", type = str,
                        help = "genome name [...]", required = True)
    parser.add_argument('--source', '-s', dest="source",
                        default="ucsc", type=str,
                        help = "source ensembl gtf / ucsc tsv", required = True)

    parser.add_argument('inifile')

    args = parser.parse_args()
    env = bootstrap(args.inifile)
    if args.source=="ucsc":
        populate_exons(args.genome_name)
    elif args.source =="ensembl":
        populate_exons_ensembl(args.genome_name)
    elif args.source =="blank":
        populate_exons_blank(args.genome_name)

    create_indexes(args.genome_name)

    
