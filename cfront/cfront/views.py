from pyramid.response import Response
from pyramid.view import view_config

from cfront.utils import genome_db, webserver_db

@view_config(route_name='main', renderer='main.mako')
def main_view(request):
    return {}
