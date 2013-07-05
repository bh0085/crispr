from ..models import Session, Job, Hit, Spacer

def identify_spacers(job_id):
    job = Session.query(Job).get(job_id)
    raise Exception("not yet implemented")
