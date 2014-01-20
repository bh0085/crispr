#!/usr/bin/env python

from cfront.utils import genome_db, webserver_db, genome_io, byte_scanner
from cfront.models import Session, SpacerERR, JobERR, Job, Spacer, Hit
import sys, shutil
import time
import transaction
from pyramid.paster import bootstrap
from cfront import cfront_settings, genomes_settings as genomes_settings
import argparse, os
from Queue import Empty
import multiprocessing as mp
from multiprocessing import Process, Manager, Value, Array, JoinableQueue, Queue
import json
import redis

def init_env(p):
    env = bootstrap(p)

def queue_loop(ofs,stride):
    while True:
        process_queue(ofs,stride)
        time.sleep(2)
            

def worker(jobs_q,**genomes):
    r = redis.Redis()
    done = False
    while not done:
        job = jobs_q.get()
        if job == 'done':
            done = True
        else:
            print job
            spacerid = job['spacerid']            
            guide = job["guide"]
            genome_name = job["genome_name"]  
            results = genome_db.fetch_hits_in_thread_shm(guide, genome_name, genomes[genome_name])   
            r.rpush(
                "cfront-{0}:job:hits".format("dev" if cfront_settings.get("debug_mode",False) else "prod"),
                json.dumps({"spacerid": spacerid,
                            "results":results}))
                    
        jobs_q.task_done()

    return

def process_queue(ofs, stride):
    possible_spacer_jobs = Session.query(Job).filter(Job.computed_spacers == False).all()
    selected_jobs = possible_spacer_jobs

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
                print j.id
            except JobERR, e:
                if e.message == Job.NOSPACERS:
                    print "No spacers in JOB ID: {0}".format(j.id)
                elif e.message == Job.ERR_INVALID_CHARACTERS:
                    print e.message
                else:
                    print "Excepted a job error during Spacer finding for Job: {0}".format(j.id)
                    print j.id
                    print j.sequence
                    raise e


    possible_hit_jobs =  Session.query(Job)\
                    .join(Spacer)\
                    .filter(Spacer.score == None)\
                    .filter(Job.failed == False)\
                     .all()
    selected_hit_jobs = possible_hit_jobs


    procs = []
    max_procs = 9
    manager = Manager()
    jobs_q = JoinableQueue()


    r = redis.Redis()

    dcount = 0 
    while(1):
        item_json = r.lpop("cfront-{0}:job:hits".format("dev" if cfront_settings.get("debug_mode",False) else "prod"))
        dcount += 1
        if item_json == None:
            break
    print "popped {0} keys from previous submission".format(dcount)



    for i in range(max_procs):
        print("loading {0}".format(i))
        genomes_dict =dict([n,byte_scanner.get_library_bytes_shm(n) ]
                           for n in genomes_settings["genome_names"])
        proc = mp.Process(target=worker, args=[jobs_q],
                          kwargs = genomes_dict
                            )
        proc.daemon=True
        proc.start()
        procs.append(proc)


    if len(selected_hit_jobs) > 0:
        with transaction.manager:
            def priority(j):
                from random import random
                f = 1 if random() > .5 else -1
                if j.batch is not None: return 100000000
                else: return f* j.id 

            for i,j in enumerate(selected_hit_jobs):
                if not j in Session: 
                    selected_hit_jobs[i] = Session.merge(j)

            batched_jobs = [j for j in selected_hit_jobs if j.batch is not None]
            #sorts jobs to process recent submissions and non-batch jobs first        
            top_jobs = sorted(selected_hit_jobs, key = priority)[:12]
            for top_job in top_jobs:
                if not top_job in Session: top_job = Session.merge(top_job)

                #spacers may be deleted from the session in the interior of this loop

                for i,s in enumerate([s for s in top_job.spacers if s.score is None][:2]):
                    jobs_q.put({"genome_name":s.job.genome_name,
                                "guide":s.guide,
                                "spacerid":s.id})
                
                
    for i in range(max_procs):
        jobs_q.put("done")
    for i,p in enumerate(procs):
        p.join()


    


    while(1):
       item_json = r.lpop("cfront-{0}:job:hits".format("dev" if cfront_settings.get("debug_mode",False) else "prod"))
       
       if item_json == None:
           break
       else:
           item = json.loads(item_json)
           
       print "PROCESSING ITEM"
       with transaction.manager:
          #HANDLE POSSIBLE ERRORS!
          result = item["results"]
          success = result[0]
          hits = result[1]
          sid = item["spacerid"]
          print("completing {0}".format(sid))
          try:
              if not success:
                  #exception handling
                  if hits=="too_many_hits":
                      raise SpacerERR(Spacer.ERR_TOOMANYHITS, Session.query(Spacer).get(sid))
                  elif hits =="no_hits":
                      raise SpacerERR(Spacer.ERR_NO_HITS,Session.query(Spacer).get(sid))
                  elif hits == "failed":
                      raise SpacerERR(Spacer.ERR_FAILED_TO_RETRIEVE_HITS,Session.query(Spacer).get(sid))
              else:
                  genome_db.process_hits_for_spacer(sid, hits)
                  print "DONE PROCESSING JOB"
          except JobERR, e:
              print "excepted a job/spacer error on COMPUTE for job {0}".format(s.job.id, top_job)
          except SpacerERR, e:
              print "excepted a spacer error for spacer id {0}".format(Session.query(Spacer).get(sid))
              print e.message
          except Exception, e:
              print "EXCEPTED AN UNKNOWN ERROR {0}".format(sid)
              print "EXCEPTED AN UNKNOWN ERROR"
              print "EXCEPTED AN UNKNOWN ERROR"
              #spc = Session.query(Spacer).get(sid)
              
              #serr = SpacerERR(Spacer.ERR_FAILED_TO_PROCESS_HITS,Session.query(Spacer).get(sid))  
              #print serr.message
              
           
       spacer = Session.query(Spacer).get(sid)


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
