#!/usr/bin/env python
import  argparse, datetime, re
from pyramid.paster import bootstrap
from cfront.models import Session, Spacer, Hit, Job
import transaction

def add_jobs(data_tsv):
    cols = ['id', 'sequence', 'date_submitted', 'genome', 'name', 'email', 'date_completed', 'chr', 'start', 'strand', 'computing_spacers', 'computed_spacers', 'files_computing', 'files_ready', 'email_complete', 'key']
    rows = []
    with open(data_tsv) as f :
        for l in f:
            rows.append(dict( zip(cols,[e.strip() for e in  l.split('\t')])  ))
    
    with transaction.manager:
        for r in rows:
            
            sequence = r["sequence"].upper()
            sequence = re.sub("\s","",sequence)
            if re.compile("[^AGTC]").search(sequence) is not None:
                continue

            j = Job(key = r['key'],
                    name = r["name"],
                    email = r["email"],
                    chr = r["chr"],
                    start = r["start"],
                    strand = r["strand"],
                    sequence = sequence,
                    genome = r["genome"],
                    email_complete=True if r["email_complete"] else False,
                    date_submitted = datetime.datetime.utcnow())

            Session.add(j)
            
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inifile",
                        help="inifile to configure the server")
    parser.add_argument("data_tsv",
                        help="data file to read0 jobs from")
    args = parser.parse_args()
    
    #starts up the paster env
    env = bootstrap(args.inifile)
    
    add_jobs(args.data_tsv)


        
