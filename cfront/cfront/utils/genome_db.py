'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job, JobERR, Spacer, Hit
import numpy as np
from numpy import *
import genome_io as gio
import random
import itertools as it


def compute_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    #error checking... this should never occur
    if spacer.computing_hits:
        raise Exception("already computing hits")
    spacer.computing_hits = True
    
    #query file IO
    jp = gio.get_job_path(job.id)
    query_file = os.path.join(jp,"query_s{0}.txt".format(spacer_id))
    with open(query_file,'w') as qf:qf.write(spacer.guide)

    cmd = "bowtie.py -q {0} -j {1} -s {2}".format(spacer.guide,job.id,spacer_id)
    prc = spc.Popen(cmd, shell=True)
    return False





def check_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job
    
    #filesystem checks for completion
    p = gio.get_job_path(job.id)
    done = "matches_s{0}.txt".format(spacer_id) in os.listdir(p)
    failed = "failed_s{0}" in os.listdir(p)
    if done:
        return True
    elif failed:
        raise Exception("job failed: {0}").format(job.id)
    else:
        return False

weights =  array([0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]);
def enter_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    #filesystem IO
    p = os.path.join(gio.get_job_path(job.id),"matches_s{0}.txt".format(spacer_id))
    cols = ["spacer_id", "sequence", "chr", "start", "strand","nrg"]    
    
    with open(p) as f: hits = [dict([[ cols[i], e] for i,e in enumerate(r.strip().split("\t"))]) for r in f]
    
    translation = {"A":0,"G":1, "T":2,"C":3}
    spacer_hits =dict([(k,list(g)) for k,g in  it.groupby(sorted(hits, key = lambda x:x["spacer_id"]), key = lambda x:int(x["spacer_id"]))])

    if not spacer_id in spacer_hits: 
        JobERR(job, Job.ERR_MISSING)
        return
    if len(spacer_hits) != 1: 
        JobERR(job,Job.ERR_TOOMANY)
        return

    #processes hits by spacer
    for spacer_id, hits_rows in spacer_hits.items():
        hits_array = np.array([[translation.get(let,4) 
                                for let in e["sequence"]] for e in hits_rows])
        spacer = Session.query(Spacer).get(spacer_id)

        #error checking... does a spacer already have a score?
        if spacer.computed_hits:
            raise Exception("already computed hits")

        #translate spacers, hits into numbers to compute sims with numpy
        spacer_array = np.array([translation.get(let,4) for let in spacer.guide])
        nz = array(nonzero(not_equal(spacer_array[newaxis,:],hits_array))).transpose()
        mismatches_by_hit = dict([(k,array([e[1] for e in g])) 
                                  for k,g in \
                                  it.groupby(nz,key = lambda x:x[0])])

        found_ontarget = None
        for idx,h in enumerate(hits_array):
            hit = hits_rows[idx]
            mismatches = mismatches_by_hit.get(idx,array([]))
            
            if len(mismatches) > 5:
                continue
            if len(mismatches) == 0:
                if found_ontarget: raise Exception("no multiple ontargets")
                else: found_ontarget = True  
                score = 100
            else:
                score = 100 * (1 - weights[mismatches]).prod()
                if len(mismatches) > 1:
                    mean_pairwise =float(sum(mismatches[1:] - mismatches[:-1])) / (len(mismatches)-1)
                    mpw_factor = ((float((19-mean_pairwise))/19)*4 + 1)
                    scl_factor = pow(len(mismatches),2)
                    
                    if hit["sequence"] == 'GAGTCAAACATGCATGCGCC':
                        print mpw_factor, scl_factor, score
                    score  = score / ( mpw_factor * scl_factor )
                score = max([score,0])

            Session.add(Hit(spacer = spacer,
                        chr = hit["chr"],
                        sequence = hit["sequence"] +hit["nrg"],
                        n_mismatches = len(mismatches),
                        start = hit["start"],
                        strand = 1 if hit["strand"] == "+" else -1,
                        score = score
                    ))

        ot_sum = sum(h.score for h in spacer.hits if not h.ontarget)
        spacer.score =100 / (100 + sum(h.score for h in spacer.hits if not h.ontarget))
        print "spacer: {1}(J{0}) -- {2}  N_OTS: {3}, TOTSCORE {4}".format(spacer.jobid, spacer.id, spacer.score, len(spacer.hits) - 1, ot_sum)

    return True



