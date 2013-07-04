#!/usr/bin/env python
'''
populates a postgres database with CRISPR loci
computes the distribution of letters in each locus
and builds an index on that distribution
'''

import os, argparse, psycopg2
import StringIO
global conn
global cur
global locsfile


DATAPATH=os.path.join(os.environ['HOME'],'data/zlab/vineeta')


def populate_trgm_table(table,nlines):
    '''
    Populates tables indexed by GIST for a trigram query.
    '''
    
    global cur
    locus_table = "{0}_locus".format(table)
    seq_table = "{0}_sequence".format(table)
    init_table = """

    CREATE TABLE {0} (
    id INT PRIMARY KEY,
    chr SMALLINT NOT NULL,
    start INT NOT NULL,
    strand SMALLINT NOT NULL,
    nrg varchar(3)
    );
    CREATE TABLE {1} (
        id        int PRIMARY KEY,
        seq       varchar(20) NOT NULL
    );
    
    """.format(locus_table, seq_table)
    cur.execute(init_table)

    cols = ["chr","start","strand","seq23"]
    lcols = ["id","chr","start","strand","nrg"]
    scols = ["id","seq"]

    #buffers for storing sequences, loci for db entry
    global lbuf, sbuf
    lbuf = None
    sbuf = None

    def copy_buffers():
        global lbuf,sbuf
        lbuf.seek(0)
        sbuf.seek(0)
        
        cur.copy_from(lbuf,locus_table)
        cur.copy_from(sbuf,seq_table)

        lbuf.close()
        sbuf.close()
        lbuf = None
        sbuf = None
    def init_buffers():
        global lbuf,sbuf
        lbuf = StringIO.StringIO()
        sbuf = StringIO.StringIO()
    

    with open(locsfile) as f:
        for i,l in enumerate(f):
            if i > nlines:
                break
            if lbuf == None:
                init_buffers()
                
            pkey = i+1
            row = dict( zip( ["id"] + cols, [pkey] + l.strip().split("\t") )) 
            lbuf.write("\t".join([str(e) for e in [row["id"],row["chr"],row["start"],\
                                                        1 if row["strand"] == "+" else -1,\
                                                        row["seq23"][-3:]]])+"\n")
            sbuf.write("\t".join([str(e) for e in [row["id"],row["seq23"][:-3]]])+"\n")
            if i % 1000000 == 0:
                copy_buffers()
                print "{0:2} ({1} / {2})".format( float(i) / nlines, i, nlines)
    if lbuf != None:
        copy_buffers()
    

def index_trgm_table(table):

    locus_table = "{0}_locus".format(table)
    seq_table = "{0}_sequence".format(table)

    global cur
    cur.execute("""
SET search_path TO "$user",public, extensions;
CREATE INDEX ON {0} USING GIST(seq gist_trgm_ops);""".format(seq_table))


def drop_trgm_table(table):
    global cur
    locus_table = "{0}_locus".format(table)
    seq_table = "{0}_sequence".format(table)
    cur.execute("DROP TABLE {0};".format(locus_table))
    cur.execute("DROP TABLE {0};".format(seq_table))

def query_trgm_table(table,limit,query_seq):
    global cur
    locus_table = "{0}_locus".format(table)
    seq_table = "{0}_sequence".format(table)
    query_sql = """
SET search_path TO "$user",public, extensions;
SELECT set_limit({2}), show_limit();  
EXPLAIN ANALYZE SELECT seq, seq <-> '{1}'
FROM {0}
WHERE seq % '{1}'
ORDER BY seq <-> '{1}'
LIMIT 10;
""".format(seq_table, query_seq, limit)

    cur.execute(query_sql)
    for r in cur.fetchall():
        print r

def get_index_size(table):
    global cur

    locus_table = "{0}_locus".format(table)
    seq_table = "{0}_sequence".format(table)

    cur.execute("select pg_size_pretty(pg_total_relation_size('{0}') - pg_relation_size('{0}'));".format(seq_table))
    for r in cur.fetchall(): print r
    cur.execute( "select pg_size_pretty(pg_relation_size('{0}'));".format(seq_table))
    for r in cur.fetchall(): print r
    

def main():
    '''
    runs scripts to populate and test the crispr loci database.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset','-r',dest="reset",
                        default=False,const=True,action="store_const",
                        help="repopulate database from a flatfile") 
    parser.add_argument('--query','-q',dest="query",
                        default=False,const=True,action="store_const",
                        help="profile a test query of tablename") 
    parser.add_argument('--table','-t',dest="table",
                        default="loci1kt",type=str,
                        help="table name to store, query")
    parser.add_argument('--limit','-l',dest="limit",
                        default=.75,type=float,
                        help="query similarity limit (default .8 == 16 bases in common)")
    parser.add_argument('--nlines','-n',dest="nlines",
                        default=10000,type=int,
                        help="number of lines to enter into db")
    parser.add_argument('--make-index','-i',dest="make_index",
                        default=False, const=True, action="store_const",
                        help="create a gist index on TABLE")
    parser.add_argument('--drop', '-d', dest = 'drop',
                        default=False, const=True, action="store_const",
                        help="drops the table TABLE before running")
    parser.add_argument('--size', '-s', dest = 'size',
                        default=False, const=True, action="store_const",
                        help="prints the size of TABLE and associated indexes")
    parser.add_argument('--file','-f',dest="file",
                        default="all_loci.txt",type=str,
                        help="file storing loci to enter into DB")
    args = parser.parse_args()


    if not (args.drop or args.reset or\
            args.make_index or args.query or args.size):
        parser.print_help()
        exit()

    global conn, cur, locsfile
    conn = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    
    if args.file:
        locsfile=os.path.join(DATAPATH,args.file)
    if args.drop:
        drop_trgm_table(args.table)

    if args.reset:
        populate_trgm_table(args.table,args.nlines)
    if args.make_index:
        index_trgm_table(args.table)
    if args.query:
        query_trgm_table(args.table, args.limit,"GAAAACTTGGTCTCTAAATG")
            
    if args.size:
        get_index_size(args.table)

    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    main()
