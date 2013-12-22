#computes all possible nickase offtargets between the spacers in a job.

from ..models import Session, Job, Spacer, Hit
def compute_nickase_matrix(jobid):
    job = Session.query(Job).get(jobid)
    spacers = job.spacers
    
    nicks = []
    nick_id_counter = 0
    for i in range(len(spacers)):
        for j in range(i):
            nick_id_counter ++;
            nicks.append(Nick(nick_id_counter, 
                              spacers[i],
                              spacers[j]))

    return nicks
    

class Nick(object):
    def __init__(self,id,spacer1,spacer2):
        self.spacer1 = spacer1
        self.spacer2 = spacer2

        #HOW DO WE EXCLUDE THE ONTARGET HITS?
        #LETS JUST USE THE ONTARGET FLAG... 
        #WILL ADD!
        self.hit_pairs =  [[h1, h2] for h1 in spacer1.hits for h2 in spacer2.hits if h1.chr == h2.chr and abs(h1.start - h2.start) < 500]
        self.individual_scores = [e[0].score * e[1].score for e in self.hit_pairs]
        self.score = 100 / (100 + sum([s.score for s in self.individual_scores]))
        
        
