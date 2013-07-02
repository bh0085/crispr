'''tools that interact with big db on zlab's computational server'''
import subprocess as spc, os

def get_job_path(job_id):
    return  os.path.join(os.environ["CFRONTDATA"],"jobs/{0}").format(job_id)

def submit_find_query_demo(query):
    query_demo = "GAAAACTTGGTCTCTAAATG"
    job_id = "sample"
    return {"status":"RUN","job_id":job_id}

def submit_find_query(query):
    prc = spc.Popen("submit_query.py -l .5 -t loci1kt",
                    stdin = spc.PIPE,
                    stdout= spc.PIPE,
                    shell=True)
    formatted_query = "{0}".format(query)
    prc.stdin.write(formatted_query)
    prc.stdin.close()
    job_id=prc.stdout.readline()
    return {"status":"RUN", "job_id":job_id}

def check_find_query(job_id):
    p = get_job_path(job_id)
    done = "summary.txt" in os.listdir(p)
    failed = "failed" in os.listdir(p)
    if done:
        return "DONE"
    elif failed:
        return "FAILED"
    else:
        return "RUN"

def retrieve_find_query(job_id):
    p = os.path.join(get_job_path(job_id),"matches.txt")
    cols = ["sequence", "similarity"]
    with open(p) as f:
        hits = [dict([[ cols[i], e] for i,e in enumerate(r.strip().split("\t"))]) for r in f.readlines()]
    return hits
    
