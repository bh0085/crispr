#!/usr/bin/env python

from cfront.utils import genome_db, webserver_db, genome_io
from cfront.models import Session, SpacerERR, JobERR, Job, Spacer, Hit
import sys, shutil
import time
import transaction
from pyramid.paster import bootstrap
from cfront import cfront_settings
import argparse, os


def init_env(p):
    env = bootstrap(p)

def queue_loop(ofs,stride):
    while True:
        process_queue(ofs,stride)
        time.sleep(1)
        
def process_queue(ofs, stride):
    #start a transaction to compute spacers for any jobs which lack them
    #NOTE this is the second place in our code where spacers can be created
    # this should be fixed as we don't do the same checks here that we do in
    # the first -- at views_ajax/post_new.
    #
    #here we protect against the case where no spacers pass but don't do
    # any checking of the input query.

    possible_spacer_jobs = Session.query(Job).filter(Job.computed_spacers == False).all()
    selected_jobs = [j for j in possible_spacer_jobs if j.id % stride == ofs and j.genome_name != "rn5"]

    for j in selected_jobs[:100]:
        with transaction.manager:
            try:
                print 'computing spacers {0}'.format(j.id)
                spacer_infos = webserver_db.compute_spacers(j.sequence)
                if(len(spacer_infos)) == 0:
                    raise JobERR(Job.NOSPACERS, j)
                for spacer_info in spacer_infos:
                    Session.add(Spacer(job = j,**spacer_info))
                j.computed_spacers = True
                Session.add(j)
            except JobERR, e:
                print "Excepted a job error during Spacer finding for Job: {0}".format(j.id)
                print j.sequence

    
    #starts a transaction to compute hits for any spacer which has not
    # "computed_hits" or "computing_hits"

    possible_hit_jobs =  Session.query(Job)\
                    .join(Spacer)\
                    .filter(Spacer.score == None)\
                    .filter(Job.failed == False)\
                     .all()
    selected_hit_jobs = [j for j in possible_hit_jobs if j.id % stride == ofs and j.genome_name != "rn5"]


    if len(selected_hit_jobs) > 0:
        batched_jobs = [j for j in selected_hit_jobs if j.batch is not None]
        #sorts jobs to process recent submissions and non-batch jobs first
        def priority(j):
            return -1 * j.id
            #if j.batch is not None: return 100
            #else: return -1* j.id 
            
        
        top_job = sorted(selected_hit_jobs, key = priority)[0]
        if not top_job in Session: top_job = Session.merge(j)
        #spacers may be deleted from the session in the interior of this loop
        for i,s in enumerate([s for s in top_job.spacers if s.score is None][:2]):
            print "batched? {0}".format(j.batch)
            if not s in Session: s = Session.merge(s)
            with transaction.manager:
                    try:
                        print "Computing hits for spacer: {0} (Job {1})".format(s.id, j.id)
                        genome_db.compute_hits_for_spacer(s.id)
                    except JobERR, e:
                        print "excepted a job/spacer error on COMPUTE for job {0}".format(s.job.id, top_job)
                    except SpacerERR, e:
                        print "excepted a spacer error for spacer id {0}".format(s.id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset','-r',dest="reset",
                        default=False, const = True , action="store_const",
                        help = "Reset all jobs (deletes /jobs/*)")
    parser.add_argument('--jobstride',dest="jobstride",
                        default=1,type=int,
                        help="stride of the multithreaded job handler")
    parser.add_argument('--jobofs',dest="joboffset",
                        default=0,type=int,
                        help="offset of this process in the case where stride is >1")

    parser.add_argument('inifile')
    args = parser.parse_args()

    init_env(args.inifile)
    
    print cfront_settings
    queue_loop(args.joboffset, args.jobstride)


if __name__ == "__main__":
    main()
