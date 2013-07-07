#!/usr/bin/env python
''' tools that interact with the file io for genome dbv''' 
import os, sys, subprocess as spc
from cfront.models import Session, Job, Spacer, Hit
from sqlalchemy import desc

CDHOME=os.environ["CDHOME"]
CDSCRIPTS=os.path.join(CDHOME,"scripts")
CDREF=os.path.join(CDHOME,"reference")

def get_job_path(job_id):
    path =   os.path.join(os.environ["CFRONTDATA"],"jobs/{0}").format(job_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def needs_file_io(job_id):
    file_names = range(1,10)
    job = Session.query(Job).get(job_id)
    jp = get_job_path(job_id)
    for f in file_names:
        file_abspath = os.path.join(jp,"f{0}.txt".format(f))
        if not os.path.isfile(file_abspath):
            return True

    return False
            

def commence_file_io(job_id):
    file_names = range(1,10)
    job = Session.query(Job).get(job_id)
    jp = get_job_path(job_id)
    for f in file_names:
        file_abspath = os.path.join(jp,"f{0}.txt".format(f))
        if os.path.isfile(file_abspath):
            print "deleting file: {0}".format(file_abspath)

    write_f1(job_id)
    write_f2(job_id)
    write_f3(job_id)
    #write_f4(job_id)
    #write_f5(job_id)
    #write_f6(job_id)
    #write_f7(job_id)
    #write_f8(job_id)
    #write_f9(job_id)    

def write_f1(job_id):
    '''writes a file formatted:
(F1). Spacers, eg:
spacer1 AATATAACCTGCCGCTTTGC AGG +
spacer2 CTTTGCAGGTGTATTCCACG TGG +
spacer3 ATGGTCGCTACAGCATCTCT CGG +
'''
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    if not job.computed_hits: raise Exception(Job.NOSPACERS)
    with open(os.path.join(jp,"f1.txt"), 'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      s.guide, 
                                      s.nrg, 
                                      "+" if s.strand ==1 else "-"])
                           for s in job.spacers ]))

def write_f2(job_id):
    '''writes a file formatted:
(F2). Offtargets, eg:
spacer33        1       13020   -       TTCTCCACCAGAGCCTTTCTTGG
spacer3 1       40914   +       ATTTTCTCTACAGCAATTCTAGG
spacer9 1       62767   -       ATGGACAAAGCTGTGCTCAGAGG
'''
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    if not job.computed_hits: raise Exception(Job.NOHITS)
    with open(os.path.join(jp,"f2.txt"),'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      h.chr, 
                                      str(h.start), 
                                      "+" if h.strand ==1 else "-",
                                      h.sequence])
                           for s in job.spacers for h in s.hits ]))
def write_f3(job_id):
    jp = get_job_path(job_id)
    f1p = os.path.join(jp,"f1.txt")
    f2p = os.path.join(jp,"f2.txt")
    f3p = os.path.join(jp,"f3.txt")

    cmd = "perl {0}/annotate_offtarget_sites.pl {1} {2} {3}/RefSeq_hg19.txt {4}".\
          format(CDSCRIPTS,f1p,f2p,CDREF,f3p)
    prc = spc.Popen(cmd, shell=True)
    prc.communicate()
    print f3p
    return f3p

def write_f4(job_id):
    raise Exception("not implemented")
def write_f5(job_id):
    raise Exception("not implemented")
def write_f6(job_id):
    raise Exception("not implemented")
def write_f7(job_id):
    raise Exception("not implemented")
def write_f8(job_id):
    raise Exception("not implemented")
def write_f9(job_id):
    raise Exception("not implemented")


import transaction
from pyramid.paster import bootstrap
if __name__ == "__main__":
    env = bootstrap(sys.argv[1])
    with transaction.manager:
        j = Session.query(Job).order_by(desc(Job.id)).first()
        #for j in alljobs:
        if needs_file_io(j.id):
                print "performing file IO sequence on job id: {0}".format(j.id)
                commence_file_io(j.id)
                #break
