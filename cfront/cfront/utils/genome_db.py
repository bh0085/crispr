'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os, re
from ..models import Session, Job, JobERR, Spacer, Hit
import numpy as np
from numpy import *
import genome_io as gio
import random
import itertools as it
from cfront import cfront_settings
import bowtie

from Bio import SeqRecord as sr, Seq as seq
import transaction
import exons

weights =  array([0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]);
TMPPATH = "/tmp/ramdisk/cfront/genomedb"
if not os.path.isdir(TMPPATH):
    os.makedirs(TMPPATH)

#runs a blat query (gfClient) to check for unique matches to a spacer.
def check_genome(spacer):
    sequence = spacer.sequence
    record = sr.SeqRecord(seq.Seq(sequence),id="seqA",description="")
    tmpfile_in = os.path.join(TMPPATH,"tmpfile_{0}.fa".format(int(random.random() * 1e10)))
    tmpfile_out = os.path.join(TMPPATH,"tmpfile_{0}.psl".format(int(random.random() * 1e10)))
    with open(tmpfile_in,'w') as f:
        f.write(record.format("fasta"))

    #uses the long wordsize index to find exact matches in the genome.
    #more than one will generate an error
    cmd = "gfClient localhost 8000 /data/genomes/ {0} {1} -minScore={2} -minIdentity=100".format(tmpfile_in, tmpfile_out, len(sequence))
    
    prc = spc.Popen(cmd,shell = True, stdout = spc.PIPE)
    prc.communicate()
    with open(tmpfile_out) as f:
        content = f.read()
        
    os.remove(tmpfile_in)
    os.remove(tmpfile_out)
    
    lines = content.splitlines()
    headers, content = lines[:5],lines[5:]
    

    cols = ['matches',
            'misMatches',
            'repMatches',
            'nCount',
            'qNumInsert',
            'qBaseInsert',
            'tNumInsert',
            'tBaseInsert',
            'strand',
            'qName',
            'qSize',
            'qStart',
            'qEnd',
            'tName',
            'tSize',
            'tStart',
            'tEnd',
            'blockCount',
            'blockSizes',
            'qStarts',
            'tStarts']

    if len(content) == 0:
        return []


    matches = []
    for l in content:
        possible = dict([(cols[i],e.strip()) for i,e in enumerate(re.compile("\s+").split(l))])
        eligible = True if int(possible["misMatches"]) == 0 else False
        if eligible:
            matches.append(possible)
        
    return matches




def compute_hits_for_spacer(spacer_id):
        spacer = Session.query(Spacer).get(spacer_id)

        #FILTER SPACERS
        #check to make sure that spacers do not have huge number of perfect matches
        exact_matches = check_genome(spacer)
        if len(exact_matches) > 5:
            raise SpacerERR(Spacer.ERR_MANY_EXACT_MATCHES,spacer)

        #BYTE SCAN FOR HITS
        hits = byte_scanner.run_sequence_vs_genome(spacer.sequence, spacer.job.genome_name)
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
         
        #CREATE HITS
        found_ontarget = False
        for idx,h in enumerate(hits_array):
            hit = hits[idx]
            mismatches = mismatches_by_hit.get(idx,array([]))
            ontarget = False
    

            #COMPUTE SCORE
            if len(mismatches) > 5:
                continue
            if len(mismatches) == 0:
                score = 100
                if int(hit["position"]) == int(spacer.chr_start) :
                    ontarget = True
                    found_ontarget = True
            else:
                score = 100 * (1 - weights[mismatches]).prod()
                if len(mismatches) > 1:
                    mean_pairwise =float(sum(mismatches[1:] - mismatches[:-1])) / (len(mismatches)-1)
                    mpw_factor = ((float((19-mean_pairwise))/19)*4 + 1)
                    scl_factor = pow(len(mismatches),2)

                    score  = score / ( mpw_factor * scl_factor )
                    score = max([score,0])
                        
            Session.add(Hit(spacer = spacer,
                            chr = hit["chr"],
                            sequence = hit["sequence"] +hit["nrg"],
                            n_mismatches = len(mismatches),
                            start = hit["position"],
                            strand = 1 if hit["strand"] == "+" else -1,
                            score = score,
                            ontarget = ontarget
                        ))
                
        Session.flush()

        #SET ONTARGET
        #if no ontarget position was explicitly set for the spacer,
        #guess one if only one hit is perfect.
        if not found_ontarget:
                possible = [h for h in spacer.hits if h.score == 100]
                if len(possible) == 1:
                    possible[0].ontarget = True
                    found_ontarget = True
                    Session.add(possible[0])
    
        #FIND EXONS
        if len(spacer.hits) > 0:
            genes_by_hitid = exons.get_hit_genes(spacer.hit, spacer.job.genome_name)
            for h in spacer.hits:
                h.gene = genes_by_hitid.get(h.id)
                Session.add(h)
                    
        #SPACER AGGREGATE CHARACTERISTICS
        ot_sum = sum(h.score for h in spacer.hits if not h.ontarget)
        spacer.score =100 / (100 + sum(h.score for h in spacer.hits if not h.ontarget))
        spacer.n_offtargets = len([ h for h in spacer.hits if not h.ontarget])
        spacer.n_genic_offtargets = len([h for h in spacer.hits if h.gene is not None])
        Session.add(spacer)
        print "spacer: {1}(J{0}) -- {2}  N_OTS: {3}, TOTSCORE {4}".format(spacer.jobid, spacer.id, spacer.score, len(spacer.hits) - 1, ot_sum)
    
