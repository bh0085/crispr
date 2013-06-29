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
SUMMARY of job: {2:06}
INPUT SEQUENCE {1}
SIMILARITY LIMIT: {3}
DATABASE NAME: {4}
NUMBER ROWS RETURNED {0}
"""

def create_summary(nrows = None,
                   input_seq = None,
                   job_number = None,
                   table = None,
                   limit = None):
    global summary_template
    return summary_template.format(nrows,input_seq,job_number,limit,table)
                  
       
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
    parser.add_argument('--table','-t',dest="table",
                        default="loci10mt",type=str,
                        help="table name to store, query")
    args = parser.parse_args()
    
    #input and output with stdout
    input_seq = sys.stdin.read().strip()
    limit = args.limit
    table = args.table
    query_seq = input_seq
    job_number = len(os.listdir(JOBSPATH))
    job_id = "job_{0:06}".format(job_number)
    job_path = os.path.join(JOBSPATH,job_id)
    os.makedirs(job_path)
    sys.stdout.write(job_id + "\n")
    sys.stdout.close()

    query=  """
    SET search_path TO "$user",public, extensions;
    SELECT set_limit({2}), show_limit();
    SELECT seq, seq <-> '{1}'
    FROM {0}
    WHERE seq % '{1}'
    ORDER BY seq <-> '{1}'
    """.format(table, query_seq, limit)

    global conn, curr
    conn = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    
    job_params = dict(
        nrows = len(rows),
        input_seq = query_seq,
        job_number = job_number,
        limit = limit,
        table = table)

    with open(os.path.join(job_path, "summary.txt"),'w') as f:
        f.write(create_summary(**job_params))
    with open(os.path.join(job_path, "matches.txt"),'w') as f:
        f.write("\n".join("\t".join(["{0}".format(e) for e in r]) for r in rows  ))
    

genomes = ["human", "mouse","rat","zebrafish", "arhabdopsis", "elegans"]
    

if __name__ == "__main__":
    main()


