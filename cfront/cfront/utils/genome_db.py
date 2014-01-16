'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os, re
from ..models import Session, Job, SpacerERR, JobERR, Spacer, Hit
import numpy as np
from numpy import *
import genome_io as gio
import random, datetime
import itertools as it
from cfront import cfront_settings

from Bio import SeqRecord as sr, Seq as seq
import transaction
import exons
import webserver_db
import byte_scanner

weights =  array([0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]);
TMPPATH = "/tmp/ramdisk/cfront/genomedb"
if not os.path.isdir(TMPPATH):
    os.makedirs(TMPPATH)

def scoring_fun(mismatches):
    if len(mismatches) == 0:
        score = 100
    else:
        score = 100 * (1 - weights[mismatches]).prod()
        if len(mismatches) > 1:
            mean_pairwise =float(sum(mismatches[1:] - mismatches[:-1])) / (len(mismatches)-1)
            mpw_factor = ((float((19-mean_pairwise))/19)*4 + 1)
            scl_factor = pow(len(mismatches),2)

            score  = score / ( mpw_factor * scl_factor )
            score = max([score,0])
    return score


#
# test_for_ontargets(spacer_id)
# fetch_hits_in_thread()
# process_hits_for_spacer
def test_for_ontargets(spacer_id):
        spacer = Session.query(Spacer).get(spacer_id)
        #FILTER SPACERS
        #check to make sure that spacers do not have huge number of perfect matches
        exact_matches = webserver_db.check_genome(spacer.sequence,spacer.job.genome_name)
        if len(exact_matches) > 5:
            raise SpacerERR(Spacer.ERR_MANY_EXACT_MATCHES,spacer)    

import json
def fetch_hits_in_thread_shm(guide_sequence,genome_name,shm_genome_array):
    rval = None
    try:
        #BYTE SCAN FOR HITS
        hits = byte_scanner.run_sequence_vs_genome_shm(guide_sequence, genome_name, shm_genome_array)
        if len(hits) == 0:
            rval = (False, "no_hits")
        rval =  (True, hits[:10])
    except byte_scanner.TooManyHits, e:
        rval =  (False, "too_many_hits")
    except Exception, e:
        rval =  (False, "failed")
    
    return rval

def process_hits_for_spacer(spacer_id, hits):
    with transaction.manager:
        v = True
        spacer = Session.query(Spacer).get(spacer_id)

        translation = {"A":0,"G":1, "T":2,"C":3}
        #LIST MISMATCHES
        hits_array = np.array([[translation.get(let,4) 
                                    for let in e["sequence"]] for e in hits])

        spacer = Session.query(Spacer).get(spacer_id)
        spacer_array = np.array([translation.get(let,4) for let in spacer.guide])

        nz = array(nonzero(not_equal(spacer_array[newaxis,:],hits_array))).transpose()
        mismatches_by_hit = dict([(k,array([e[1] for e in g])) 
                                      for k,g in \
                                      it.groupby(nz,key = lambda x:x[0])])
        scores = [scoring_fun( mismatches_by_hit.get(i,array([])) )
                  for i in range(len(hits))]

        if len(scores) > 500:
            if v: print "many hits; taking top 1000"
        hits_taken_idxs = np.argsort(scores)[::-1][:501]

        #CREATE HITS
        found_ontarget = False
        for idx in hits_taken_idxs:
            hit = hits[idx]
            mismatches = mismatches_by_hit.get(idx,array([]))
            score = scores[idx]

            if int(hit["start"]) == int(spacer.chr_start) :
                    ontarget = True 
                    found_ontarget = True
            else: ontarget = False
            
            Session.add(Hit(spacer = spacer,
                            chr = hit["chr"],
                            sequence = hit["sequence"] +hit["nrg"],
                            n_mismatches = len(mismatches),
                            start = hit["start"],
                            strand = 1 if hit["strand"] in ["+",1] else -1,
                            score = score,
                            ontarget = ontarget
                        ))

        if v: print "created {0} hits for spacer {1}".format(len(hits_taken_idxs),spacer.id)
        Session.flush()

        #SET ONTARGET
        #if no ontarget position was explicitly set for the spacer,
        #guess one if only one hit is perfect.
        if not found_ontarget:
                possible = [h for h in spacer.hits if h.n_mismatches == 0]
                if len(possible) == 1:
                    possible[0].ontarget = True
                    found_ontarget = True
                    Session.add(possible[0])

        if found_ontarget and v: print "found offtarget for spacer {0}".format(spacer.id)
        if v: print "finding exons for spacer {0}".format(spacer.id)
        
        time = datetime.datetime.utcnow()
        #FIND EXONS
        if len(spacer.hits) > 0:
            genes_by_hitid = exons.get_hit_genes(spacer.hits, spacer.job.genome_name)
            for h in spacer.hits:
                h.gene = genes_by_hitid.get(h.id)
                Session.add(h)

        delta = datetime.datetime.utcnow() - time
        if v: print "found exons, took {0}".format(delta)
                    

        #SPACER AGGREGATE CHARACTERISTICS
        ot_sum = sum(h.score for h in spacer.hits if not h.ontarget)
        spacer.score =100 / (100 + sum(h.score for h in spacer.hits if not h.ontarget))
        spacer.n_offtargets = len([ h for h in spacer.hits if not h.ontarget])
        spacer.n_genic_offtargets = len([h for h in spacer.hits if h.gene is not None])
        Session.add(spacer)
        print "done with spacer: {1} from (J{0}) -- {2} score is {4} with {3} offtargets.".format(spacer.jobid, spacer.id, spacer.score, len(spacer.hits) - 1, ot_sum)
