from pyramid.response import Response
from pyramid.view import view_config

from cfront.utils import genome_db, webserver_db

@view_config(route_name="readout", renderer='readout.mako')
def readout_view(request):
    return {}
@view_config(route_name="submit", renderer="submit.mako")
def submit_view(request):
    return {}
