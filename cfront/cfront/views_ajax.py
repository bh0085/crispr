from pyramid.view import view_config
from .utils import webserver_db, genome_db, mail
from .models import Session, Job, Hit, Spacer
import datetime, re


@view_config(route_name='job_check_spacers', renderer='json')
def job_check_spacers(request):
    return request.job.computed_spacers

@view_config(route_name='spacer_check_hits', renderer='json')
def spacer_check_hits(request):
    spacer_id =  request.matchdict['spacer_id']
    spacer = Session.query(Spacer).get(spacer_id)
    return spacer.computed_hits

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
    sequence = request.params["sequence"].upper()
    sequence = re.sub("\s","",sequence)
    print sequence
    if re.compile("[^AGTC]").search(sequence) is not None:
            return {"status":"error",
                    "message":"Ambiguous or invalid characters found in input sequene.",
                    "matches":None,
                    "job_key":None}
    if len(sequence)<23 :
        return {"status":"error",
                "message":"Sequence length not within allowed range (23 - 500bp)",
                "matches":None,
                "job_key":None}
    
    matches = webserver_db.check_genome(sequence)
    infos = webserver_db.compute_spacers(sequence)

    if matches == None:
            return {"status":"error",
                    "message":"No matches found in the human genome (hg19). Please try a new query.",
                    "matches":None,
                    "job_key":None}
    elif len(matches) > 1:
            return {"status":"error",
                    "message":"More than one unique match found in the human genome (hg19). Please try a unique query.",
                    "matches":matches,
                    "job_key":None}
    elif len(infos) == 0:
            return {"status":"error",
                    "message":"No spacers (20nt followed by the PAM sequence NRG) in the input sequence. Please try a new query.",
                    "matches":matches,
                    "job_key":None}
    else:
            job = Job(date_submitted = datetime.datetime.utcnow(),
                      sequence = request.params["sequence"],
                      genome = Job.GENOMES["HUMAN"],
                      name = request.params["name"],
                      email = request.params["email"],
                      date_completed = None,
                      chr=matches[0]["tName"],
                      start=matches[0]["tStart"],
                      strand=1 if matches[0]["strand"] == "+" else -1
            )

            Session.add(job)

    for spacer_info in infos:
        Session.add(Spacer(job = job,**spacer_info))
            
    job.computed_spacers = True
    Session.flush()
    mail.mail_new_job(request,job)
        
    return {"status":"success",
                "message":None,
                "matches":matches,
                "job_key":job.key}
        
            
    
