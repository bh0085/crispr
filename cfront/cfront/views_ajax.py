from pyramid.view import view_config
from .utils import webserver_db, genome_db

@view_config(route_name='job_compute_spacers', renderer='json')
def job_compute_spacers(request):
    job_id = request.matchdict['job_id']
    status = webserver_db.compute_spacers(job_id)
    return status

@view_config(route_name='job_compute_hits',renderer='json')
def job_compute_hits(request):
    job_id = request.matchdict['job_id']
    status = genome_db.compute_hits(job_id)
    return status

@view_config(route_name='job_check_hits',renderer='json')
def job_check_hits(request):
    job_id = request.matchdict['job_id']
    status = genome_db.check_hits(job_id)
    return status
