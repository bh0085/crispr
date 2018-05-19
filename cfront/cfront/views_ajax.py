from pyramid.view import view_config
from .utils import webserver_db, genome_db, mail
from .models import Session, Job, Hit, Spacer, JobERR, Batch
import datetime, re
from cfront import cfront_settings



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




@view_config(route_name='job_check_spacers', renderer='json')
def job_check_spacers(request):
    return request.job.computed_spacers

@view_config(route_name='spacer_check_hits', renderer='json')
def spacer_check_hits(request):
    spacer_id =  request.matchdict['spacer_id']
    spacer = Session.query(Spacer).get(spacer_id)
    return spacer.computed_hits
    # NOT USED WITH NEW NICKASE VIEW MODE
@view_config(route_name='spacer_retrieve_regions',renderer='json')
def spacer_retrieve_regions(request):
    import twobitreader
    spacer_id = request.matchdict['spacer_id']
    spacer= Session.query(Spacer).get(spacer_id)
    genome = spacer.job.genome_name
    genome_path = "/fastdata/genomes/{0}.2bit".format(spacer.job.genome_name)
    tbf = twobitreader.TwoBitFile(genome_path)
    hits = spacer.hits
    return [{"sequence":tbf.get(h.chr)[h.start:h.start+100]} for h in hits[:100]]


@view_config(route_name='job_retrieve_spacers',renderer='json')
def job_retrieve_spacers(request):
    return [s.toJSON() for s in request.job.spacers]

@view_config(route_name='job_email_complete',renderer='json')
def job_email_complete(request):
    request.job.email_complete = request.params["do_email"]
    return request.job.email_complete

@view_config(route_name='spacer_retrieve_hits',renderer='json')
def spacer_retrieve_hits(request):
    spacer_id = request.matchdict['spacer_id']
    spacer = Session.query(Spacer).get(spacer_id)
    return {"genic":spacer.genic_hits,
            "top":spacer.top_hits}



@view_config(route_name="job_post_new",renderer='json')
def job_post_new(request):
    sequence = request.params["query"].upper()
    sequence = re.sub("\s","",sequence)

    if cfront_settings.get("debug_mode",False): print sequence
    
    if re.compile("[^AGTCN]").search(sequence) is not None:
            return {"status":"error",
                    "message":"Ambiguous or invalid characters found in input sequene.",
                    "matches":None,
                    "job_key":None}
    if len(sequence)<23 or len(sequence) > 250 :
        return {"status":"error",
                "message":"Sequence length not within allowed range (23 - 250bp)",
                "matches":None,
                "job_key":None}

    genome = request.params.get("genome","hg19")
    matches = webserver_db.check_genome(sequence,genome)
    infos = webserver_db.compute_spacers(sequence)

    if cfront_settings.get("debug_mode",False): print "lmatches: {0}".format(len(matches))
    if cfront_settings.get("debug_mode",False): print "linfos: {0}".format(len(infos))

    print request.params.get("inputRadios")
    if ( request.params.get("inputRadios",None) == "unique_genomic" ) and len(matches) == 0:
        raise JobERR(Job.ERR_NOGENOME,None)
    if request.params.get("inputRadios",None) == "unique_genomic" and len(matches) > 1:
        raise JobERR(Job.ERR_MULTIPLE_GENOME,None)
    elif len(infos) == 0:
        raise JobERR(Job.NOSPACERS,None)
    else:
        
    
        params = dict(date_submitted = datetime.datetime.utcnow(),
                      sequence = sequence,
                      name = request.params["name"],
                      email = request.params["email"],
                      genome = Job.GENOMES[genome],
                      query_type = request.params.get("inputRadios"))

        if len(matches) > 0:
            params.update(dict(chr=matches[0]["tName"],
                               start=matches[0]["tStart"],
                               strand=1 if matches[0]["strand"] == "+" else -1))
        if "key" in request.params:
            params["key"] = request.params.get("key")

        job = Job(**params)

        Session.add(job)

    for spacer_info in infos:
        Session.add(Spacer(job = job,**spacer_info))
            
    job.computed_spacers = True
    Session.flush()
    mail.mail_new_job(request,job)
        
    return {"status":"success",
                "message":None,
                "job_key":job.key}
        
            
    
