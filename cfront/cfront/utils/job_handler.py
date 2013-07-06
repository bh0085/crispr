#!/usr/bin/env python

from cfront.utils import genome_db, webserver_db, genome_io
from cfront.models import Session, Job, Spacer, Hit
import sys
import time
import transaction
from pyramid.paster import bootstrap
def init_env(p):
    env = bootstrap(p)

def queue_loop():
    while True:
        process_queue()
        print "processing"
        time.sleep(10)
        

def process_queue():
    with transaction.manager:
        unspacered = Session.query(Job).filter(Job.computed_spacers == False).all()
        for j in unspacered:
             Session.add(j)
             webserver_db.compute_spacers(j.id)
         
        unstarted = Session.query(Job).filter(Job.computing_hits == False).all()
        for j in unstarted:
             Session.add(j)
             genome_db.compute_hits(j.id)
         
        unfinished = Session.query(Job).filter(Job.computed_hits == False).all()
        for j in unfinished:
             Session.add(j)
             ready = genome_db.check_hits(j.id)
             if ready:
                 genome_db.enter_hits(j.id)
                 print "entering hits for {0}".format(j.id)
        
        print "Number of jobs unspacered: {0}".format(len(unspacered))
        print "Number of jobs unstarted (unfinished): {0} ({1})"\
             .format(len(unstarted),len(unfinished))
         
         
    

if __name__ == "__main__":
    init_env(sys.argv[1])
    queue_loop()
    
