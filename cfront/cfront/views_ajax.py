from pyramid.view import view_config
from .utils import webserver_db, genome_db
from .models import Session, Job, Hit, Spacer

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
