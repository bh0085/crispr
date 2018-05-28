from pyramid.view import view_config
from .utils import webserver_db, genome_db, mail
from .models import Session, Job, Hit, Spacer, JobERR, Batch
import datetime, re
from cfront import cfront_settings
import simplejson as sjson

import gffutils
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import Alphabet
from Bio.SeqRecord import SeqRecord
from gffutils import biopython_integration
import StringIO
import random
from pyramid.response import FileResponse
import os
    
import sendgrid
import os
from sendgrid.helpers.mail import *

import base64




@view_config(route_name='email_all_genbank',renderer = 'json')
def email_all_genbankl(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    email = request.matchdict['email']

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("ben@coolship.io")
    
    to_email = Email(email)
    
    
    subject = "your genbank files are ready"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    #
    #
    #
    #
    #"""Build attachment mock."""
    #attachment = Attachment()
    #attachment.content = (gene_genbank_spacers_helper(assembly, geneid, returntype="text",
    #                            spacer_sequence_filter=None,
    #                            tool_filter=None,
    #                            min_score=90))
    #
    #attachment.type = "application/pdf"
    #attachment.filename = "guides_{0}_{1}.gb".format(assembly,geneid)
    #attachment.disposition = "attachment"
    #attachment.content_id = "recommended guides"


    attachment = Attachment()
    text=gene_genbank_spacers_helper(assembly, geneid, returntype="text",
                                                                       spacer_sequence_filter=None,
                                                                       tool_filter=None,
                                                                       min_score=90)

    #text = gene_genbank_spacers_helper(assembly, geneid, returntype="filename",
    #                                                                   spacer_sequence_filter=None,
    #                                                                    tool_filter=None,
    #                                                                    min_score=90)

    #with open('raw/test-report.csv', 'rb') as fd:
    #b64data = base64.b64encode("""hi, hello
#    1, 2
#""")


    b64data = base64.b64encode(text)
    attachment = Attachment()
    out = str(b64data)
    attachment.content = out
    
    #attachment.content = ( "BwdW")
    #attachment.type = "text/plain"
    attachment.filename = "guides_{0}_{1}.gb".format(assembly,geneid)
    attachment.disposition = "attachment"
    attachment.content_id = "genbank"

    mail.add_attachment(attachment)

    
    response = sg.client.mail.send.post(request_body=mail.get())

    #raise Exception(email)

    print(response.status_code)
    print(response.body)
    print(response.headers)


    
    return {"status":"success"}
    

@view_config(route_name='genes_autocomplete_info',renderer='json')
def genes_autocomplete_info(request):

    import gffutils
    assembly = request.matchdict['assembly']
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    allgenes = list(db.features_of_type("gene"))
    #allnames = [e["Name"] for e in allgenes]
    genes_dict = dict([( e["Name"][0], {"strand":e.strand,"start":e.start,"end":e.end,"chrom":e.chrom}) for e in allgenes])
    return genes_dict



@view_config(route_name='genes_autocomplete_array',renderer='json')
def genes_autocomplete_array(request):

    import gffutils
    assembly = request.matchdict['assembly']
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    allgenes = list(db.features_of_type("gene"))
    return [ e["Name"][0] for e in allgenes]


@view_config(route_name="gene_genbank")
def gene_genbank(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    fname = gene_genbank_helper(assembly,geneid,returntype="filename")
    response = FileResponse(
        fname,
        request=request,
        content_type='text'
        )
    return response




@view_config(route_name="gene_genbank_spacer")
def gene_genbank_spacer(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']

    guide_sequence=request.matchdict['guide_sequence']
    tool=request.matchdict['tool']


    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    fname = gene_genbank_spacers_helper(assembly,geneid,returntype="filename",spacer_sequence_filter=guide_sequence,tool_filter=tool)


        
    response = FileResponse(
        fname,
        request=request,
        content_type='text'
        )
    return response



@view_config(route_name="gene_genbank_all_spacers")
def gene_genbank_all_spacers(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    fname = gene_genbank_spacers_helper(assembly,geneid,returntype="filename",spacer_sequence_filter=None)


        
    
    response = FileResponse(
        fname,
        request=request,
        content_type='text'
        )
    return response



@view_config(route_name="gene_fasta")
def gene_fasta(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    fname= gene_fasta_helper(assembly, geneid, returntype="filename")
    response = FileResponse(
        fname,
        request=request,
        content_type='text'
        )
    return response
    

@view_config(route_name="gene_genbank_json",renderer="json")
def gene_genbank_json(request):    
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    return  gene_genbank_helper(assembly, geneid, returntype="text")
    

@view_config(route_name="gene_sequence", renderer="json")
def gene_sequence(request):
    assembly = request.matchdict['assembly']
    geneid = request.matchdict['geneid']
    return gene_sequence_helper(assembly,geneid)
    
def gene_sequence_helper(assembly, geneid):

    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))

    return seq_letters

def gene_fasta_helper(assembly, geneid, returntype="filename"):
        
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))
    
    record  = SeqRecord(Seq(seq_letters,Alphabet.DNAAlphabet()),
                        id=geneid, name=gene.attributes["Name"][0],
                        description="gene region exported by crispr.mit.edu",
                        features=[sf])

    fname = "/fastdata/webserver/tmp/{0}.fa".format(long(random.random()*1000000))
    with open(fname,"w") as f:
        SeqIO.write(record,f,"fasta")

    if returntype=="filename":
        return fname
    elif returntype =="text":
        with open(fname) as fopen:
            return fopen.read()
    else:
        raise Exception("unknown return type {0}".format(returntype))

def gene_genbank_helper(assembly, geneid, returntype="filename"):

    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))
    
    record  = SeqRecord(Seq(seq_letters,Alphabet.DNAAlphabet()),
                        id=geneid, name=gene.attributes["Name"][0],
                        description="gene region exported by crispr.mit.edu",
                        features=[sf])

    fname = "/fastdata/webserver/tmp/{0}.gb".format(long(random.random()*1000000))
    with open(fname,"w") as f:
        SeqIO.write(record,f,"genbank")

    
    if returntype=="filename":
        return fname
    elif returntype=="text":
        with open(fname) as fopen:
            return fopen.read()
    else:
        raise Exception("unknown return type {0}".format(returntype))

