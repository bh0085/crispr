#!/usr/bin/env python
''' tools that interact with the file io for genome dbv''' 
import os, sys, subprocess as spc, time
from cfront.models import Session, Job, Spacer, Hit
from sqlalchemy import desc, func
from sqlalchemy.sql.expression import case
from cfront.utils import mail
from cfront import cfront_settings
import re, datetime

CDHOME="/home/ben/v_crispr_design"
CDSCRIPTS=os.path.join(CDHOME,"scripts")
CDREF=os.path.join(CDHOME,"reference")
v = True


def commence_file_io(job_id):

    print "DEBUG?? ", "{0}".format( cfront_settings.get("debug_mode",False))

    if v: print "commencing file io"

    job = Session.query(Job).get(job_id)    
    Session.add(job)
    
    if job.genome_name != "HUMAN" or len(job.good_spacers) == 0:
        job.files_failed = True
        job.date_failed = datetime.datetime.utcnow()
    else:
        job.files_computing = True

    write_f1(job_id)
    write_f2(job_id)
    write_f4(job_id)
    write_f5_f6(job_id)
    
    if len([f for f in job.files if f["ready"] == False]) == 0:
        job.files_ready = True
        job.date_completed = datetime.datetime.utcnow()
    else:
        job.files_failed = True
    job.files_computing = False

    #if job.email_complete:
    #    if not cfront_settings.get("debug_mode",False):
    #        mail.mail_completed_job(None, job)





def write_f1(job_id):
    '''writes a file formatted:
(F1). Spacers, eg:
spacer1 AATATAACCTGCCGCTTTGC AGG +
spacer2 CTTTGCAGGTGTATTCCACG TGG +
spacer3 ATGGTCGCTACAGCATCTCT CGG +
'''
    
    job = Session.query(Job).get(job_id)
    if not job.computed_spacers: raise Exception(Job.NOSPACERS)

    fpath = job.f1

    if os.path.isfile(fpath):
        os.remove(fpath)

    if v: print "writing f1 at {0}".format(fpath)
    with open(fpath, 'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      s.guide, 
                                      s.nrg, 
                                      "+" if s.strand ==1 else "-"])
                           for s in job.good_spacers ]))
    if v: print "DONE"
    if v: print

def write_f2(job_id):
    '''writes a file formatted:
(F2). Offtargets, eg:
spacer33        1       13020   -       TTCTCCACCAGAGCCTTTCTTGG
spacer3 1       40914   +       ATTTTCTCTACAGCAATTCTAGG
spacer9 1       62767   -       ATGGACAAAGCTGTGCTCAGAGG
'''
    job = Session.query(Job).get(job_id)
    if not job.computed_hits: raise Exception(Job.NOHITS)
    fpath = job.f2
    
    if os.path.isfile(fpath):
        os.remove(fpath)

    if v: print "writing f2 at {0}".format(fpath)
    with open(fpath,'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      h.chr, 
                                      str(h.start), 
                                      "+" if h.strand ==1 else "-",
                                      h.sequence])
                           for s in job.good_spacers for h in s.hits ]))
    if v: print "done"
    if v: print

def write_f3(job_id):
    job = Session.query(Job).get(job_id)
    f1p = job.f1;
    f2p = job.f2; 
    f3p = job.f3; 

    if os.path.isfile(f3p):
        os.remove(f3p)
    
    cmd = "perl {0}/annotate_offtarget_sites.pl {1} {2} {3}/RefSeq_hg19.txt {4}".\
          format(CDSCRIPTS,f1p,f2p,CDREF,f3p)
    
    if v: print "running {0} to ".format(cmd)
    if v: print "writing f3 at {0}".format(f3p)
    
    prc = spc.Popen(cmd, shell=True)
    prc.communicate()
    if v: print "done"

    return f3p

def write_f4(job_id):
    job = Session.query(Job).get(job_id)
    f3p = job.f3
    f4p = job.f4
    if os.path.isfile(f4p):
        os.remove(f4p)
    
    #cmd = "R -f ${HOME}/scripts/classify_on_off_targets.R --slave --vanilla --args {0} ${CHR} {1}".format(f3p, f4p)
    #this command outputs:
    '''SPACER ON_TARGET ID CHR POS STRAND SEQUENCE MISMATCH MISMATCH_POS SCORE GENE
spacer1 1 spacer1 18 44589693 + GAACAGTGAGATGCGAGAATTGG 0 NA 100 KATNAL2'''
    # we do that by hand
    
    if v: print "writing f4 at {0}".format(f4p)

    with open(f4p,"w") as f:
        f.write(" ".join(["SPACER","ON_TARGET", "ID", "CHR", "POS", "STRAND", "SEQUENCE", "MISMATCH", "MISMATCH_POS", "SCORE", "GENE"])+"\n")
        for spacer in job.good_spacers:
           ot_count=1
           for hit in sorted(spacer.hits, key=lambda x:-1* x.score):
               spacerid = "spacer_{0}".format(spacer.id)
               ontarget = 1 if hit.ontarget else 0
               if ontarget: 
                   hitid = "{0}".format(spacerid)
               else: 
                   hitid = "{0}_off_{1}".format(spacerid, ot_count) 
                   ot_count+=1
               chr=hit.chr[3:]
               pos=hit.start
               strand="+" if hit.strand == 1 else "-"
               sequence=hit.sequence
               mismatch=hit.n_mismatches
               
               mismatch_pos= "NA" if mismatch == 0 \
                             else ":".join( ["{0}".format(i) for i in range(20) 
                                             if spacer.sequence[i] != hit.sequence[i]])
               score = "{0:.1f}".format(hit.score)
               gene = hit.gene
               row = " ".join("{0}".format(e) for e in [spacerid, ontarget, hitid, chr, pos, strand, sequence, mismatch,
                                mismatch_pos, score, gene])
               f.write(row+"\n")
    if v: print "DONE"
    if v: print 
            
def write_f5_f6(job_id):
    job = Session.query(Job).get(job_id)
    f4p = job.f4
    f5p = job.f5
    f6p = job.f6
    gene= os.path.join(job.safe_name)
    
    if os.path.isfile(f5p):
        os.remove(f5p)    
    if os.path.isfile(f6p):
        os.remove(f6p)

    if v: print "writing f5 at {0}".format(f5p)
    if v: print "writing f6 at {0}".format(f6p)

    cmd = ("R -f "+\
           "{0}/make_graphical_output.R --slave --vanilla --args "+\
           "{1} {2} {3} {4}")\
        .format(CDSCRIPTS,f4p,f5p,gene,f6p)

    if v: print "running cmd:"
    if v: print "  {0}".format(cmd)
    prc = spc.Popen(cmd, shell=True)
    out = prc.communicate()
    print "outval: {0}".format(out)

    if v: print "DONE"
    if v: print


import transaction
from pyramid.paster import bootstrap
if __name__ == "__main__":
    env = bootstrap(sys.argv[1])
    while 1:
        j = Session.query(Job)\
                   .filter(Job.files_failed == False)\
                   .filter(Job.files_ready == False)\
                   .filter(Job.files_computing == False)\
                   .join(Spacer)\
                   .group_by(Job.id)\
                   .having(func.sum(case([(Spacer.score == None,1)], else_=0)) == 0)\
                   .order_by(Job.id.desc()).first()
        if j:
            with transaction.manager:
                commence_file_io(j.id)

        time.sleep(2)
