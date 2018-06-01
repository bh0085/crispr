#!/usr/bin/env python

import argparse, os, re,time, random, csv
import simplejson as sjson
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature,  FeatureLocation
from Bio.Alphabet import generic_dna
from Bio.Alphabet import DNAAlphabet
from Bio import Alphabet
import gffutils
from gffutils import biopython_integration
from time import strftime, gmtime
from numpy import array
import itertools as it
import numpy

import sendgrid
from sendgrid.helpers.mail import *
import base64

import shlex


def queue_loop():
    while True:
        print "processing"
        process_queue()
        print "sleeping"
        time.sleep(5)
       


def gene_genbank_spacers_data_helper(data, assembly, geneid, returntype="filename",
                                spacer_sequence_filter=None,
                                tool_filter=None,
                                min_score=90):


    
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    sf = biopython_integration.to_seqfeature(gene)
    seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))


 


    cas9_spacers = data["cas9"]["spacers"]
    cpf1_spacers = data["cas9"]["spacers"]

    
    sfs = []
    count=0
    for tool,spacer_list in {"cas9":cas9_spacers,
                             "cpf1":cpf1_spacers}.items():
        if tool_filter != None:
            if tool != tool_filter:
                continue
        for s in spacer_list:
            if spacer_sequence_filter:
                if s["guide_sequence"] != spacer_sequence_filter:
                    continue
            if min_score != None:
                
                #print s["score"]
                if s["score"] < min_score:
                    continue

            quals = {}
            if s["pam_before"]:
                quals.update({"upstream_pam":s["pam_before"]})
                
            if s["pam_after"]:
                quals.update({"downstream_pam":s["pam_after"]})

            quals.update({"score":s["score"],
                          "tool":tool,
                          "target_seq":s["guide_sequence"]})
        
                
            sfs.append(SeqFeature(FeatureLocation(s["guide_start"],
                                                  s["guide_start"]+s["guide_length"],
                                                  strand=s["guide_strand"]),
                                  id="guide{0}".format(count),
                                  qualifiers=quals,
                                  type="{0}_guide".format(tool)))
            count+=1



    
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

        

def send_email(data,assembly, geneid, email):        
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("hi@crispr.mit.edu","crispr design platform")
    to_email = Email(email)
    subject = "Your crispr query of {0} is complete!".format(geneid)
    content = Content("text/plain", """Hello--you've successfully submitted a guide search to crispr.mit.edu and your results are ready. 

To see your job's output at our online gateway, please head over to:
http://35.231.249.4:6539/v2/{0}/{1}/gene_results

We've also attached our top guide recommendations for cas9 and cpf1 targeting of {1} in genbank format to this email.

If you have any questions about job output, or for feature suggestions and important announcements, please visit our forum,
https://groups.google.com/forum/#!forum/crispr

Thanks for using crispr.mit.edu!
--the Zhang Lab

    """.format(assembly, geneid))
    mail = Mail(from_email, subject, to_email, content)
  
    attachment = Attachment()
    text=gene_genbank_spacers_data_helper(data, assembly, geneid, returntype="text",
                                          spacer_sequence_filter=None,
                                          tool_filter=None,
                                          min_score=90)


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



    
emails_dir = "/fastdata/crispr/emails"
def email_complete(assembly,geneid):

    job_filename = "{0}_{1}_data.json".format(assembly,geneid)
    
    for email in os.listdir(emails_dir):
        folderpath = os.path.join(emails_dir,email)
        for f in os.listdir(folderpath):
            if f != job_filename:
                print "skipping {0}".format(f)
                continue
            with open(os.path.join(folderpath,f)) as fopen:
                status = sjson.loads(fopen.next())
                data = sjson.loads(fopen.next())
                dates = status.get("email-dates",[])
                if len(dates) == 0:
                    send_email(data, assembly, geneid, email)
                status["dates"] = dates
                
                
            with open(os.path.join(folderpath,f),"w") as fopen:
                fopen.writelines([sjson.dumps(status)+"\n",sjson.dumps(data)+"\n"])
                
    

 
