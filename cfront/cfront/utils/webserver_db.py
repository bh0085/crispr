from ..models import Session, Job, Hit, Spacer
import re

def compute_spacers(job_id):
    #retrieves job
    job = Session.query(Job).get(job_id)
    if job.computing_spacers or job.computed_spacers: raise Exception("already computed(ing) spacers")
    Session.add(job)

    #computes spacers
    job.computing_spacers = True
    sequence = job.sequence
    fwd = sequence
    rev = reverse_complement(sequence)
    
    expression = re.compile(".{20}[ATGC][GA][T]")
    for m in re.finditer(expression, fwd):
        Session.add(Spacer(job = job,
                           sequence = m.group(),
                           guide = m.group()[:-3],
                           nrg = m.group()[-3:],
                           strand = 1,
                           position = m.start()))
    for m in re.finditer(expression,rev):
        Session.add(Spacer(job = job,
                           sequence = m.group(),
                           guide = m.group()[:-3],
                           nrg = m.group()[-3:],
                           strand = -1,
                           position = m.start()))

    
    #marks job complete, returns status
    job.computed_spacers = True      
    Session.add(job)
    Session.flush()

    return job.computed_spacers


def reverse_complement(sequence):
    repl = {"A":"T",
            "T":"A",
            "G":"C",
            "C":"G"}
    return "".join(repl[let] for let in sequence[::-1])
    
