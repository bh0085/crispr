'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job, Spacer, Hit
import numpy as np
import genome_io as gio




def compute_hits(job_id):
    '''
    computes off and on-target hits for all guide sequences of JOB
    '''
    job = Session.query(Job).get(job_id)
    if job.computing_hits:
        raise Exception("already computing hits")
    job.computing_hits = True
    print "check to make sure computing hits works without session.add()"

    table_prefix = "loci10mt"
    if not job.computed_spacers:
        raise Exception("no spacers yet computed")
        

    jp = gio.get_job_path(job_id)
    query_file = os.path.join(jp,"query.txt")
    with open(query_file,'w') as qf:
        qf.write("\n".join([e.guide for e in job.spacers]))
    cmd =  "submit_query.py -l .7 -t {2} -q {0} -i {1}".format( query_file, job_id, table_prefix)
    prc = spc.Popen(cmd, shell=True)
    return False


def check_hits(job_id):
    '''
    checks files in the job path to determine whether a query is completed
    '''
    p = gio.get_job_path(job_id)
    done = "summary.txt" in os.listdir(p)
    failed = "failed" in os.listdir(p)
    if done:
        return True
    elif failed:
        raise Exception("job failed: {0}").format(job_id)
    else:
        return False

#this should store the rows in the webserver backend "hit" table
#
def enter_hits(job_id):
    job = Session.query(Job).get(job_id)
    if job.computed_hits:
        raise Exception("already computed hits")

    p = os.path.join(gio.get_job_path(job_id),"matches.txt")
    cols = ["id", "sequence", "chr", "start", "strand"]    

    #parse file IO from DB query
    with open(p) as f:
        hits = [dict([[ cols[i], e] 
                      for i,e in enumerate(r.strip().split("\t"))]) \
                for r in f.readlines()]
        
    #translate spacers, hits into numbers to compute sims with numpy
    spacers = job.spacers
    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3}
    all_hits = np.array([[translation[let] for let in e["sequence"]] for e in hits])
    all_spacers = np.array([[translation[let] for let in e.guide] for e in spacers])
    hit_length = 20;
    min_matches = 10;
    sims_array = np.sum(np.equal(all_spacers[:,np.newaxis,:] - all_hits[np.newaxis,:,:], 0),2)

    #generates a similarity matrix of spacers, hits
    hits_by_spacer = np.nonzero(np.greater_equal(sims_array,min_matches))
    

    #creates hits for every spacer
    for idx_s, idx_h in zip(*hits_by_spacer):
        spacer = spacers[idx_s]
        hit = hits[idx_h]
        Session.add(Hit(spacer = spacer,
                        chr = hit["chr"],
                        sequence = hit["sequence"],
                        similarity = float(sims_array[idx_s,idx_h]) / hit_length,
                        start = hit["start"],
                        strand = hit["strand"],
                        ontarget = False
                    ))
    job.computed_hits = True
    Session.add(job)


    return True


def retrieve_hits(job_id):
    job = Session.query(Job).get(job_id)
    if not job.computed_hits:
        raise Exception("haven't computed hits")
    spacers = job.spacers
    return [h.toJSON() for s in spacers for h in s.hits ]
    
