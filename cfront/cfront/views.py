from pyramid.response import Response
from pyramid.view import view_config
from cfront.utils import genome_db, webserver_db
from cfront.models import JobERR, JobNOTFOUND, JobFAILED

@view_config(route_name="readout", renderer='base.mako')
def readout_view(request):
    jj = request.job.toJSON()
    spacers = [s.toJSON() for s in request.job.spacers]
    jj["spacers"] = spacers
    return {"init_state":{"job":jj},
            "sessionInfo":{"routes":routes_dict(request)}}

@view_config(route_name="nickase", renderer="base.mako")
def nickase_view(request):
    jj = request.job.toJSON()
    spacers = [s.toJSON() for s in request.job.spacers]
    jj["spacers"] = spacers
    return {"init_state":{"job":jj},
            "sessionInfo":{"routes":routes_dict(request)}}

@view_config(route_name="submit", renderer="base.mako")
def submit_view(request):
    return { "sessionInfo":{"routes":routes_dict(request)}}

@view_config(route_name="readonly", renderer="readonly.mako")
def readonly_view(request):
    return { "sessionInfo":{"routes":routes_dict(request)}}

@view_config(route_name="maintainance",renderer='maintainance.mako')
def maintainance_view(request):
    return {}

from pyramid.config import Configurator
def routes_dict(request):
    return dict([(k,v.path) 
                for k,v in Configurator(request.registry).get_routes_mapper().routes.items()])


@view_config(context=JobERR, renderer="json")
def joberr_view(err, request):
    return   {"status":"error",
              "message":err.message,
              "job_key":err.job.key if err.job is not None else None}
        
@view_config(context=JobNOTFOUND, renderer="errors/notfound.mako")
def jobnotfound_view(err,request):
    return {"job":None}
    
@view_config(context=JobFAILED, renderer="errors/failed.mako")
def jobfailed_view(err,request):
    return {"job":err.job.toJSON(),
            "message":err.job.error_message
    }
