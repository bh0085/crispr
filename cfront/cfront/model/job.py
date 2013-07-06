from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base
import calendar

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

    computing_spacers = Column(Boolean, nullable = False, default = False)
    computed_spacers = Column(Boolean, nullable = False, default = False)

    GENOMES={
        "HUMAN":1
    }

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
        #computing if any spacer is computing hits
        if not self.computed_spacers: return False
        return True if True in [e.computing_hits for e in self.spacers] else False
    @property
    def computed_hits(self):
        #done if all spacers have computed hits
        if not self.computed_spacers: return False
        return False if False in [e.computed_hits for e in self.spacers] else True
        
    def jsonAttributes(self):
        return ["id", "sequence", 
                "submitted_ms", "completed_ms", 
                "genome", "name", "email",
                "computing_spacers",
                "computed_spacers",
                "computed_hits",
                "computing_hits"]

    
