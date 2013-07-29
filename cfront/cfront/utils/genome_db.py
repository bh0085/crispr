'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job, JobERR, Spacer, Hit
import numpy as np
from numpy import *
import genome_io as gio
import random
import itertools as it
from cfront import cfront_settings

def compute_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    #error checking... this should never occur
    if spacer.computing_hits:
        raise Exception("already computing hits")
    spacer.computing_hits = True
    
    #query file IO
    jp = job.path
    query_file = os.path.join(jp,"query_s{0}.txt".format(spacer_id))
    with open(query_file,'w') as qf:qf.write(spacer.guide)

    jobpath = cfront_settings["jobs_directory"]
    cmd = "bowtie.py -q {0} -j {1} -s {2} -p {3}".format(spacer.guide,job.id,spacer_id, jobpath)
    prc = spc.Popen(cmd, shell=True)
    return False


def check_hits(spacer_id):
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job
    
    #filesystem checks for completion
    p = job.path
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
    p = os.path.join(job.path,"matches_s{0}.txt".format(spacer_id))
    cols = ["spacer_id", "sequence", "chr", "start", "strand","nrg"]    
    
    with open(p) as f: hits = [dict([[ cols[i], e] for i,e in enumerate(r.strip().split("\t"))]) for r in f]
    
    translation = {"A":0,"G":1, "T":2,"C":3}
    spacer_hits =dict([(k,list(g)) for k,g in  it.groupby(sorted(hits, key = lambda x:x["spacer_id"]), key = lambda x:int(x["spacer_id"]))])

    if not spacer_id in spacer_hits: 
        raise JobERR(Job.ERR_MISSING, job)
    if len(spacer_hits) != 1: 
        raise JobERR(Job.ERR_TOOMANY, job)

    #processes hits by spacer
    for spacer_id, hits_rows in spacer_hits.items():
        hits_array = np.array([[translation.get(let,4) 
                                for let in e["sequence"]] for e in hits_rows])
        spacer = Session.query(Spacer).get(spacer_id)

        #error checking... does a spacer already have a score?
        if spacer.computed_hits:
            raise JobERR(Job.ERR_ALREADYCOMPUTED, job)
            return

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
            ontarget = False

            if len(mismatches) > 5:
                continue
            if len(mismatches) == 0:
                if hit["start"] != spacer.chr_start :
                    print "ontarget at nonmatching locus {0} / {1}".format(hit["start"],spacer.chr_start)
                    raise JobERR(Job.ERR_MULTIPLE_ONTARGETS, job)
                    return
                else:
                    score = 100
                    ontarget = True
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
                        score = score,
                            ontarget = ontarget
                    ))

        Session.flush()

        updates = ",".join( ["({0},'{1}',{2})".format(h.id,h.chr,h.start) 
                                for h in spacer.hits]
                        )
        print updates
        for h in spacer.hits:
            if h.id == None:
                print h.toJSON()
                raise Exception()

        print "HIT? {0}".format(spacer.hits[0].id)
        import psycopg2

        conn = psycopg2.connect("dbname=vineeta user=ben password=random12345")
        cur = conn.cursor()
        cmd = """
CREATE TEMP TABLE {0} (
        id int
        , chr text
        , start int);
INSERT INTO {0} VALUES
        {2};
SELECT 
        {0}.id as exon_id, 
        {1}.gene_name as gene_name
FROM {0}, exon_hg19
        WHERE {1}.chr = {0}.chr
        AND ({0}.start+20) > ({1}.exon_start -100)
        AND ({0}.start) < ({1}.exon_end +100)
        """\
                    .format("hits_{0}".format(spacer.id),
                            "exon_hg19",
                            updates
                            )
        cur.execute(cmd)
        results = cur.fetchall()
        conn.close()
        for r in results:
            Session.query(Hit).get(r[0]).gene = r[1]

        ot_sum = sum(h.score for h in spacer.hits if not h.ontarget)
        spacer.score =100 / (100 + sum(h.score for h in spacer.hits if not h.ontarget))
        spacer.n_offtargets = len(spacer.hits) -1
        spacer.n_genic_offtargets = len([h for h in spacer.hits if h.gene is not None])
        print "spacer: {1}(J{0}) -- {2}  N_OTS: {3}, TOTSCORE {4}".format(spacer.jobid, spacer.id, spacer.score, len(spacer.hits) - 1, ot_sum)

    return True