tmpdir = "/fastdata/webserver/tmp"
def run_job(assembly, geneid):

    tool_regexes = {"cas9":re.compile("(?P<spacer>[ATGC]{20})(?P<pam_after>[ATGC]GG)"),
                    "cpf1":re.compile("(?P<pam_before>TT[ATGC])(?P<spacer>[ATGC]{31})"),
                    #"cas13":re.compile("(?P<spacer>[ATGC]{28})(?P<pam_after>GCT)")
    }


    tool_guidelens = {
        "cas9":20,
        "cpf1":31,
        #"cas13":28,
    }
    tool_pamlens = {
     
        "cas9":3,
        "cpf1":3,
       #"cas13":3,   
    }
    
    db = gffutils.FeatureDB('/fastdata/zlab-genomes/gffutils/{0}.db'.format(assembly), keep_order=True)
    gene = db[geneid]
    out_data={}

    search_features = []
    cds = list(db.children(gene,featuretype="CDS",order_by="start"))[::-1]
    
    current=cds.pop()
    current_start = current.start
    current_end = current.end
    intervals=[]
    
    while cds:
        n = cds.pop()
        if n.start <=current_end:
            current_end = max(n.end,current_end)
        else:
            intervals.append({"start":current_start,
                              "end":current_end})
            current_start = n.start
            current_end = n.end
                          
    complete_fwd_seq_letters = gene.sequence("/fastdata/refseq/{0}.refseq.fa".format(assembly))
    fwd_seq = Seq(complete_fwd_seq_letters, DNAAlphabet())
    rev_seq = fwd_seq.reverse_complement()
    complete_rev_seq_letters = str(rev_seq)

    
    
    
    count = 0
    for tool in tool_regexes.keys():
        out_data[tool] = {}
        out_data[tool]["spacers"] = []
        out_data[tool]["search_regions"] = []
        
        tool_spacers = []   
        
        for region in intervals:
            start = region["start"]
            end=region["end"]
            chrom=gene.chrom
 
            from pyfaidx import Fasta
            genes = Fasta("/fastdata/refseq/{0}.refseq.fa".format(assembly))
            fa_seq = genes[chrom][start:end]
                                          
            region_dict = {"start":start,
                           "end":end,
                           "chrom":chrom,
                           "name":fa_seq.fancy_name}
            out_data[tool]["search_regions"].append(region_dict)       



            seq_letters = fa_seq.seq
            seq_reverse_letters = fa_seq.reverse.complement.seq
            
            out_status = {"complete":True}
            spacers_file = os.path.join(tmpdir,"{assembly}_{geneid}_{tool}_spacers.fa".format(assembly=assembly,geneid=geneid, tool=tool))
            spacer_regex = tool_regexes[tool]

            for i, m in enumerate(spacer_regex.finditer(seq_letters)):

                #continue
                guide_seq = m.groupdict()["spacer"]
                this_spacer_regex = re.compile(guide_seq)
                genic_hits = len(this_spacer_regex.findall(complete_fwd_seq_letters)) + len(this_spacer_regex.findall(complete_rev_seq_letters))
                if genic_hits > 1:
                    print "skipping guide for multiple hits ({0}) on this locus, {1}".format(genic_hits, guide_seq)
                    continue
                
                tool_spacers +=[{
                    "guide_strand":1,
                    "guide_start":m.start() + len(m.groupdict().get("pam_before","")),
                    "guide_length":len(m.groupdict()["spacer"]),
                    "guide_sequence":m.groupdict()["spacer"],
                    "pam_after":m.groupdict().get("pam_after",None),
                    "pam_before":m.groupdict().get("pam_before",None),
                    "guide_id":"{0}_g{1}".format(geneid,count),
                    "region_start":start,
                    "tool":tool}]
                count+=1

            for i, m in enumerate(spacer_regex.finditer(seq_reverse_letters)):

                #continue
                guide_seq = m.groupdict()["spacer"]
                this_spacer_regex = re.compile(guide_seq)
                genic_hits = len(this_spacer_regex.findall(complete_fwd_seq_letters)) + len(this_spacer_regex.findall(complete_rev_seq_letters))
                if genic_hits > 1:
                    print "skipping guide for multiple hits ({0}) on this locus, {1}".format(genic_hits, guide_seq)
                    continue
                
                
                tool_spacers += [{
                    "guide_strand":-1,
                    "guide_start":len(seq_letters) - m.span()[1] +len(m.groupdict().get("pam_after","")),
                    "guide_length":len(m.groupdict()["spacer"]),
                    "guide_sequence":m.groupdict()["spacer"],
                    "pam_after":m.groupdict().get("pam_after",None),
                    "pam_before":m.groupdict().get("pam_before",None),
                    "guide_id":"{0}_g{1}".format(geneid,count),
                    "region_start":start,
                    "tool":tool}]

                count+= 1
        
        tmpfile_2 = "/fastdata/webserver/tmp/{0}_{1}_pam_feature_spacers.fa".format(geneid,tool)
        with open(tmpfile_2, "w") as tf2:
            if tool =="cpf1":
                pams_before = ["TTA","TTG", "TTC", "TTT"]
                pams_after = [""]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.1".format(assembly)
                weights = numpy.ones(28);
            if tool =="cas9":
                pams_before =[""]
                pams_after = ["AGG","TGG","GGG","CGG"]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.1".format(assembly)
                weights =  array([0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]);

            if tool =="cas13":
                pams_before =[""]
                pams_after = ["GGG"]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.mrnas.1".format(assembly)

            records = (SeqRecord(Seq(pbefore + spacer["guide_sequence"] + pafter, generic_dna), spacer["guide_id"], description =  "{0} {3}---{4} target in {1} {2}".format(tool,assembly,geneid,pbefore,pafter)) for spacer in tool_spacers for pbefore in pams_before for pafter in pams_after )
            SeqIO.write(records, tf2, "fasta")


            
        outfile = "/fastdata/webserver/tmp/{0}_{1}_bowtie_hits.map".format(geneid,tool)
        import subprocess

    
        cmd = " ".join(["bowtie","{0}".format(bowtie_index) ,"-a", "-f", "-v", "3", "{0}".format(tmpfile_2), "{0}".format(outfile)])
        proc = subprocess.Popen(shlex.split(cmd))
        print "the commandline is %s" % cmd
        proc.wait()
        
        #result = subprocess.call()



        def scoring_fun(mismatches):
            if len(mismatches) == 0:
                score = 100
            else:
                score = 100 * (1 - weights[mismatches]).prod()
                if len(mismatches) > 1:
                    mean_pairwise =float(sum(mismatches[1:] - mismatches[:-1])) / (len(mismatches)-1)
                    mpw_factor = ((float((19-mean_pairwise))/19)*4 + 1)
                    scl_factor = pow(len(mismatches),2)

                    score  = score / ( mpw_factor * scl_factor )
                    score = max([score,0])
            return score

        cols =["name","strand","chrom","start","guide_sequence","qualities","ceiling","mismatches"]
        test_count=0
        guide_id_regex = re.compile("^(?P<guide_id>[^_]*_[\S]*)")


        output_spacers = []
        #looks through output file for all unique spacer guide sequenes
        #groups together pam sequence wild cards
        with open(outfile) as of:
            for k1, g1 in it.groupby([ dict(zip(cols,l)) for l in csv.reader(of,delimiter="\t")],
                                    key = lambda x:guide_id_regex.search(x["name"]).groups()[0]):
                items1 = list(g1)
                offtarget_scores = []
                offtarget_alignments =[]
                ontarget_alignments =[]
                guide_id=k1

                if len(items1) > 1000:
                    spacer = filter(lambda x:x["guide_id"] == guide_id, tool_spacers)[0]
                    spacer["offtarget_count"] = len(items1)
                    spacer["ontarget_count"] = 1
                    spacer["score"] = 0
                    continue
                
                #breaks apart groups by pam sequence wild card matches
                #discards all pam mismatches
                for k2, g2 in it.groupby(items1, key = lambda x:x["name"]):
                    items2 = list(g2)                    
                    for e in items2:
                        pams = re.compile("(?P<pam_before>[\S]*)---(?P<pam_after>[\S]*)")\
                             .search(e["name"])
                        pam_before= pams.groupdict()["pam_before"]
                        pam_after= pams.groupdict()["pam_after"]                 
                        match_offset = 0
                        if pam_before:
                            guide_sequence = e["guide_sequence"][len(pam_before):]
                            guide_match = e["guide_sequence"][0:len(pam_before)]
                            if guide_match != pam_before:
                                continue
                            match_offset=len(pam_before)
                        elif pam_after:
                            guide_sequence = e["guide_sequence"][:-1*len(pam_after)]
                            guide_match = e["guide_sequence"][-1*len(pam_after):]

                            if guide_match != pam_after:
                                continue
                            match_offset=0
                        else:
                            raise Exception("case of no guide sequences not yet implemented")


                            
                        mismatches = numpy.zeros([len(guide_sequence)],numpy.int8)
                    
                        mms = e["mismatches"].split(",")
                        n_mms =  len([m for m in mms if m.strip() != ""])
                        
                        markbad = False
                        if n_mms == 0:
                            ontarget_alignments.append(e)
                            continue
                        else:
                            for m in mms:
                                og_position = int(re.compile("(?P<position>[\d]*):[ATGC]>[ATGC]").search(m).groups()[0])
                                position_in_guide = og_position-match_offset
                                if position_in_guide <0:
                                    markbad=True
                                    continue
                                if position_in_guide >= len(guide_sequence):
                                    markbad=True
                                    continue
                                
                                mismatches[position_in_guide] = 1
                                
                                
                        if markbad: continue
                        score = scoring_fun(mismatches)
                        offtarget_scores += [score]
                        offtarget_alignments.append(e)


                
                total_score = 100*(100 / (100 + sum([s for s in offtarget_scores])))
                test_count+=1

                spacer = filter(lambda x:x["guide_id"] == guide_id, tool_spacers)[0]
                
                spacer["offtarget_count"] = len(offtarget_alignments)
                spacer["ontarget_count"] = len(ontarget_alignments)
                spacer["offtarget_alignments"] = offtarget_alignments
                spacer["score"] = total_score
                output_spacers.append(spacer)
                
                                         
        out_data[tool]["spacers"]+=output_spacers
            
        

    return out_status, out_data
        
    
        
        
