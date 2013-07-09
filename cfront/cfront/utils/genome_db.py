'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job, Spacer, Hit
import numpy as np
import genome_io as gio




def compute_hits(spacer_id):
    '''
    computes off and on-target hits for all guide sequences of JOB
    '''
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    if spacer.computing_hits:
        raise Exception("already computing hits")
    spacer.computing_hits = True

    print "check to make sure computing hits works without session.add()"

    table_prefix = "locs10mt_ram"

        

    jp = gio.get_job_path(job.id)
    query_file = os.path.join(jp,"query_s{0}.txt".format(spacer_id))
    with open(query_file,'w') as qf:
        qf.write(spacer.guide)
    cmd =  "submit_query.py -l .5 -t {3} -q {0} -j {1} -s {2}".format( query_file, job.id, spacer_id, table_prefix)
    prc = spc.Popen(cmd, shell=True)
    return False


def check_hits(spacer_id):
    '''
    checks files in the job path to determine whether a query is completed
    '''
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job
    p = gio.get_job_path(job.id)
    done = "summary_s{0}.txt".format(spacer_id) in os.listdir(p)
    failed = "failed_s{0}" in os.listdir(p)
    if done:
        return True
    elif failed:
        raise Exception("job failed: {0}").format(job.id)
    else:
        return False

#this should store the rows in the webserver backend "hit" table
#
def enter_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    if spacer.computed_hits:
        raise Exception("already computed hits")

    p = os.path.join(gio.get_job_path(job.id),"matches_s{0}.txt".format(spacer_id))
    cols = ["id", "sequence", "chr", "start", "strand"]    

    #parse file IO from DB query
    with open(p) as f:
        hits = [dict([[ cols[i], e] 
                      for i,e in enumerate(r.strip().split("\t"))]) \
                for r in f.readlines()]
        
    #translate spacers, hits into numbers to compute sims with numpy
    translation = {"A":0,
                   "G":1,
                   "T":2,
                   "C":3}
    all_hits = np.array([[translation[let] for let in e["sequence"]] for e in hits])
    all_spacers = np.array([translation[let] for let in spacer.guide])

    if len(all_hits) > 0 and len(all_spacers) > 0:
        hit_length = 20;
        min_matches = 10;
        print all_spacers, all_hits
        sims_array = np.sum(np.equal(all_spacers[np.newaxis,:] - all_hits[:,:], 0),1)
        
        #generates a similarity matrix of spacers, hits
        accepted_hits = np.nonzero(np.greater_equal(sims_array,min_matches))[0]
        for idx_h in accepted_hits:
           hit = hits[idx_h]
           is_ontarget =  True if hit_length ==  sims_array[idx_h] else False
           Session.add(Hit(spacer = spacer,
                           chr = hit["chr"],
                           sequence = hit["sequence"],
                           similarity = float(sims_array[idx_h]) / hit_length,
                           start = hit["start"],
                           strand = hit["strand"],
                           ontarget = is_ontarget
                       ))
    
    spacer.computed_hits = True
    return True

