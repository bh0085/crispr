#!/usr/bin/env python

import argparse, os, re,time, random, csv
import simplejson as sjson
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna
from Bio.Alphabet import DNAAlphabet
import gffutils
from gffutils import biopython_integration
from time import strftime, gmtime
from numpy import array
import itertools as it
import numpy


def queue_loop():
    while True:
        print "processing"
        process_queue()
        print "sleeping"
        time.sleep(5)
       
            

tmpdir = "/fastdata/webserver/tmp"
def run_job(assembly, geneid):

    tool_regexes = {"cas9":re.compile("(?P<spacer>[ATGC]{20})(?P<pam_after>[ATGC]GG)"),
                    "cpcf1":re.compile("(?P<pam_before>TT[ATGC])(?P<spacer>[ATGC]{28})"),
                    #"cas13":re.compile("(?P<spacer>[ATGC]{28})(?P<pam_after>GCT)")
    }


    tool_guidelens = {
        "cas9":20,
        "cpcf1":31,
        #"cas13":28,
    }
    tool_pamlens = {
     
        "cas9":3,
        "cpcf1":3,
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
            seq_reverse_letters = fa_seq.reverse.seq
            
            out_status = {"complete":True}
            spacers_file = os.path.join(tmpdir,"{assembly}_{geneid}_{tool}_spacers.fa".format(assembly=assembly,geneid=geneid, tool=tool))
            spacer_regex = tool_regexes[tool]

            for i, m in enumerate(spacer_regex.finditer(seq_letters)):
                
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

            for i, g in enumerate(spacer_regex.finditer(seq_reverse_letters)):

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
            if tool =="cpcf1":
                pams_before = ["TTA","TTG", "TTC", "TTT"]
                pams_after = [""]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.1".format(assembly)
            if tool =="cas9":
                pams_before =[""]
                pams_after = ["AGG","TGG","GGG","CGG"]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.1".format(assembly)
            if tool =="cas13":
                pams_before =[""]
                pams_after = ["GGG"]
                bowtie_index ="/fastdata/bowtie/{0}.refseq.bowtie.mrnas.1".format(assembly)

                
            records = (SeqRecord(Seq(pbefore + spacer["guide_sequence"] + pafter, generic_dna), spacer["guide_id"], description =  "{0} {3}---{4} target in {1} {2}".format(tool,assembly,geneid,pbefore,pafter)) for spacer in tool_spacers for pbefore in pams_before for pafter in pams_after )
            SeqIO.write(records, tf2, "fasta")

        i
            
        outfile = "/fastdata/webserver/tmp/{0}_{1}_bowtie_hits.map".format(geneid,tool)
        print "calling subprocess"
        import subprocess
        result = subprocess.call(["bowtie", "-a", "-n", "3", "-c", "-f", "-l","{0}".format(tool_guidelens[tool]+tool_pamlens[tool]),bowtie_index, "{0}".format(tmpfile_2), "{0}".format(outfile)])
        print "completed bowtie subprocess"
        print "result: {0}".format(result)


        weights =  array([0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]);

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
                

                for k2, g2 in it.groupby(items1, key = lambda x:x["name"]):
                    items2 = list(g2)
                    print k2, len(items2)
                    
                    for e in items2:
                        pams = re.compile("(?P<pam_before>[\S]*)---(?P<pam_after>[\S]*)")\
                             .search(e["name"])
                        pam_before= pams.groupdict()["pam_before"]
                        pam_after= pams.groupdict()["pam_after"]                 
                        match_offset = 0
                        if pam_before:
                            guide_sequence = e["guide_sequence"][len(pam_before):]
                            match_offset=len(pam_before)
                        else:
                            guide_sequence = e["guide_sequence"][:-1*len(pam_after)]
                            match_offset=0

                        mismatches = numpy.zeros([len(guide_sequence)],numpy.int8)
                    

                        mms = e["mismatches"].split(",")
                        if len(mms) == 1:
                            ontarget_alignments.append(e)
                        else:
                            for m in mms:
                                og_position = int(re.compile("(?P<position>[\d]*):[ATGC]>[ATGC]").search(m).groups()[0])
                                position_in_guide = og_position-match_offset
                                if position_in_guide <0:
                                    continue
                                if position_in_guide >= len(guide_sequence):
                                    continue
                                mismatches[position_in_guide] = 1

                            score = scoring_fun(mismatches)
                            offtarget_scores += [score]
                            offtarget_alignments.append(e)
                

                
                total_score = 100*(100 / (100 + sum([s for s in offtarget_scores])))
                test_count+=1

                spacer = filter(lambda x:x["guide_id"] == guide_id, tool_spacers)[0]
                #print spacer
                spacer["offtarget_count"] = len(offtarget_alignments)
                spacer["ontarget_count"] = len(ontarget_alignments)
                spacer["score"] = total_score
                
                #print "guide_id: {0} ontgts: {1}, offtgts: {2}, score: {3}".format(guide_id, len(ontarget_alignments), len(offtarget_alignments), total_score)
                
                #if test_count > 40: break
                         
        out_data[tool]["spacers"]+=tool_spacers
            
        

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
