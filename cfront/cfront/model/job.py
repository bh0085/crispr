from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base
import calendar, os, random, re
from sqlalchemy.types import VARCHAR


class Job(Base):
    __tablename__ = 'job'
    
    #pkey
    id = Column(BigInteger, primary_key = True)

    #nonnull
    sequence = Column(Unicode, nullable = False)
    date_submitted = Column(DateTime, nullable = False)
    genome = Column(Integer, nullable = False)

    #nullable
    name = Column(Unicode, nullable = True)
    email = Column(Unicode, nullable = True)
    date_completed = Column(DateTime, nullable = True)
    query_type = Column(Unicode, nullable = True)

    computed_spacers = Column(Boolean, nullable = False, default = False)

    #error handling for offtargets
    failed = Column(Boolean, nullable = False, default = False)
    date_failed = Column(DateTime, nullable = True)
    error_traceback = Column(Unicode, nullable = True)
    error_message = Column(Unicode, nullable = True)

    #v0 maps to exactly one site on the genome
    chr = Column(VARCHAR(6), nullable = True)
    start = Column(BigInteger, nullable = True)
    strand = Column(Integer, nullable = True)
    twostrand = Column(Boolean, default = True, nullable = False)

    #messaging for offtargets
    files_computing = Column(Boolean, nullable = False, default = False)
    files_ready = Column(Boolean, nullable = False, default = False)
    files_failed = Column(Boolean, nullable = False, default = False)
    email_complete = Column(Boolean, nullable = False, default = False)
    key = Column(String, nullable = False, index = True, unique = True)
    batchid = Column(BigInteger, ForeignKey("batch.id"), nullable = True)

    #fake enum type for genomes
    GENOMES={
        "hg38":1,
        "mm10":2,
        "rn5":3,
        "danRer11":4,
        "ce10":5,
        "dm6":6,
        "susScr11":7,
        "oryCun2":8,
        "monDom5":9,
    }

    ERR_BADINPUT = "Problem with query input: "
    ERR_INVALID_CHARACTERS = "Invalid characters in submission, please restrict query input to sequences including A, T, G, or C"
    ERR_LARGEFILE = "Please submit a smaller file. As of 9/10/2013 we're limiting filesizes to <10kb to reduce load on the alpha server. Look for increased limits in the future!"

    ERR_UNIMPLEMENTED = "Batch submit from .fa files is not yet implemented."
    ERR_BADFILETYPE = "Please input a fasta file (.fa)."
    ERR_PARSING_FASTA = "Could not parse fasta file."
    ERR_NOGENOME = "No matches found in the target genome. Please try a new query."
    ERR_MULTIPLE_GENOME = "More than one unique match found in the target genome. Please try a unique query."
    
    #exceptions
    NOSPACERSYET = "spacers not yet computed"
    NOSPACERS = "No spacers (20nt followed by the PAM sequence NRG) in the input sequence. Please try a new query."
    NOHITS = "hits not yet computed"
    ERR_TOOMANY = "too many spacers in a single alignment. right now does 1 at a time"
    ERR_MISSING = "no spacers in bowtie alignment"
    ERR_ALREADYCOMPUTED = "already computed hits"
    ERR_MULTIPLE_ONTARGETS = "found multiple exact hits for a spacer"
    ERR_MISCSPACER = "unexplained spacer processing error"
    ERR_BADSPACER_LENGTH = "a spacer has been submitted with the wrong length (should be 23 bp)" 

    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            self.__setattr__(k,v)
        if not "key" in kwargs:
            self.key = "{0}".format(long(random.random() * 1e16))
            
    @property
    def genome_name(self):
        for k,v in Job.GENOMES.items():
            if v == self.genome:
                return k
        raise Exception("Genome not found")

    @property
    def mapped(self):
        if self.chr is not None:
            return True
        else:
            return False
    @property
    def safe_name(self):
        r = re.compile("[^a-z]")
        return re.sub(r, "_", self.name.lower())

    @property
    def f1(self):
        return os.path.join(self.path,"f1.txt")
    @property
    def f2(self):
        return os.path.join(self.path,"f2.txt")
    @property
    def f3(self):
        return os.path.join(self.path,"f3.txt")
    @property
    def f4(self):
        return os.path.join(self.path,"f4.txt")
    @property
    def f5(self):
        return os.path.join(self.path,"f5.pdf")
    @property
    def f6(self):
        return os.path.join(self.path,"f6.csv")
    @property
    def f7(self):
        return os.path.join(self.path,"f7.in")
    @property
    def f8(self):
        return os.path.join(self.path,"f8.out")
    @property
    def f9(self):
        return os.path.join(self.path,"f9.csv")
    @property
    def files(self):
        return [{"name":"summary.pdf".format(self.name),
                 "filename":"{0}-summary.pdf".format(self.name),
                 "url":self.url(self.f5),
                 "ready":os.path.isfile(self.f5)},
                {"name":"offtargets.csv".format(self.name),
                 "filename":"{0}-offtargets.csv".format(self.name),
                 "url":self.url(self.f6),
                 "ready":os.path.isfile(self.f6)}]

