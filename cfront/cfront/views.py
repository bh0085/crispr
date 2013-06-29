from pyramid.response import Response
from pyramid.view import view_config

import cfront.utils.genome_db as genome_db

@view_config(route_name='main', renderer='main.mako')
def main_view(request):
    return {}

@view_config(route_name='find_submit',renderer='json')
def find_submit(request):
    query = request.matchdict['query']
    return genome_db.submit_find_query(query)

@view_config(route_name='find_check',renderer='json')
def find_check(request):
    job_id = request.matchdict['job_id']
    return genome_db.check_find_query(job_id)

@view_config(route_name='find_retrieve',renderer='json')
def find_retrieve(request):
    job_id = request.matchdict['job_id']
    return genome_db.retrieve_find_query(job_id)
