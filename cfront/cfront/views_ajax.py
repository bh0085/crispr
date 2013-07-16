from pyramid.view import view_config
from .utils import webserver_db, genome_db
from .models import Session, Job, Hit, Spacer
import datetime

@view_config(route_name='job_check_spacers', renderer='json')
def job_check_spacers(request):
    job_id =  request.matchdict['job_id']
    job = Session.query(Job).get(job_id)
    return job.computed_spacers

@view_config(route_name='job_check_hits', renderer='json')
def job_check_hits(request):
    job_id =  request.matchdict['job_id']
    job = Session.query(Job).get(job_id)
    return job.computed_hits

@view_config(route_name='job_retrieve_spacers',renderer='json')
def job_retrieve_spacers(request):
    job_id = request.matchdict['job_id']
    job = Session.query(Job).get(job_id)
    return [s.toJSON() for s in job.spacers]

@view_config(route_name='job_retrieve_hits',renderer='json')
def job_retrieve_hits(request):
    job_id = request.matchdict['job_id']
    job = Session.query(Job).get(job_id)
    return [h.toJSON() for s in job.spacers for h in s.hits]

@view_config(route_name="job_post_new",renderer='json')
def job_post_new(request):
    
    matches = webserver_db.check_genome(request.params["sequence"])
    infos = webserver_db.compute_spacers(request.params["sequence"])

    print matches
    print infos

    if matches == None:
            return {"status":"error",
                    "message":"nomatches",
                    "matches":None,
                    "job_id":None}
    elif len(matches) > 1:
            return {"status":"error",
                    "message":"manymatches",
                    "matches":matches,
                    "job_id":None}
    elif len(infos) == 0:
        return {"status":"error",
                "message":"nospacers",
                "matches":matches,
                "job_id":None}
    else:
            job = Job(date_submitted = datetime.datetime.utcnow(),
                  sequence = request.params["sequence"],
                  genome = Job.GENOMES["HUMAN"],
                  name = request.params["name"],
                  email = request.params["email"],
                  date_completed = None
                  )

            Session.add(job)
            for spacer_info in infos:
                Session.add(Spacer(job = job,**spacer_info))

            job.computed_spacers = True
            Session.flush()
            print job.id

            return {"status":"success",
                    "message":None,
                    "matches":matches,
                    "job_id":job.id}
                    
            
        