def gene_genbank_spacers_helper(assembly, geneid, returntype="filename",
                                spacer_sequence_filter=None,
                                tool_filter=None,
                                min_score=90):


    
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))


    
    gene_queries_directory = "/fastdata/crispr/gene_queries"
    query_data_basename = "{assembly}_{geneid}_data.json".format(assembly=assembly,geneid=geneid)
    query_data_file = os.path.join(gene_queries_directory,query_data_basename)
    with open(query_data_file) as fopen:
        status = sjson.loads(fopen.next())
        data = sjson.loads(fopen.next())


    cas9_spacers = data["cas9"]["spacers"]
    cpcf1_spacers = data["cas9"]["spacers"]

    
    sfs = []
    for tool,spacer_list in {"cas9":cas9_spacers,
                             "cpcf1":cpcf1_spacers}.items():
        if tool_filter != None:
            if tool != tool_filter:
                continue
        print tool
        for s in spacer_list:
            if spacer_sequence_filter:
                if s["guide_sequence"] != spacer_sequence_filter:
                    continue
            if min_score != None:
                
                print s["score"]
                if s["score"] < min_score:
                    continue

            quals = {}
            if s["pam_before"]:
                quals.update({"pam5":s["pam_before"]})
                
            if s["pam_after"]:
                quals.update({"pam3":s["pam_after"]})

            quals.update({"score"}:s["score"]})
            quals.update({"tool"}:tool)
                
            sfs.append(SeqFeature(FeatureLocation(s["guide_start"],
                                                  s["guide_start"]+s["guide_length"],
                                                  strand=s["guide_strand"]),
                                  id=s["guide_sequence"],
                                  qualifiers=quals,
                                  type="{0}_tgt".format(tool)))



    
    record  = SeqRecord(Seq(seq_letters,Alphabet.DNAAlphabet()),
                        id=geneid, name=gene.attributes["Name"][0],
                        description="{2} gene {1} exported by crispr.mit.edu, with all spacer sequences scored >{0}".format(min_score,db[geneid].attributes['Name'][0],assembly),
                        features=[sf]+sfs,
                        annotations={"organism":assembly})

   
    
    fname = "/fastdata/webserver/tmp/{0}.gb".format(long(random.random()*1000000))
    with open(fname,"w") as f:
        SeqIO.write(record,f,"genbank")

    
    if returntype=="filename":
        return fname
    elif returntype=="text":
        with open(fname) as fopen:
            return fopen.read()
    else:
        raise Exception("unknown return type {0}".format(returntype))

    
gene_queries_directory = "/fastdata/crispr/gene_queries"
emails_directory = "/fastdata/crispr/emails"
def post_or_update_gene_query(assembly, geneid, email):
    if not os.path.isdir(emails_directory): os.makedirs(emails_directory)
    if not os.path.isdir(gene_queries_directory): os.makedirs(gene_queries_directory)
        
    query_data_basename = "{assembly}_{geneid}_data.json".format(assembly=assembly,geneid=geneid)
    query_data_file = os.path.join(gene_queries_directory,query_data_basename)

    #create an empty datafile
    with open(query_data_file,"a"): pass

    email_clean  = re.compile("[^A-z]").sub("_",email)
    user_email_directory = os.path.join(emails_directory,email_clean)
    if not os.path.isdir(user_email_directory): os.makedirs(user_email_directory)
    if not os.path.isfile(os.path.join(user_email_directory,query_data_basename)):
        os.symlink(query_data_file,os.path.join(user_email_directory,query_data_basename))
    
    

@view_config(route_name="job_data", renderer="json")
def job_data(request):
    assembly = request.matchdict["assembly"]
    geneid = request.matchdict["geneid"]


    gene_queries_directory = "/fastdata/crispr/gene_queries"
    query_data_basename = "{assembly}_{geneid}_data.json".format(assembly=assembly,geneid=geneid)
    query_data_file = os.path.join(gene_queries_directory,query_data_basename)
    
    with open(query_data_file) as fopen:
        try:
            status = sjson.loads(fopen.next())
        except StopIteration, e:
            status = None
            
        try:
            data = sjson.loads(fopen.next())
        except StopIteration, e:
            data = None

    return data

@view_config(route_name="v2_query_gene",renderer='json')
def v2_query_gene(request):

    assembly = request.matchdict["assembly"]
    geneid = request.matchdict["geneid"]
    email = request.matchdict["email"]


    post_or_update_gene_query(assembly,geneid,email)
    
    return {"status":"success",
            "message":None,
            "geneid":geneid,
            "email":email,
            "assembly":assembly}
        
            
    


