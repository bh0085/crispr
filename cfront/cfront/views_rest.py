from pyramid.response import Response
from pyramid.view import view_config
from .models import Job, Session, Spacer, Hit
import datetime
from .utils import webserver_db as wdb

@view_config(route_name="job_rest", renderer="json")
def job_rest(request):
    method = request.method
    job = request.job
    if method != 'POST' and not job:
        raise Exception("id-less request with a non-post method")
    elif method == 'POST' and job:
        raise Exception("post request for persisted job")

    if method == 'POST':
        raise Exception("please post jobs through the ajax gateway")
        job = Job(date_submitted = datetime.datetime.utcnow(),
                  sequence = request.params["sequence"],
                  genome = Job.GENOMES["HUMAN"],
                  name = request.params["name"],
                  email = request.params["email"],
                  date_completed = None
        )

        

    elif method == 'GET':
        pass
    else:
        raise Exception("unsupported method: {0}".format(method))
                  
    Session.add(job)
    Session.flush()
    json = job.toJSON()
    json["spacers"] = [s.toJSON() for s in job.spacers]

    return json


@view_config(route_name="spacer_rest", renderer="json")
def spacer_rest(request):

    # fakes the resource factory
    spacer_id = int(request.matchdict['spacer_id'])
    if  spacer_id == -1:
        spacer = None
    else:
        spacer = Session.query(Spacer).get(spacer_id)
        if not spacer:
            raise Exception("Spacer not found")

    method = request.method

    if method == 'GET':
        pass
    else:
        raise Exception("unsupported method: {0}".format(method))
                  
    print spacer.score
    json = spacer.toJSON()

    return json
