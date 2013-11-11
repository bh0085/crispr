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
    
    if  len(job.good_spacers) == 0 or job.genome_name != 'hg19':
        job.files_failed = True
        job.date_failed = datetime.datetime.utcnow()
        return 

    write_f4(job_id)
    write_f5_f6(job_id)
    
    if len([f for f in job.files if f["ready"] == False]) == 0:
        job.files_ready = True
        job.date_completed = datetime.datetime.utcnow()
    else:
        job.files_failed = True

    
    try:
        if job.email_complete:
            if (not cfront_settings.get("debug_mode",False)) and cfront_settings.get("mails_on_completion",False):
                mail.mail_completed_job(None, job)
    except mail.MailError as m:
        print "writing mail on complete failed for job {0}".format(job.id)
        


def write_f4(job_id):
    job = Session.query(Job).get(job_id)
    f4p = job.f4
    if os.path.isfile(f4p):
        os.remove(f4p)
    
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
                   .join(Spacer)\
                   .group_by(Job.id)\
                   .having(func.sum(case([(Spacer.score == None,1)], else_=0)) == 0)\
                   .order_by(Job.id.desc()).first()
        if j:
            with transaction.manager:
                commence_file_io(j.id)
        time.sleep(2)
