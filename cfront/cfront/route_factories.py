from cfront.models import Job, Batch
import pyramid.httpexceptions as exc
from cfront import cfront_settings

from pyramid.security import (
    ALL_PERMISSIONS,
    Everyone,
    Authenticated,
    Allow,
    )

class Res(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, ALL_PERMISSIONS)
    ]
    def __init__(self, request):
        self.request = request
        request.job = None

def set_request_job(request):
        if 'job_key' in request.matchdict:
            if request.matchdict["job_key"] == "-1":
                request.job = None
            else:
                request.job = Job.get_job_by_key(request.matchdict["job_key"])
        else: raise Exception()


def set_request_batch(request):
        if 'batch_key' in request.matchdict:
            if request.matchdict["batch_key"] == "-1":
                request.batch = None
            else:
                request.batch = Batch.get_batch_by_key(request.matchdict["batch_key"])
        else: raise Exception()


        

class JobResourceFactory(Res):
    def __init__(self, request):
        set_request_job(request)


class BatchResourceFactory(Res):
    def __init__(self, request):
        set_request_batch(request)

class PageResourceFactory(Res):
    def __init__(self,request):
        print  cfront_settings.get("maintenance_mode", False)
        if "job_key" in request.matchdict:
            set_request_job(request)
            
        
        if cfront_settings.get("maintenance_mode", False):
            if not "sorry" in request.url:
                raise exc.HTTPFound(request.route_url("maintainance")) 