#                {"name":"primers.csv".format(self.name),
#                 "filename":"{0}-primers.csv".format(self.name),
#                 "url":self.url(self.f9),
#                 "ready":os.path.isfile(self.f9)}
#
        
    @property 
    def good_spacers(self):
        return [s for s in self.spacers if len([h for h in s.hits if h.ontarget]) == 1]

    @property
    def submitted_ms(self):
        return calendar.timegm(self.date_submitted.utctimetuple()) * 1000 if self.date_submitted is not None else None
    @submitted_ms.setter
    def submitted_ms(self, value):
        self.date_submitted = datetime.utcfromtimestamp(value//1000) if value is not None else None
    @property
    def completed_ms(self):
        return calendar.timegm(self.date_completed.utctimetuple()) * 1000 if self.date_completed is not None else None
    @completed_ms.setter
    def completed_ms(self, value):
        self.date_completed = datetime.utcfromtimestamp(value//1000) if value is not None else None
    @property
    def computing_hits(self):
        if not self.computed_spacers:
            return False
        for s in self.spacers:
            if(s.computing_hits):
                return True
        return False
    @property
    def computed_hits(self):
        if not self.computed_spacers: 
            return False
        for s in self.spacers:
            if(not s.computed_hits):
                return False
        return True

    @property
    def n_spacers(self):
        return len(self.spacers)

    @property
    def n_completed_spacers(self):
        return len([s for s in self.spacers if s.computed_hits])

    @property
    def computed_n_hits(self):
        return sum([len(s.hits) for s in self.spacers])

    def url(self,filepath):
        #we simlink /files to [jobs_directory]/..
        #hence we do this the easy way:
        # 1. extract os.path.join(os.path.split(this.path)[:-1]) from the file
        # 2. return /files + result
        
        rootpath = os.path.split(os.path.split(self.path)[0])[0]
        server_rel = filepath.split(rootpath)[1]
        return "/files" + server_rel

    @property
    def path(self):
        from cfront import cfront_settings
        job_key = self.id
        jobpath = cfront_settings["jobs_directory"]
        path =   os.path.join(jobpath,"{0}").format(job_key)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path


    def jsonAttributes(self):
        return ["id", "sequence", 
                "submitted_ms", "completed_ms", 
                "genome", "name", "email",
                "computed_spacers",
                "computed_hits",
                "computed_n_hits",
                "chr", "start", "strand",
                "files_ready",
                "email_complete",
                "files","key",
                "genome_name",
                "mapped", "query_type",
                "n_spacers","n_completed_spacers"]
    @staticmethod
    def get_job_by_key(job_key):
        j =  Session.query(Job).filter(Job.key == job_key).first()
        if j is None:
            from cfront.models import JobNOTFOUND
            raise JobNOTFOUND("job not found {0}".format(job_key), None)
        return j
    
    def __repr__(self):
        if self.files_ready:
            status_string = "Files ready"
        elif self.computed_hits:
            status_string = "Hits ready"
        elif self.computed_spacers:
            status_string = "Spacers ready"
        else:
            status_string = "New job"
            
        return "Job {0} {1}bp ({2})".format(self.id, len(self.sequence), status_string)