gene_queries_directory = "/fastdata/crispr/gene_queries"
emails_directory = "/fastdata/crispr/emails"
def process_queue(reset = False):
    for f in os.listdir(gene_queries_directory):
        do_run_job = reset
        
        with open(os.path.join(gene_queries_directory,f)) as fopen:
            if not do_run_job:
                try:
                    l0 = fopen.next()
                    if not l0:
                        do_run_job = True
                    else:
                        status_line = sjson.loads(l0.rstrip())
                    
                        if not status_line.get("complete",False):
                            do_run_job = True
                except StopIteration as e:
                    do_run_job = True

        if do_run_job:

            with open(os.path.join(gene_queries_directory,f), "w") as fopen:
                match = re.compile("(?P<assembly>[^_]*)_(?P<geneid>[^_]*)").search(f)
                assembly = match.groupdict()["assembly"]
                geneid = match.groupdict()["geneid"]
                print "running job for {0} / {1} at time {2}".format(assembly,geneid,strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

                status, data = run_job(assembly,geneid)
                fopen.writelines([sjson.dumps(status)+"\n",sjson.dumps(data)+"\n"])
                print "done! output at: \n{0}".format(os.path.join(gene_queries_directory,f))
        
            print "sending email"
            email_complete(assembly, geneid)
            print "done sending email!"
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset','-r',dest="reset",
                        default=False, const = True , action="store_const",
                        help = "resets all jobs")
    parser.add_argument('--noloop', '-n',dest="noloop",
                        default=False, const = True, action="store_const")
    args = parser.parse_args()

    if args.noloop:
        process_queue(reset = args.reset)
    else:
        queue_loop()
        

if __name__ == "__main__":
    main()
