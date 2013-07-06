'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job

def get_job_path(job_id):
    path =   os.path.join(os.environ["CFRONTDATA"],"jobs/{0}").format(job_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def compute_hits(job_id):
    job = Session.query(Job).get(job_id)
    table_prefix = "loci10mt"
    
    jp = get_job_path(job_id)
    query_file = os.path.join(jp,"query.txt")
    
    if not job.computed_spacers:
        raise Exception("no spacers yet computed")

    with open(query_file,'w') as qf:
        qf.write("\n".join([e.guide for e in job.spacers]))
        
    
    cmd =  "submit_query.py -l .6 -t {2} -q {0} -i {1}".format( query_file, job_id, table_prefix)
    prc = spc.Popen(cmd, shell=True)
    return False

def check_hits(job_id):
    p = get_job_path(job_id)
    done = "summary.txt" in os.listdir(p)
    failed = "failed" in os.listdir(p)
    if done:
        return True
    elif failed:
        return False
    else:
        return False

#this should store the rows in the webserver backend "hit" table
#
def retrieve_hits(job_id):
    p = os.path.join(get_job_path(job_id),"matches.txt")
    cols = ["id", "sequence"]
    with open(p) as f:
        hits = [dict([[ cols[i], e] for i,e in enumerate(r.strip().split("\t"))]) for r in f.readlines()]
    return hits
