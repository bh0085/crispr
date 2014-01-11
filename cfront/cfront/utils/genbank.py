#helper functions to format genbank files from various objects
from ..models import Session, Job, Spacer, Hit
import nickase
import json                                
from Bio import SeqFeature, SeqRecord, Seq

def all_nicks_to_GB(jobid):
    job = Session.query(Job).get(jobid)
    gb_seq = Seq.Seq(job.sequence,alphabet=Seq.Alphabet.DNAAlphabet())
    
    description = """double nickase analysis for job "{0}" submitted by "{1}", with URL: crispr.mit.edu/{2}""".format(job.name, job.email, job.key)

    seq_record = SeqRecord.SeqRecord(gb_seq, id=job.key , name = job.genome_name , 
                                     description=description)
    
    nicks = nickase.compute_nickase_matrix(jobid)
    for n in nicks:
        sf = n.spacer1
        sr = n.spacer2
        
        span_left = min(sf.cut_site, sr.cut_site)
        span_right = max(sf.cut_site, sr.cut_site)
        
        #in the genbank file, "FWD GUIDE" refers to the guide with FWD strand PAM
        qualifiers = {
            "note":"DS-break overhang",
            "fwd_guide_cuts":sf.cut_site,
            "fwd_guide_id":sf.id,
            "fwd_guide_score":sf.formatted_score,
            "fwd_guide_n_offtargets":sf.n_offtargets,
            "rev_guide_cuts":sr.cut_site,
            "rev_guide_id":sr.id,
            "rev_guide_score":sr.formatted_score,
            "rev_guide_n_offtargets":sf.n_offtargets
        }
        seq_record.features.append( 
            SeqFeature.SeqFeature(location = SeqFeature.FeatureLocation(span_left, span_right), 
                                  qualifiers = qualifiers,
                                  type="misc_feature"))

    return seq_record.format("genbank")

def one_nick_to_GB(job, sfwd, srev):
    gb_seq = Seq.Seq(job.sequence,
                     alphabet = Seq.Alphabet.DNAAlphabet())

    
    span_left = min(sfwd.cut_site, srev.cut_site)
    span_right = max(sfwd.cut_site, srev.cut_site)

    description = """double nickase analysis for job "{0}" a pair of guides nicking the query input at +{1} bp and -{2} bp""".format(job.name, srev.cut_site, sfwd.cut_site)
    
    seq_record = SeqRecord.SeqRecord(gb_seq, 
                                     id = job.key, 
                                     name = job.genome_name,
                                     description = description)


    seq_record.features.append(  SeqFeature.SeqFeature( 
        location= SeqFeature.FeatureLocation(span_left, span_right), 
        qualifiers = {"note":json.dumps({"guide_fwd_score":sfwd.score,
                                         "guide_rev_score":srev.score})},
        type="misc_feature"))

    seq_record.features.append( SeqFeature.SeqFeature(
        location = SeqFeature.FeatureLocation(sfwd.start,sfwd.start+23),
        type="protein_bind",
        qualifiers={
            "bound_moiety":"forward guide",
            "note":json.dumps(dict(score = sfwd.formatted_score))
        }
    ))
    
    seq_record.features.append( SeqFeature.SeqFeature(
        location = SeqFeature.FeatureLocation(srev.start,srev.start+23),
        type="protein_bind",
        qualifiers={
            "bound_moiety":"reverse guide",
            "note":json.dumps(dict(score = srev.formatted_score))
        }
    ))
    
    

    nick = nickase.compute_nick_of_spacers(-1,sfwd,srev)
    #for hp in nick.hit_pairs:
    #    qualifiers = {
    #        "score":nick.ot_hit_score(hp[0],hp[1])
    #    }
    #    
    #    seq_record.features.append( 
    #        SeqFeature.SeqFeature( 
    #            location= SeqFeature.FeatureLocation(span_left, span_right), 
    #            qualifiers = {"spacer1_score":}))
    nick.compute_score()
                     
    return seq_record.format("genbank")


def one_spacer_to_CSV(job,spacer):
    return "\n".join(
        ["chr, strand, position, sequence, n_mismatches, score, ontarget, gene"] + 
        [ ", ".join(["{0}".format(e2) for e2 in [e.chr,e.strand,e.start,e.sequence,e.n_mismatches,e.score, e.ontarget, e.gene]]) 
                       for e in sorted(spacer.hits, key = lambda x:-1*x.score)])
