from pyramid.response import Response
from pyramid.view import view_config
from models import Session, Job
from cfront.utils import genome_db, webserver_db

@view_config(route_name="readout", renderer='readout.mako')
def readout_view(request):
    jobid = request.matchdict['job_id']
    job = Session.query(Job).get(jobid)
    jj = job.toJSON()
    spacers = [s.toJSON() for s in job.spacers]
    jj["spacers"] = spacers
    return {"init_state":{"job":jj}}
@view_config(route_name="submit", renderer="submit.mako")
def submit_view(request):
    return {}
