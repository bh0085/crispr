#!/usr/bin/env python

from cfront.utils import genome_db, webserver_db, genome_io
from cfront.models import Session, Job, Spacer, Hit
import sys, shutil
import time
import transaction
from pyramid.paster import bootstrap
from cfront.models import JobERR
from cfront import cfront_settings
import argparse, os


def init_env(p):
    env = bootstrap(p)

def queue_loop():
    while True:
        process_queue()
        time.sleep(1)
        


def process_queue():
    #start a transaction to compute spacers for any jobs which lack them
    #NOTE this is the second place in our code where spacers can be created
    # this should be fixed as we don't do the same checks here that we do in
    # the first -- at views_ajax/post_new.
    #
    #here we protect against the case where no spacers pass but don't do
    # any checking of the input query.


    for j in Session.query(Job).filter(Job.computed_spacers == False)\
                               .order_by(Job.id.desc()).limit(10).all():

        print "computing spacers for job {0}".format(j.id)
        with transaction.manager:
            
            try:
                print 'computing spacers {0}'.format(j.id)
                spacer_infos = webserver_db.compute_spacers(j.sequence)
                if(len(spacer_infos)) == 0:
                    raise JobERR(Job.ERR_NOSPACERS, j)
                for spacer_info in spacer_infos:
                    Session.add(Spacer(job = j,**spacer_info))
                j.computed_spacers = True
                Session.add(j)
            except JobERR, e:
                print "excepted a job error for job: {0}".format(j.id)

    
    #starts a transaction to compute hits for any spacer which has not
    # "computed_hits" or "computing_hits"
    for j in Session.query(Spacer)\
                    .filter(Spacer.computing_hits == False)\
                    .filter(Spacer.score == None)\
                    .join(Job)\
                    .filter(Job.failed == False)\
                    .order_by(Job.id.desc()).limit(3).all():

        print "computing hits for spacer {0}".format(s.id)
        with transaction.manager:
            try:
                if not s in Session: s = Session.merge(s)
                if s.job.failed: 
                    print "j failed, continuing"
                    continue
                    
                genome_db.compute_hits(s.id)
                s.computing_hits = True
                Session.add(s)
            except JobERR, e:
                print "excepted a job/spacer error on COMPUTE for job {0}".format(s.job.id)

    for s in Session.query(Spacer).join(Job)\
                             .filter(Spacer.score == None)\
                             .filter(Job.failed != True)\
                             .order_by(Job.id.desc()).limit(3).all():

        #opens up a transaction for each spacer.
        #genome_db will enter hits and modify s in the Session

        print "entering hits for spacer {0}".format(s.id)
        with transaction.manager:
            try:
            
                ready = genome_db.check_hits(s.id)
                if not ready:
                    continue
                if s not in Session: s = Session.merge(s)
                
                #check to see if another spacer computation has caused the job to fail...
                if s.job.failed:
                    print "marked job failed for: {0}, SKIPPING (job {1})".format(s.id,s.job.id)
                    continue
                else:
                    print "entering spacer: {0}".format(s.id)
                    
                genome_db.enter_hits(s)

            except JobERR, e:
                print "excepted a job/spacer on ENTRY for job {0}".format(s.job.id)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset','-r',dest="reset",
                        default=False, const = True , action="store_const",
                        help = "Reset all jobs (deletes /jobs/*)")
    parser.add_argument('inifile')
    args = parser.parse_args()

    init_env(args.inifile)
    
    print cfront_settings
    jobpath = cfront_settings["jobs_directory"]
    if args.reset:
        for d in os.listdir(jobpath):
            print "removing directory: {0}".format(d)
            shutil.rmtree(os.path.join(jobpath,d))
            print os.path.join(jobpath,d)

        with transaction.manager:
            for j in Session.query(Job).all():
                for s in j.spacers:
                    Session.delete(s)
                j.computing_spacers = False
                j.computed_spacers = False
                j.files_computing = False
                j.files_ready=False
                j.date_completed = None
                
                
    
    queue_loop()


if __name__ == "__main__":
    main()
