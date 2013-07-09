#!/usr/bin/env python
import argparse, subprocess as spc, os, StringIO
from Bio import SeqIO as sio

#ROOT = os.environ["HOME"]
DATAPATH = os.environ["CFRONTDATA"]
JOBSPATH = os.path.join(DATAPATH,"jobs")
if not os.path.isdir(JOBSPATH):
    os.makedirs(JOBSPATH)


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
    
    args = parser.parse_args()
    
    cmd = "bowtie -n 2 -l 15 -c hg19 {0} --quiet -a".format(args.query)

    prc = spc.Popen(cmd, shell=True, cwd="/tmp/ramdisk/bowtie-indexes",
              stdout = spc.PIPE)
    outs = prc.stdout.readlines()
    rows = [dict(zip(["query_id","strand","chr","position","sequence","alignment","mismatch","mistmatch_pos"] , l.split("\t") )) for l in outs]


    contexts = []
    regions =["{0}:{1}-{2}".format(r["chr"],int(r["position"])+1-5,int(r["position"])+23-5) for r in rows]
    for i in range(1+ (len(regions)/50) ):
        regions_str = " ".join(regions[50*i:50*(i+1)])
        if regions_str != "":
            regions_cmd = "samtools faidx hg19.fa {0}".format(regions_str)
            prc = spc.Popen(regions_cmd,shell=True,cwd="/tmp/ramdisk/bowtie-indexes",
                            stdout=spc.PIPE)
            contexts += [ str(e.seq) for e in sio.parse(StringIO.StringIO(prc.stdout.read()),"fasta")]
    

    for i,r in enumerate(rows):
        r["sequence"] = contexts[i][:-3].upper()
        r["nrg"] = contexts[i][-3:].upper()
        r["context"] = contexts[i].upper()
        r["chr"] = r["chr"][3:]

    print len(rows[0]["sequence"])
        
    rows = [r for r in rows if r["nrg"][-2:] == "AG" or r["nrg"][-2:] == "GG"]

        
    cols = ["sequence","chr", "position", "strand","nrg"]
    job_path = os.path.join(JOBSPATH,args.job_id)
    if not os.path.isdir(job_path):
        os.makedirs(job_path)
        
    

    with open(os.path.join(job_path, "matches_s{0}.txt".format(args.spacer_id)),'w') as f:
        f.write("\n".join(["\t".join([o[c] for c in cols]) for o in rows]))
        


if __name__ == "__main__":
    main()
