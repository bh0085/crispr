from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base
import calendar
from sqlalchemy.types import VARCHAR


class Job(Base):
    __tablename__ = 'job'
    
    #pkey
    id = Column(Integer, primary_key = True)

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
    start = Column(Integer, nullable = False)
    strand = Column(Integer, nullable = False)

    computing_spacers = Column(Boolean, nullable = False, default = False)
    computed_spacers = Column(Boolean, nullable = False, default = False)

    #fake enum type for genomes
    GENOMES={
        "HUMAN":1
    }

    
    #exceptions
    NOSPACERS = "spacers not yet computed"
    NOHITS = "hits not yet computed"
    ERR_TOOMANY = "too many spacers in a single alignment"
    ERR_MISSING = "no spacers in bowtie alignment"

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

    def jsonAttributes(self):
        return ["id", "sequence", 
                "submitted_ms", "completed_ms", 
                "genome", "name", "email",
                "computing_spacers",
                "computed_spacers",
                "computed_hits",
                "computing_hits",
                "computed_n_hits",
                "chr", "start", "strand"]


    
