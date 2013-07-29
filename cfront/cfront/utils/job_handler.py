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
    with transaction.manager:

        unstarted = Session.query(Spacer).filter(Spacer.computing_hits == False).all()
        for s in unstarted[:3]:
             genome_db.compute_hits(s.id)
         
        entered =0
        unfinished = Session.query(Spacer).join(Job).filter(Job.failed == False).filter(Spacer.score == None).all()
        for s in unfinished:
             ready = genome_db.check_hits(s.id)
             if ready:
                if s.job.failed:
                    print "marked job failed for: {0}, SKIPPING (job {1})".format(s.id,s.job.id)S
                    continue
                else:
                    print "entering spacer: {0}".format(s.id)
                #try:
                genome_db.enter_hits(s.id)
                #except JobERR, e:
                # if cfront_settings.get("debug_mode", False):
                #  raise Exception()
                # else:
                #  pass
                # raise Exception()
                
                entered+=1
                if entered >3:
                     break

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
    
    queue_loop()


if __name__ == "__main__":
    main()
