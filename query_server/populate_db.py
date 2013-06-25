#!/usr/bin/env python
'''
populates a postgres database with CRISPR loci
computes the distribution of letters in each locus
and builds an index on that distribution
'''

import os, argparse, psycopg2


DATAPATH=os.path.join(os.environ['HOME'],'data/zlab/vineeta')
locs1k = os.path.join(DATAPATH,'locs1k.txt')
locsall = os.path.join(DATAPATH,'all_loci.txt')

bytes_10k = 10000000 #273,000 lines
bytes_1m =  1000000000 #27M lines


def populate_range_tables():
    '''
    Populates tables indexed by letter distribution for a range query.
    '''
    conn  = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    init_table = """
    CREATE TABLE loci10m (
        id        int PRIMARY KEY,
        seq       char(20) NOT NULL,
        A         smallint,
        T         smallint,
        G         smallint,
        C         smallint
    );
    
    

    """
    """
    CREATE INDEX loci_trgm_idx on loci10m using gist (seq extensions.gist_trgm_ops);
    """
    cur.execute(init_table)
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    rows = fetch_data()
    for r in rows:
            generic_insert = """INSERT INTO loci10m (""" + ", ".join(r.keys())+ """) VALUES ( %s, %s, %s, %s, %s, %s)"""
            cur.execute(generic_insert,r.values()) 
    conn.commit()
    conn.close()


def populate_trgm_tables(table,nlines):
    '''
    Populates tables indexed by GIST for a trigram query.
    '''
    conn  = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    tablename = table
    init_table = """
    CREATE TABLE {0} (
        id        int PRIMARY KEY,
        seq       varchar(20) NOT NULL
    );
    
    """.format(tablename)
    make_index =  """
    CREATE INDEX loci_trgm_idx on loci10m using gist (seq extensions.gist_trgm_ops);
   """
    cur.execute(init_table)
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    cols = ["id", "seq"]
    generic_insert = ("""INSERT INTO {0} (""" + ", ".join(cols)+ """) VALUES ( %s, %s)""").format(tablename)

    with open(locsall) as f:
        for i,l in enumerate(f):
            if i > nlines:
                break
            row = dict(id=i, seq= l.split("\t")[3].strip()[:-3])
            cur.execute(generic_insert,[row[c] for c in cols])
            if i %100000 == 0:
                print "{0:2} ({1} / {2})".format( float(i) / nlines, i, nlines)
    conn.commit()
    conn.close()




def query_trgm_tables(table):
    query = """
SET search_path TO "$user",public, extensions;
SELECT seq, seq <-> 'GAAAACTTGGTCTCTAAATG'
FROM {0}
ORDER BY seq <-> 'GAAAACTTGGTCTCTAAATG'
LIMIT 10;
""".format(table)
    conn  = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    cur.execute(query)
    print cur.fetchall()
    

if __name__ == "__main__":
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
    parser.add_argument('--nlines','-n',dest="nlines",
                        default=10000,type=int,
                        help="number of lines to enter into db")
    args = parser.parse_args()
    

    if args.reset:
        populate_trgm_tables(args.table,args.nlines)
    if args.query:
        query_trgm_tables(args.table)
