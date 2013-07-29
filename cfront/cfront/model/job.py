from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base
import calendar, os, random
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

    #v0 maps to exactly one site on the genome
    chr = Column(VARCHAR(6), nullable = False)
    start = Column(BigInteger, nullable = False)
    strand = Column(Integer, nullable = False)

    computing_spacers = Column(Boolean, nullable = False, default = False)
    computed_spacers = Column(Boolean, nullable = False, default = False)
    files_computing =  Column(Boolean, nullable = False, default = False)
    files_ready = Column(Boolean, nullable = False, default = False)
    email_complete = Column(Boolean, nullable = False, default = True)
    key = Column(String, nullable = False, index = True)

    #fake enum type for genomes
    GENOMES={
        "HUMAN":1
    }

    
    #exceptions
    NOSPACERS = "spacers not yet computed"
    NOHITS = "hits not yet computed"
    ERR_TOOMANY = "too many spacers in a single alignment. right now does 1 at a time"
    ERR_MISSING = "no spacers in bowtie alignment"
    ERR_ALREADYCOMPUTED = "already computed hits"
    ERR_MULTIPLE_ONTARGETS = "found multiple exact hits for a spacer"
    ERR_MISCSPACER = "unexplained spacer processing error"

    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            self.__setattr__(k,v)
        self.key = "{0}".format(int(random.random() * 1e10))
        

    @property
    def path(self):
        from cfront import cfront_settings
        job_key = self.id
        jobpath = cfront_settings["jobs_directory"]
        path =   os.path.join(jobpath,"jobs/{0}").format(job_key)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

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
                 "ready":os.path.isfile(self.f6)},
                {"name":"primers.csv".format(self.name),
                 "filename":"{0}-primers.csv".format(self.name),
                 "url":self.url(self.f9),
                 "ready":os.path.isfile(self.f9)}]

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
    def computed_n_hits(self):
        return sum([len(s.hits) for s in self.spacers])

    def url(self,path):
        server_rel = path.split("/jobs")[1]
        return "/files" + server_rel

    def jsonAttributes(self):
        return ["id", "sequence", 
                "submitted_ms", "completed_ms", 
                "genome", "name", "email",
                "computing_spacers",
                "computed_spacers",
                "computed_hits",
                "computing_hits",
                "computed_n_hits",
                "chr", "start", "strand",
                "files_ready",
                "email_complete",
                "files","key"]
    @staticmethod
    def get_job_by_key(job_key):
        return Session.query(Job).filter(Job.key == job_key).one()



