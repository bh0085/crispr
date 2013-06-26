#!/usr/bin/env python
'''
Submits a single query to the psql server from a file, "input"
Waits for a response and prints to a file, "output"
'''

import psycopg2,os, argparse

ROOT = os.environ["HOME"]
DATAPATH = os.path.join(ROOT,"data")
JOBSPATH = os.path.join(DATAPATH,"jobs")
if not os.path.isdir(JOBSPATH):
    os.makedirs(JOBSPATH)

def write_sample():
    '''writes a sample (single sequence input to sample-input.txt''')

    input_file = "sample_input.txt"
    sample_seq = "GAAAACTTGGTCTCTAAATG"
    with open(input_file, 'w') as f:
        f.writelines(["\t".join(["0",sample_seq])])
    print "wrote sequence:"
    print sample_seq+"\n"
    print "to input file: {0}".format(input_file)
    
                         

def main():
    '''
    reads input file
    submits a query to the server. 
    enters a wait loop
    writes output file
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', dest="input",
                        required="true", type=str,
                        help="input file")

    parser.add_argument('--output', '-o', dest="output",
                        required="true", type=str,
                        help="output file")
    args = parser.parse_args()
    
    with open(args.input) as f:
        input_lines = f.readlines()
    if len(input_lines) > 1:
        raise Exception("multiple queries currently unsupported")
    id, input_seq = input_lines[0].split('\t')

    global conn, curr
    conn = psycopg2.connect("dbname=vineeta user=ben")
    cur = conn.cursor()

    limit = .75
    query_seq = input_seq
    table = "loci10mt"
    job_number = len(os.listdir(JOBSPATH))
    job_path = os.path.join(JOBSPATH,"job_{0:06}".format(job_number))



    query=  """
    SET search_path TO "$user",public, extensions;
    SELECT set_limit({2}), show_limit();
    EXPLAIN ANALYZE SELECT seq, seq <-> '{1}'
    FROM {0}
    WHERE seq % '{1}'
    ORDER BY seq <-> '{1}'
    """.format(table, query_seq, limit)

    cur.execute(query)
    rows = cur.fetchall()
    for r in rows: print r
    
    with open(os.path.join(job_path, "summary.txt"),w) as f:
        f.writelines(["number of rows\t{0}\n".format(len(rows))])
    
    

if __name__ == "__main__":
    main()
