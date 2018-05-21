from pyramid.response import Response
from pyramid.view import view_config
from cfront.utils import genome_db, webserver_db, nickase
from cfront import genomes_settings
import simplejson as sjson
import os
import gffutils

from gffutils import biopython_integration

from pyramid.config import Configurator
def routes_dict(request):
    return dict([(k,v.path) 
                for k,v in Configurator(request.registry).get_routes_mapper().routes.items()])



@view_config(route_name="submit_v2", renderer="base.mako")
def submit_v2_view(request):
    assembly = request.matchdict["assembly"]
    genome_infos = dict([[e["assembly"],e] for e in genomes_settings["genomes_info"]])
    
    import gffutils
    assembly = request.matchdict['assembly']
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    allgenes = list(db.features_of_type("gene"))
    gene_infos = [{"name":e["Name"][0],'id':e.id} for e in allgenes]

    
    return  { "sessionInfo":
             {"routes":routes_dict(request),
              "genome_info":genome_infos[assembly],
              "gene_infos":gene_infos}}

@view_config(route_name="splash_v2", renderer="base.mako")
def splash_v2_view(request):
    return  { "sessionInfo":
             {"routes":routes_dict(request),
              "genomes_info":genomes_settings["genomes_info"]}} 



@view_config(route_name="gene_results_v2", renderer="base.mako")
def gene_results_v2(request):

    assembly=request.matchdict["assembly"]
    geneid=request.matchdict["geneid"]

    genome_infos = dict([[e["assembly"],e] for e in genomes_settings["genomes_info"]])
    
    gene_queries_directory = "/fastdata/crispr/gene_queries"
    query_data_basename = "{assembly}_{geneid}_data.json".format(assembly=assembly,geneid=geneid)
    query_data_file = os.path.join(gene_queries_directory,query_data_basename)

    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    
    gene_info = dict(gene.attributes.iteritems())

    gene_info["start"] = gene.start
    gene_info["end"] = gene.end
    gene_info["id"] = gene.id
    gene_info["strand"] = gene.strand
    gene_info["chrom"] = gene.chrom


    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))

    
    
    with open(query_data_file) as fopen:
        try:
            status = sjson.loads(fopen.next())
        except StopIteration, e:
            status = None
            
        try:
            data = sjson.loads(fopen.next())
        except StopIteration, e:
            data = None
            
        
    return {
        "sessionInfo":
        {"routes":routes_dict(request),
         "assembly":assembly,
         "geneid":geneid,
         "data":data,
         "status":status,
         "genome_info":genome_infos[assembly],
         "gene_info":gene_info,
         "seq_letters":seq_letters
        }
    }
