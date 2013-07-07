#!/usr/bin/env python
'''
Submits a single query to the psql server from a file, "input"
Waits for a response and print to stdout
'''

import psycopg2,os, argparse, sys

#ROOT = os.environ["HOME"]
DATAPATH = os.environ["CFRONTDATA"]
JOBSPATH = os.path.join(DATAPATH,"jobs")
if not os.path.isdir(JOBSPATH):
    os.makedirs(JOBSPATH)

def write_sample():
    '''writes a sample (single sequence) input to sample-input.txt'''

    input_file = "sample_input.txt"
    sample_seq = "GAAAACTTGGTCTCTAAATG"
    with open(input_file, 'w') as f:
        f.writelines(["\t".join(["0",sample_seq])])
    print "wrote sequence:"
    print sample_seq+"\n"
    print "to input file: {0}".format(input_file)
    

global summary_template
summary_template =  """
SUMMARY of job: {2}
INPUT SEQUENCE {1}
SIMILARITY LIMIT: {3}
DATABASE NAME: {4}
NUMBER ROWS RETURNED {0}
"""

def create_summary(nrows = None,
                   input_seq = None,
                   job_id = None,
                   table_prefix = None,
                   limit = None):
    global summary_template
    print summary_template
    print job_id
    return summary_template.format(nrows,input_seq,job_id,limit,table_prefix)
                  
       
def main():
    '''
    reads input file from stdin
    writes output path to stdout

    submits a query to the server. 
    enters a wait loop
    writes output file
    '''


    parser = argparse.ArgumentParser()
    parser.add_argument('--limit','-l',dest="limit",
                        default=.8,type=float,
                        help="query similarity limit (default .8 == 16 bases in common)")
    parser.add_argument('--table','-t',dest="table_prefix",
                        default="loci10mt",type=str,
                        help="table name to store, query")
    parser.add_argument('--id','-i',dest="job_id",
                        default="1",type=str,
                        help="job_id for this job")
    parser.add_argument('--query','-q',dest="query",
                        type=str, required=True,
                        help="query input file")
    args = parser.parse_args()
    
    #input and output with stdout
    input_file  = args.query
    with open(input_file) as qs:
        query_seqs = [l.strip() for l in qs.readlines()]

    limit = args.limit
    table_prefix = args.table_prefix
    locus_table = "{0}_locus".format(table_prefix)
    sequence_table = "{0}_sequence".format(table_prefix)

    job_id =args.job_id
    job_path = os.path.join(JOBSPATH,job_id)
    if not os.path.isdir(job_path):
        os.makedirs(job_path)

    query_orstring = " OR ".join([" st.seq % '{0}'".format(e) for e in query_seqs])
        
    sel = ""
    
    query=  """
    SELECT set_limit({3}), show_limit();
    SELECT  st.id, st.seq, lt.chr, lt.start, lt.strand
    FROM {0} as st, {1} as lt
    WHERE ({2}) 
    AND st.id = lt.id
    ORDER BY st.id;
    """.format(sequence_table,locus_table, query_orstring, limit)

    print query

    global conn, curr
    # password=random12345 no password for current production server
    conn = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    job_params = dict(
        nrows = len(rows),
        input_seq = "\n".join(query_seqs),
        job_id = job_id,
        limit = limit,
        table_prefix = table_prefix)

    with open(os.path.join(job_path, "summary.txt"),'w') as f:
        f.write(create_summary(**job_params))
    with open(os.path.join(job_path, "matches.txt"),'w') as f:
        f.write("\n".join("\t".join(["{0}".format(e) for e in r]) for r in rows  ))
    

genomes = ["human", "mouse","rat","zebrafish", "arhabdopsis", "elegans"]
    

if __name__ == "__main__":
    main()


