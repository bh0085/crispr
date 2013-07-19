#!/usr/bin/env python
''' tools that interact with the file io for genome dbv''' 
import os, sys, subprocess as spc
from cfront.models import Session, Job, Spacer, Hit
from sqlalchemy import desc

CDHOME=os.environ["CDHOME"]
CDSCRIPTS=os.path.join(CDHOME,"scripts")
CDREF=os.path.join(CDHOME,"reference")
v = True

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
    if v: print "cmmencing file io"
    delete_file_names = range(4,10)
    job = Session.query(Job).get(job_id)
    jp = get_job_path(job_id)
    
    write_f1(job_id)
    write_f2(job_id)
    write_f3(job_id)
    write_f4(job_id)
    write_f5_f6(job_id)
    write_f7(job_id)
    write_f8(job_id)
    write_f9(job_id)    

def write_f1(job_id):
    '''writes a file formatted:
(F1). Spacers, eg:
spacer1 AATATAACCTGCCGCTTTGC AGG +
spacer2 CTTTGCAGGTGTATTCCACG TGG +
spacer3 ATGGTCGCTACAGCATCTCT CGG +
'''
    
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    if not job.computed_spacers: raise Exception(Job.NOSPACERS)

    fpath = os.path.join(jp,"f1.txt")
    if os.path.isfile(fpath):
        os.remove(fpath)

    if v: print "writing f1 at {0}".format(fpath)
    with open(fpath, 'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      s.guide, 
                                      s.nrg, 
                                      "+" if s.strand ==1 else "-"])
                           for s in job.spacers ]))
    if v: print "DONE"
    if v: print

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

    fpath = os.path.join(jp,"f2.txt")
    if os.path.isfile(fpath):
        os.remove(fpath)

    if v: print "writing f2 at {0}".format(fpath)
    with open(fpath,'w') as f:
        f.write("\n".join(["\t".join([str(s.id),
                                      h.chr, 
                                      str(h.start), 
                                      "+" if h.strand ==1 else "-",
                                      h.sequence])
                           for s in job.spacers for h in s.hits ]))
    if v: print "done"
    if v: print

def write_f3(job_id):
    jp = get_job_path(job_id)
    f1p = os.path.join(jp,"f1.txt")
    f2p = os.path.join(jp,"f2.txt")
    f3p = os.path.join(jp,"f3.txt")

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
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    f3p = os.path.join(jp,"f3.txt")
    f4p = os.path.join(jp,"f4.txt")
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
        for spacer in job.spacers:
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
               gene = "NA"
               row = " ".join("{0}".format(e) for e in [spacerid, ontarget, hitid, chr, pos, strand, sequence, mismatch,
                                mismatch_pos, score, gene])
               f.write(row+"\n")
    if v: print "DONE"
    if v: print 
            
def write_f5_f6(job_id):
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    f4p = os.path.join(jp,"f4.txt")
    f5p = os.path.join(jp,"f5.pdf")
    f6p = os.path.join(jp,"f6.csv")
    gene= os.path.join(job.name)
    
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

def write_f7(job_id):
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    f6p = os.path.join(jp,"f6.csv")
    f7p = os.path.join(jp,"f7.in")

    cmd = ("perl {0}/scripts/make_primer3_offtarget_input.pl {1} "+\
           "{0}/reference/human_g1k_v37.fasta {2}").format(CDHOME, f6p, f7p)

    if v: print "running cmd:"
    if v: print "  {0}".format(cmd)

        
    prc = spc.Popen(cmd,shell=True)
    out = prc.communicate()
    
    if v:print "wrote output at: {0}".format(f7p)
    if v:print "DONE"
    if v:print

def write_f8(job_id):
    #runs primer3
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    f7p = os.path.join(jp,"f7.in")
    f8p = os.path.join(jp,"f8.out")
    
    cmd="primer3_core -p3_settings_file={0}/primer3/primer3-2.3.5/primer3web_v4_0_0_default_settings.txt -output={1} {2}".format(CDHOME,f8p,f7p)
    
    if v: print "running command: {0}".format(cmd)
    if v: print "writing: {0}".format(f8p)
    prc = spc.Popen(cmd, shell=True)
    out = prc.communicate()
    
    if v: print "DONE"
    if v: print

def write_f9(job_id):
    #runs primer3
    jp = get_job_path(job_id)
    job = Session.query(Job).get(job_id)
    f6p = os.path.join(jp,"f6.csv")
    f8p = os.path.join(jp,"f8.out")
    f9p = os.path.join(jp,"f9.csv")

    cmd = "perl {0}/parse_primer3_output.pl {1} {2} {3}".format(CDSCRIPTS, f8p, f6p,f9p)

    if v: print "running command: {0}".format(cmd)
    if v: print "writing: {0}".format(f9p)
    prc = spc.Popen(cmd, shell=True)
    out = prc.communicate()
    
    if v: print "DONE"
    if v: print

import transaction
from pyramid.paster import bootstrap
if __name__ == "__main__":
    env = bootstrap(sys.argv[1])
    with transaction.manager:
        j = Session.query(Job).order_by(desc(Job.id)).first()
        #for j in alljobs:
        if needs_file_io(j.id):
            print j.id
            print j.computed_spacers
            print "performing file IO sequence on job id: {0}".format(j.id)
            commence_file_io(j.id)
            #break
