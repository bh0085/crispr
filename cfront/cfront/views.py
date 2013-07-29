from pyramid.response import Response
from pyramid.view import view_config
from cfront.utils import genome_db, webserver_db

@view_config(route_name="readout", renderer='readout.mako')
def readout_view(request):
    jj = request.job.toJSON()
    spacers = [s.toJSON() for s in request.job.spacers]
    jj["spacers"] = spacers
    return {"init_state":{"job":jj},
            "sessionInfo":{"routes":routes_dict(request)}}
@view_config(route_name="submit", renderer="submit.mako")
def submit_view(request):
    return { "sessionInfo":{"routes":routes_dict(request)}}

@view_config(route_name="maintainance",renderer='maintainance.mako')
def maintainance_view(request):
    return {}

from pyramid.config import Configurator
def routes_dict(request):
    return dict([(k,v.path) 
                for k,v in Configurator(request.registry).get_routes_mapper().routes.items()])


