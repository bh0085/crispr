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

    import csv
    with open("/fastdata/crispr/config/genomes.csv") as f:
        r = csv.reader(f)
        cols = r.next()
        genomes_settings["genomes_info"] = []
        for l in r:
            g = dict(zip(cols,l))
            genomes_settings["genomes_info"].append(g)
    #genomes_settings["genome_names"] = [e.strip() 
    #                                    for e in genomes_settings["genome_names"].split(",")]
     

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
    
    config.add_route('splash_v2', '/', factory=PageResourceFactory)
    config.add_route('gene_results_v2', '/v2/{assembly}/{geneid}/gene_results', factory=PageResourceFactory)
    config.add_route('submit_v2', '/v2/{assembly}/submit', factory=PageResourceFactory)
    config.add_route('genes_autocomplete_array', '/v2/{assembly}/gene_names.json')
    config.add_route('genes_autocomplete_info', '/v2/{assembly}/genes_info.json')
    config.add_route('gene_genbank', '/v2/{assembly}/{geneid}/gene.gb')
    config.add_route('gene_genbank_spacer', '/v2/{assembly}/{geneid}/{tool}/{guide_sequence}/gene.gb')
    config.add_route('gene_genbank_all_spacers', '/v2/{assembly}/{geneid}/all_spacers.gb')
    config.add_route('gene_fasta', '/v2/{assembly}/{geneid}/gene.fa')
    config.add_route('gene_genbank_json', '/v2/{assembly}/{geneid}/genbank.json')
    config.add_route('gene_sequence', '/v2/{assembly}/{geneid}/sequence.json')
    config.add_route('job_data','/v2/{assembly}/{geneid}/job.json')
    
    config.add_route('about', '/about', factory=PageResourceFactory)
    config.add_route('batch', '/v1/batch/{batch_key}', factory = BatchResourceFactory)
    config.add_route('submit', '/v1/submit', factory=PageResourceFactory)
    config.add_route('job', '/v1/job/{job_key}', factory=PageResourceFactory)
    config.add_route('readonly', '/readonly',factory=PageResourceFactory)
    config.add_route('readout', '/v1/guides/{job_key}',factory=PageResourceFactory)
    config.add_route('nickase', '/v1/nick/{job_key}',factory=PageResourceFactory)
    config.add_route('downloads', '/v1/downloads/{job_key}',factory=PageResourceFactory)

    
    #export routes
    config.add_route('gb_all_nicks', '/v1/export/nicks_gb/{job_key}',factory=JobResourceFactory)
    config.add_route('gb_one_nick', '/v1/export/nicks_gb/{job_key}/{spacerfwdid}/{spacerrevid}',factory=JobResourceFactory)
    config.add_route('csv_one_spacer', '/v1/export/spacer_csv/{job_key}/{spacerid}',factory=JobResourceFactory)
    config.add_route('csv_all_guides', '/v1/export/csv_all_guides/{job_key}',factory=JobResourceFactory)
    config.add_route('gb_all_guides', '/v1/export/guides_gb/{job_key}',factory=JobResourceFactory)
    
    #v2 ajax routes
    config.add_route('v2_query_gene', '/v2/{assembly}/{geneid}/{email}/query_gene')

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
