#!/usr/bin/env python
import  argparse, datetime, re
from pyramid.paster import bootstrap
from cfront.models import Session, Spacer, Hit, Job
from cfront import cfront_settings
import transaction
import os, shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inifile",
                        help="inifile to configure the server")
    args = parser.parse_args()
    
    #starts up the paster env
    env = bootstrap(args.inifile)
    jobpath = cfront_settings["jobs_directory"]


    #for d in os.listdir(jobpath):
    #        print "removing directory: {0}".format(d)
    #        shutil.rmtree(os.path.join(jobpath,d))
    #        print os.path.join(jobpath,d)

    with transaction.manager:
            for j in Session.query(Job).order_by(Job.id).all():
                if j.genome_name == "hg19" :
                    continue
                else:
                    for s in j.spacers:
                        Session.delete(s)
                    print "deleting spacers for job {0}".format(j.id)
                    j.computed_spacers = False
                    j.files_ready=False
                    j.date_completed = None
                    j.files_failed =False
                    j.failed = False
