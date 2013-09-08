#!/usr/bin/env python
# Configures exon databases used by the CRISPR server to get labels
# for offtarget hits.
#

import os, StringIO
import psycopg2    
import random
             

def genes_file(genome_name):
    return os.path.join(os.environ["HOME"],"data/zlab/ben/ucsc/{0}-genes.tsv".format(genome_name))

#simple code takes every one of a list of hits and runs a SQL query on an indexed
#database containing all UCSC exons.
def get_hit_genes(hits, genome_name):
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()


    updates = ",".join( ["({0},'{1}',{2})".format(h.id,h.chr,h.start) 
                                        for h in hits]
    )
    
    if genome_name != "hg19":
        raise Exception()

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
    FROM {0}, {2}
    WHERE  ({0}.start+20+100) > {1}.exon_start
    AND ({0}.start-100 - 5000) < {1}.exon_start
    """\
        .format("hits_{0}".format(int(random.random() * 10000000 )),
                "exon_{0}".format(genome_name),
                genome_name,
                updates,
                
        )    
    
    cur.execute(cmd)
    results = cur.fetchall()
    conn.close()
      
    hits_by_id = dict([(h.id, h) for h in hits])
    genes_by_hitid = dict[(h.id, None) for h in hits])
    for r in results:
        h = hits_by_id[r[0]]
        if h.chr == r[2]:
            #print "accepted {0}".format(h.gene)
            if h.start > r[3] - 100:
                if h.start < r[4] + 100 + 20:
                    hits_by_id[h.id] = r[1]
    return hits_by_id


def populate_exons(genome_name):
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
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
    exon_cols = ["id","gene_name","exon_number","chr","strand","start","end","protein_id","cds_start","cds_end"]
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
                                                           row["proteinID"] if row["proteinID"] !="" else None,
                                                           row["cdsStart"],
                                                           row["cdsEnd"]]]) + "\n"
                id_counter+=1
                buf.write(buffered_row)
    

    buf.seek(0)
    buf.seek(0)
    cur.copy_from(buf,"exon_{0}".format(genome_name))
    buf.close()
    conn.commit()

def create_indexes(genome_name):
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()
    cur.execute("""
    CREATE INDEX exon_start_idx ON exon_{0}(exon_start);
    CREATE INDEX cds_start_idx ON exon_{0}(cds_start);
    CREATE INDEX exon_end_idx ON exon_{0}(exon_end);
    CREATE INDEX cds_end_idx ON exon_{0}(cds_end);
    CREATE INDEX chr_idx ON exon_{0}(chr);
    CREATE INDEX strand_idx ON exon_{0}(strand);
    """.format(genome_name))
    conn.commit()
    return
                
if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--genome', '-g', dest = "genome_name",
                        default="hg19", type = str,
                        help = "genome name [hg19]")
    args = parser.parse_args()

    populate_exons(args.genome_name)
    create_indexes(args.genome_name)

