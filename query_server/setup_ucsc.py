#!/usr/bin/env python
import os, StringIO
import psycopg2
HUMAN_GENES=os.path.join(os.environ["HOME"],"data/zlab/ben/ucsc/hg19-genes.tsv")

def populate_exons():
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()

    init_table = """
    DROP TABLE exon_hg19;
    CREATE TABLE exon_hg19 (
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
    
    """
    cur.execute(init_table);
    buf = StringIO.StringIO()
    exon_cols = ["id","gene_name","exon_number","chr","strand","start","end","protein_id","cds_start","cds_end"]
    id_counter = 1
    with open(HUMAN_GENES) as f:
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
    cur.copy_from(buf,"exon_hg19")
    buf.close()
    conn.commit()

def create_indexes():
    conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
    cur = conn.cursor()
    cur.execute("""
    CREATE INDEX exon_start_idx ON exon_hg19(exon_start);
    CREATE INDEX cds_start_idx ON exon_hg19(cds_start);
    CREATE INDEX exon_end_idx ON exon_hg19(exon_end);
    CREATE INDEX cds_end_idx ON exon_hg19(cds_end);
    CREATE INDEX chr_idx ON exon_hg19(chr);
    CREATE INDEX strand_idx ON exon_hg19(strand);
""")
    conn.commit()
    return
                
if __name__ =="__main__":
    populate_exons()
    create_indexes()

