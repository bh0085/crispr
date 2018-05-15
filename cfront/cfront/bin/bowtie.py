#!/usr/bin/env python
import argparse, subprocess as spc, os, StringIO
from Bio import SeqIO as sio, Seq, SeqRecord
import random
import twobitreader
from cfront import cfront_settings

#ROOT = os.environ["HOME"]
DATAPATH = os.environ["CFRONTDATA"]

TMPPATH = "/fastadata/bowtie"
if not os.path.isdir(TMPPATH):
    os.makedirs(TMPPATH)
GENOMEPATH = "/fastdata/genomes/"

def run_queries(queries, genome):

    tmpfile_in = os.path.join(TMPPATH,"tmpfile_{0}.fa".format(int(random.random() * 1e10)))
    tmpfile_out = os.path.join(TMPPATH,"tmpfile_{0}.out".format(int(random.random() * 1e10)))
        
    records = []
    for i,q in enumerate(queries):
        if len(q) != 20:
            raise Exception("demands queries of length 20")
        
        records.extend([SeqRecord.SeqRecord(Seq.Seq( q[5:] + n + r + "G"), 
                                            id="query_{0}".format(i),
                                            description="")  
                        for n in "ATGC" for r in "GA"])

    with open(tmpfile_in,'w') as f:
        f.writelines([r.format("fasta") for r in records])

        
    if genome=="HUMAN":
        genome_string = "hg19"
    elif genome=="MOUSE":
        genome_string = "mm9"
    else:
        raise Exception("NO SUCH GENOME {0}".format(genome))

    GENOME2BIT = os.path.join(GENOMEPATH,"{0}.2bit".format(genome_string))

    #cmd = "bowtie -n 3 -l 18 {2} -f {0} --quiet -a {1}".format(tmpfile_in,tmpfile_out)
    cmd = "bowtie -n 2 -l 18 {2} -f {0} --quiet -a {1}".format(tmpfile_in,tmpfile_out,genome_string)
    prc = spc.Popen(cmd, shell=True, cwd="/fastadata/bowtie-indexes")
    prc.communicate()

    with open(tmpfile_out) as f:
        lines = f.readlines()
        
    os.remove(tmpfile_in)
    os.remove(tmpfile_out)

    rows = [dict(zip(["query_id","strand","chr","position","sequence","alignment","mismatch","mistmatch_pos"] , l.split("\t") )) for l in lines]


    tbf = twobitreader.TwoBitFile(GENOME2BIT)


    out,regions = [],set()
    for i,r in enumerate(rows):
    
        if r["strand"] == "+":
            start =int( r["position"])  - 5
            end =int( r["position"]) + 23 - 5
            context = tbf[r["chr"]][start:end]
        else:
            start = int(r["position"]) 
            end = int(r["position"]) + 23 
            context = reverse_complement(tbf[r["chr"]][start:end])
                                    
        region = "{0}:{1}-{2}{3}".format(r["chr"],
                                         start,
                                         end,
                                         r["strand"])
        if region in regions:
            continue
        regions.add(region)
        
        r["position"] = start + 1 # converts back to zero basis
        r["sequence"] = context[:-3].upper()
        r["nrg"] = context[-3:].upper()
        r["context"] = context.upper()
        r["chr"] = r["chr"]
        
        if r["nrg"][-2:] == "AG" or r["nrg"][-2:] == "GG":
            out.append(r)

    return out

def reverse_complement(seq):
    comp = {"A":"T",
            "G":"C",
            "C":"G",
            "T":"A",
            "N":"N"}
    return "".join(comp[l.upper()] for l in seq[::-1])

def main():
    '''
    uses bowtie to grab all hits in the human genome for a query
    '''

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--jobid','-j',dest="job_id",
                        default="1",type=str,
                        help="job_id for this job")
    parser.add_argument('--spacerid','-s',dest="spacer_id",
                        default="1",type=str,
                        help="spacer_id for this job")
    parser.add_argument('--query','-q',dest="query",
                        type=str, required=True,
                        help="query input sequence")
    parser.add_argument('--jobspath','-p',dest="jobspath",
                        type=str,required=True,
                        help="root path for job files IO")
    parser.add_argument('--genome', '-g', dest="genome",
                        type=str, required=True)
    
    args = parser.parse_args()
    query =args.query
    JOBSPATH = args.jobspath

    job_path = os.path.join(JOBSPATH,args.job_id)
    if not os.path.isdir(job_path):
        os.makedirs(job_path)
        
    match_file = os.path.join(job_path, "matches_s{0}.txt".format(args.spacer_id))
    rows = run_queries([query],args.genome)
    cols = [ "sequence","chr", "position", "strand","nrg"]
    with open(match_file,'w') as f:
        f.write("\n".join(["\t".join(["{0}".format(args.spacer_id)] + [str(o[c]) for c in cols]) for o in rows]))
    print "writing " + match_file

if __name__ == "__main__":
    main()
