#computes all possible nickase offtargets between the spacers in a job.

from ..models import Session, Job, Spacer, Hit
def compute_nickase_matrix(jobid):
    job = Session.query(Job).get(jobid)
    sorted_spacers = sorted(job.spacers, key = lambda x:x.id)
    
    #precompute possibly matching hits by chromosome
    all_hits = [h for s in sorted_spacers for h in s.hits]
    hits_by_chr = {}
    for h in all_hits:
        if not h.chr in hits_by_chr: hits_by_chr[h.chr] = []
        hits_by_chr[h.chr].append(h)


    nicks = {}
    nick_id_counter = 0
    for i in range(len(sorted_spacers)):
        for j in range(i+1):
            #NOTE j < i so all keys are ordered as nicks[j,i] w/ j < i
            nick_id_counter+=1;
            #MAKE SURE THAT WE'RE NOT NICKING THE SAME STRAND
            
            if sorted_spacers[i].strand != sorted_spacers[j].strand:
                top_spacer = sorted_spacers[i] if sorted_spacers[i].strand == 1 else sorted_spacers[j]
                bottom_spacer = sorted_spacers[i] if sorted_spacers[i].strand == -1 else sorted_spacers[j]
                offset = (top_spacer.start ) - (bottom_spacer.start + 23) 
                
                if offset > 0 and offset < 31:
                    nicks[(sorted_spacers[j].id,
                           sorted_spacers[i].id)] = Nick(nick_id_counter, 
                                                         sorted_spacers[j],
                                                         sorted_spacers[i])



    global dist_cutoff
    #not sure if we should really be using the "start"s here.
    #also, how do we handle reversed spacers
    loops = 0
    hits = 0
    for k,v in hits_by_chr.iteritems():
        hsrt = sorted(v, key = lambda x:x.start)
        for i,e in enumerate(hsrt):
            for j in range(i+1, len(hsrt)):
                loops += 1

                if abs(hsrt[j].start - hsrt[i].start) > dist_cutoff:
                    break
                else:
                    hits+=1
                    h1 = hsrt[i]
                    h2 = hsrt[j]
                    if nicks.get((h1.spacer.id,h2.spacer.id),False):
                        nicks.get((h1.spacer.id,h2.spacer.id)).add_pair(h1,h2)
                    elif nicks.get((h2.spacer.id,h1.spacer.id),False):
                        nicks.get((h2.spacer.id,h1.spacer.id)).add_pair(h1,h2)
                    else:
                        pass

    print "LOOPS {0} ".format(loops)
    print "hits {0} ".format(hits)
        
    for n in nicks.values():
        n.compute_score()
        
    return nicks.values()

dist_cutoff = 500
    
def is_double_hit(h1,h2):
    global dist_cutoff
    if h1.chr != h2.chr: return False
    if abs(h1.start - h2.start) > dist_cutoff: return False
    return True
    

def compute_nick_of_spacers(id, sfwd,srev):
    n = Nick(id,sfwd,srev)
    for h1 in sfwd.hits:
        for h2 in srev.hits:
            if h2.chr == h1.chr:
                if is_double_hit(h1,h2): n.add_pair(h1,h2)
    n.compute_score()
    return n

                    
    

class Nick(object):
    def __init__(self,id,spacer1,spacer2):
        #CORRECTS SPACER STRANDS SO THAT SPACER1 is ALWAYS FORWARD
        self.spacer1 = spacer1 if spacer1.strand ==1 else spacer2
        self.spacer2 = spacer2 if spacer1.strand ==1 else spacer1
        self.id = id
        self.hit_pairs =[]
        self.individual_scores = None
        self.score = None
        self.job = spacer1.job
    
    def add_pair(self, h1,h2):
        self.hit_pairs.append([h1,h2])

    def compute_score(self):
        h1_on = [h1 for h1 in self.spacer1.hits if h1.ontarget]
        h2_on = [h2 for h2 in self.spacer2.hits if h2.ontarget]
        if len(h1_on) == 1 and len(h2_on) == 1:
            score_constant = self.spacer1.score * self.spacer2.score
            self.individual_scores = [self.ot_hit_score(e[0],e[1]) 
                                      for e in self.hit_pairs 
                                      if not e[0].ontarget and not e[1].ontarget]

            ##IMPLEMENTS A COMPLETELY TRIVIAL SCORING SYSTEM
            ##PENALTY OF 100 FOR ALL GUIDES WITH MISMATCHES OF ANY KIND
            self.unorm_score = 100 * 100 / (100. + sum([100 for s in self.individual_scores]))
            self.score = score_constant * self.unorm_score
        else:
            self.unorm_score = 0
            self.score = 0
            
    def ot_hit_score(self, h1, h2):
        return h1.score * h2.score
        

    def toJSON(self):
        return {"n_genic_offtargets":\
                len( [(h1,h2) \
                      for h1,h2 in self.hit_pairs \
                      if (h1.gene is not None or h2.gene is not None) \
                      and (not h1.ontarget and  not h2.ontarget)]),
                "n_offtargets": \
                len([(h1,h2) for h1,h2 in self.hit_pairs if (not h1.ontarget and not h2.ontarget)]),
                "score":self.score,
                
                "unorm_score":self.unorm_score,
                "spacerfwdid":self.spacer1.id,
                "spacerrevid":self.spacer2.id,
                "id":self.id,
                "job":self.job.id
    }

        