@view_config(route_name="jobs_from_fasta", renderer='json')
def jobs_from_fasta(request):
    '''
    takes fasta file and spawns jobs from it.
    currently checks for 
    1. file type (.fa)
    2. fasta parse errors
    3. file size < 100,000 bytes

    but makes no guarantees that the individual jobs are good.
    '''

    filename = request.POST['fasta_file'].filename
    if not filename[-3:] == ".fa":
        raise JobERR(Job.ERR_BADFILETYPE, None)

    input_file = request.POST['fasta_file'].file
    import StringIO
    output_buffer = StringIO.StringIO()
    
    # Finally write the data to a temporary file
    input_file.seek(0)
    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_buffer.write(data)

    if output_buffer.len > 1e4:
        raise JobERR(Job.ERR_LARGEFILE, None)

    from Bio import SeqIO
    try:
        output_buffer.seek(0)
        fasta_records = [r for r in SeqIO.parse(output_buffer,"fasta")]
    except Exception,e:
        raise JobERR(Job.ERR_PARSING_FASTA,None)
        
    b = Batch(original_filename = filename,
              email = request.params["email"],
              date_submitted = datetime.datetime.utcnow(),
              genome = Job.GENOMES[request.params["genome"]],
          )
    output_buffer.seek(0)
    b.save_input_file(output_buffer)       
    Session.add(b)

    for r in fasta_records:
        sequence = str(r.seq.upper())
            
        if re.compile("[^AGTCN]").search(sequence) is not None:
            raise JobERR(Job.ERR_INVALID_CHARACTERS, None) 

        matches = webserver_db.check_genome(sequence,request.params["genome"])
        if len(matches) == 1:
            chr = matches[0]["tName"]
            start = matches[0]["tStart"]
            strand=1 if matches[0]["strand"] == "+" else -1
        else:
            chr = None
            start = None
            strand = None

        j = Job(batch = b,
                name = r.id,
                email = b.email,
                chr = chr,
                start = start,
                strand = strand,
                sequence = sequence,
                genome = Job.GENOMES[request.params["genome"]],
                email_complete=False,
                date_submitted = datetime.datetime.utcnow())

        Session.add(j)

    return {"status":"success",
            "message":None,
            "batch_key":b.key}


@view_config(route_name="job_from_spacers",renderer='json')
def job_from_spacers(request):
    spacer_lines = request.params["query"].strip().splitlines()
    spacer_row_lists = [re.compile("\s+").split(l.strip()) for l in spacer_lines]
    spacers = [dict(sequence = rl[0].upper(),
                    strand_input = rl[2] if len(rl) > 2 else "+",
                    name = rl[1] if len(rl) > 1 else None) for rl in spacer_row_lists]
    
    #checks input for strand and sequence
    for i,s in enumerate(spacers):
        if s["strand_input"] == "+":
            s["strand"] = 1
        elif s["strand_input"] == "-":
            s["strand"] = -1
        else:
            raise JobERR(Job.ERR_BADINPUT + "unrecognized character for strand ({0})".format(s["strand_input"]),None)
        
        strand = s["strand"]
        seq = s["sequence"]
        if s["strand"] == 1:
            if len(seq) != 23 or (seq[-2:] != "AG" and seq[-2:] != "GG"):
                   raise JobERR(Job.ERR_BADINPUT + " no forward strand guide found in sequence {0}: {1}"\
                                .format(i,s["sequence"]),None)
        else:
            if len(seq) != 23 or (seq[:2] != "CT" and seq[:2] != "CC"):
                   raise JobERR(Job.ERR_BADINPUT + " no reverse strand guide found in sequence {0}: {1}"\
                                .format(i,s["sequence"]),None)
                         
                   

    job_sequence = ""
    spacer_infos = []
    for i,s in enumerate(spacers):
        job_sequence += "NN"
        si = dict(name = s["name"],
                  sequence = s["sequence"],
                  position = len(job_sequence),
                  strand = s["strand"])
        if len(s["sequence"]) != 23:
            raise JobERR(Job.BADSPACER_LENGTH,None)
        spacer_infos.append(si)
        job_sequence += si["sequence"]
        job_sequence += "NN"
    

    if cfront_settings.get("debug_mode",False): print job_sequence

    
    if re.compile("[^AGTCN]").search(job_sequence) is not None:
            return {"status":"error",
                    "message":"Ambiguous or invalid characters found in input sequene.",
                    "matches":None,
                    "job_key":None}
    if len(job_sequence) > 500 :
        return {"status":"error",
                "message":"Sequence length not within allowed range (23 - 500bp)",
                "matches":None,
                "job_key":None}
    
    print "GENOME: {0}".format(request.params.get("genome","hg19"))
    
        
    if len(spacer_infos) == 0:
        raise JobERR(Job.NOSPACERS,None)
    else:
        params = dict(date_submitted = datetime.datetime.utcnow(),
                      sequence = job_sequence,
                      genome = Job.GENOMES[request.params.get("genome","hg19")],
                      name = request.params["name"],
                      email = request.params["email"],
                      twostrand = False,
                      query_type = "guides_list")

        if "key" in request.params:
            params["key"] = request.params.get("key")

        job = Job(**params)

        Session.add(job)

    for spacer_info in spacer_infos:
        Session.add(Spacer(job = job,**spacer_info))
            
    job.computed_spacers = True
    Session.flush()
    mail.mail_new_job(request,job)
        
    return {"status":"success",
                "message":None,
                "job_key":job.key}
        
    
