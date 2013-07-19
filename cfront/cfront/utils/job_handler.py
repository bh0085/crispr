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
        time.sleep(1)
        


def process_queue():
    with transaction.manager:

        unstarted = Session.query(Spacer).filter(Spacer.computing_hits == False).all()
        for s in unstarted[:3]:
             genome_db.compute_hits(s.id)
         
        entered =0
        unfinished = Session.query(Spacer).filter(Spacer.score == None).all()
        for s in unfinished:
             ready = genome_db.check_hits(s.id)
             if ready:
                 entered+=1
                 if entered >3:
                     break
                 print "entering spacer: {0}".format(s.id)
                 genome_db.enter_hits(s.id)

if __name__ == "__main__":
    init_env(sys.argv[1])
    queue_loop()
    
