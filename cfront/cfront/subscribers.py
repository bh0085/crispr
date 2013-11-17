from pyramid.events import subscriber, NewRequest, NewResponse
import pyramid.httpexceptions as exc

@subscriber(NewResponse)
def no_cache_subscriber(event):
    """Sets http headers on all responses such that browsers won't cache them."""
    event.response.cache_expires = 1

@subscriber(NewRequest)
def http_method_override_subscriber(event):
    """Sets request.method properly using http method override if needed"""
    request = event.request
    if 'X-Http-Method-Override' in request.headers :
        request.method = request.headers['HTTP_X_HTTP_METHOD_OVERRIDE']

