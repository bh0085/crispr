

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
    
    cmd = "bowtie -n 3 -l 15 -c hg19 {0} --quiet -a".format(args.query)
    spc.Popen(cmd, shell=True, cwd="/tmp/ramdrive/bowtie-indexes/hg19.ebwt",
              stdout = spc.PIPE)
    outs = spc.stdout.read()
    rows = [dict(zip(["query_id","strand","chr","position","sequence","alignment","mismatch","mistmatch_pos"],"\t".split(l)]) for l in out.splitlines()]
    
    for r in rows:
        rows["sequence"] += "GGGGG"
        rows["nrg"] = "CAG"
        
    cols = ["sequence","chr", "start", "strand","nrg"]
    with open(os.path.join(job_path, "matches_s{0}.txt".format(spacer_id)),'w') as f:
        f.write("\n".join(["\t".join([o[c] for c in cols]) for o in outs])
        


if __name__ == "__main__":
    main()
