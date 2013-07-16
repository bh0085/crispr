'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os
from ..models import Session, Job, Spacer, Hit
import numpy as np
import genome_io as gio
import random



def compute_hits(spacer_id):
    '''
    computes off and on-target hits for all guide sequences of JOB
    '''
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job

    if spacer.computing_hits:
        raise Exception("already computing hits")
    spacer.computing_hits = True
    table_prefix = "loci1mt"

    jp = gio.get_job_path(job.id)
    query_file = os.path.join(jp,"query_s{0}.txt".format(spacer_id))
    with open(query_file,'w') as qf:
        qf.write(spacer.guide)
        
    cmd = "bowtie.py -q {0} -j {1} -s {2}".format(spacer.guide,job.id,spacer_id)
    #cmd =  "submit_query.py -l .4 -t {3} -q {0} -j {1} -s {2}".format( query_file, job.id, spacer_id, table_prefix)
    prc = spc.Popen(cmd, shell=True)
    return False





def check_hits(spacer_id):
    '''
    checks files in the job path to determine whether a query is completed
    '''
    spacer = Session.query(Spacer).get(spacer_id)
    job = spacer.job
    p = gio.get_job_path(job.id)
    done = "matches_s{0}.txt".format(spacer_id) in os.listdir(p)
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
    cols = ["sequence", "chr", "start", "strand","nrg"]    

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
        sims_array = np.sum(np.equal(all_spacers[np.newaxis,:] - all_hits[:,:], 0),1)
        
        #generates a similarity matrix of spacers, hits
        accepted_hits = np.nonzero(np.greater_equal(sims_array,min_matches))[0]
        for idx_h in accepted_hits:
           hit = hits[idx_h]
           is_ontarget =  True if hit_length ==  sims_array[idx_h] else False


           

           Session.add(Hit(spacer = spacer,
                           chr = hit["chr"],
                           sequence = hit["sequence"] + hit["nrg"],
                           similarity = float(sims_array[idx_h]) / hit_length,
                           start = hit["start"],
                           strand = 1 if hit["strand"] == "+" else -1,
                           ontarget = is_ontarget
                       ))
           
    if(len(spacer.hits) > 0):
        spacer.score = min([1,  (1 - max([h.similarity for h in spacer.hits if not h.ontarget]+[0])) *4  ])
    else:
        spacer_score = 1

 


    spacer.computed_hits = True
    return True


#SCORING FUNCTION >>>
'''
        weights = (0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583);
	if ($num_mismatch > 5) {
		next;
	}               
                
	if ($num_mismatch == 1) {
		$score = 100*(1-$weights[$mismatch_positions-1]);
	}
                
	if ($num_mismatch > 1) {
                        @values = split(':',$mismatch_positions);
                        $score = $score * (1-$weights[$values[0]-1]);
                        for ($k = 1; $k < scalar(@values); $k++) {
                                $mean_pairwise = $mean_pairwise + ($values[$k] - $values[$k-1]);
                                $score = $score * (1-$weights[$values[$k]-1]);
                        }
                        $mean_pairwise = $mean_pairwise / (scalar(@values) - 1);
                        $score = $score / ( ((19-$mean_pairwise)/19)*4 + 1);
			$score = $score / ($num_mismatch*$num_mismatch);
                                
                        if ($score < 0) {
                                $score = 1;
                        }
	}
	

        '''
