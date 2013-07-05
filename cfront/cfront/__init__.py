from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from cfront.models import Session, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    #static routes
    config.add_static_view('/css', 'static/css', cache_max_age=3600)
    config.add_static_view('/js', 'static/js', cache_max_age=3600)
    config.add_static_view('/img', 'static/img', cache_max_age=3600)
    config.add_static_view('/pages', 'static/pages', cache_max_age=3600)

    #page routes
    config.add_route('main', '/')

    #ajax routes
    config.add_route('job_compute_spacers', '/j/compute_spacers/{job_id}')
    config.add_route('job_compute_hits', '/j/compute_hits/{job_id}')
    config.add_route('job_check_hits', '/j/check_hits/{job_id}')

    #rest routes
    config.add_route('job_rest', '/r/job/{job_id}')
    
    config.scan()
    return config.make_wsgi_app()
