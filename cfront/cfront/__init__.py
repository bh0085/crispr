from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from cfront.models import Session, Base

cfront_settings = {}
genomes_settings = {}

from .route_factories import (
    JobResourceFactory,
    PageResourceFactory,
    BatchResourceFactory
)


def set_cfront_settings(settings):
    prefix = "cfront."
    global cfront_settings
    for k,v in settings.iteritems():
        if prefix == k[:len(prefix)]:
            cfront_settings[k[len(prefix):]] = (v.lower()=='true') \
                                         if v.lower() in ['true', 'false'] else v

def set_genomes_settings(settings):
    prefix = "genomes."
    global genomes_settings
    for k,v in settings.iteritems():
        if prefix == k[:len(prefix)]:
            genomes_settings[k[len(prefix):]] = (v.lower()=='true') \
                                                if v.lower() in ['true', 'false'] else v
    genomes_settings["genome_names"] = [e.strip() 
                                        for e in genomes_settings["genome_names"].split(",")]
     

def main(global_config, **settings):
    """ 
    This function returns a Pyramid WSGI application.
    """
    import inspect
    set_cfront_settings(settings)
    set_genomes_settings(settings)

    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    #static routes
    config.add_static_view('/css', 'static/css', cache_max_age=3600)
    config.add_static_view('/js', 'static/js', cache_max_age=3600)
    config.add_static_view('/img', 'static/img', cache_max_age=3600)
    config.add_static_view('/pages', 'static/pages', cache_max_age=3600)
    config.add_static_view('/files', 'static/files', cache_max_age=3600)

    #page routes
    config.add_route('about', '/about', factory=PageResourceFactory)
    config.add_route('batch', '/batch/{batch_key}', factory = BatchResourceFactory)
    config.add_route('submit', '/', factory=PageResourceFactory)
    config.add_route('job', '/job/{job_key}', factory=PageResourceFactory)
    config.add_route('readonly', '/readonly',factory=PageResourceFactory)
    config.add_route('readout', '/guides/{job_key}',factory=PageResourceFactory)
    config.add_route('nickase', '/nick/{job_key}',factory=PageResourceFactory)
    config.add_route('downloads', '/downloads/{job_key}',factory=PageResourceFactory)
    
    #export routes
    config.add_route('gb_all_nicks', '/export/nicks_gb/{job_key}',factory=JobResourceFactory)
    config.add_route('gb_one_nick', '/export/nicks_gb/{job_key}/{spacerfwdid}/{spacerrevid}',factory=JobResourceFactory)
    config.add_route('csv_one_spacer', '/export/spacer_csv/{job_key}/{spacerid}',factory=JobResourceFactory)
    config.add_route('csv_all_guides', '/export/csv_all_guides/{job_key}',factory=JobResourceFactory)
    config.add_route('gb_all_guides', '/export/guides_gb/{job_key}',factory=JobResourceFactory)
    

    #ajax routes
    config.add_route('job_check_spacers','/j/check_spacers/{job_key}',factory=JobResourceFactory)
    config.add_route('job_post_new', '/j/post_new')
    config.add_route('jobs_from_fasta', '/j/from_fasta')
    config.add_route('job_from_spacers', '/j/from_spacers')
    config.add_route('job_retrieve_spacers', '/j/retrieve_spacers/{job_key}',factory=JobResourceFactory)
    config.add_route('job_email_complete', '/j/email_complete/{job_key}',factory=JobResourceFactory)

    config.add_route('spacer_retrieve_hits', '/s/retrieve_hits/{spacer_id}')
    config.add_route('spacer_check_hits', '/s/check_hits/{spacer_id}')
    config.add_route('spacer_retrieve_regions', '/s/retrieve_regions/{spacer_id}')

    #rest routes
    config.add_route('job_rest', '/r/job/{job_key}',factory=JobResourceFactory)
    config.add_route('batch_rest', '/r/batch/{batch_key}',factory=BatchResourceFactory)
    config.add_route('spacer_rest', '/r/spacer/{spacer_id}')
    
    config.add_route('maintainance','/sorry')

    config.scan()
    return config.make_wsgi_app()
