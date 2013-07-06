''' tools that interact with the file io for genome dbv''' 
import os
from cfront.models import Session, Job, Spacer, Hit

def get_job_path(job_id):
    path =   os.path.join(os.environ["CFRONTDATA"],"jobs/{0}").format(job_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def write_f1(job_id):
    '''writes a file formatted:
(F1). Spacers, eg:
spacer1 AATATAACCTGCCGCTTTGC AGG +
spacer2 CTTTGCAGGTGTATTCCACG TGG +
spacer3 ATGGTCGCTACAGCATCTCT CGG +
'''
    jp = get_job_path(job_id)
    job = Session.query(job).get(job_id)
    if not job.computed_hits: raise Exception(Job.NOSPACERS)
    with open(os.path.join(fp,"f1.txt"), 'w') as f:
        f.write("\n".join(["\t".join([s.id,
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
    job = Session.query(job).get(job_id)
    if not job.computed_hits: raise Exception(Job.NOHITS)
    with open(os.path.join(fp,"f2.txt"),'w') as f:
        f.write("\n".join(["\t".join([s.id,
                                      h.chr, 
                                      h.start, 
                                      "+" if h.strand ==1 else "-",
                                      h.sequence])
                           for s in job.spacers for h in s.hits ]))
