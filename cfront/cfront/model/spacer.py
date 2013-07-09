from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float, UniqueConstraint
from sqlalchemy.types import VARCHAR
from cfront.models import Session, Base

class Spacer(Base):
    __tablename__ = 'spacer'

    __table_args__ = (
        UniqueConstraint('jobid', 'strand', 'position'),
    )
    
    id = Column(Integer, primary_key = True)
    jobid = Column(Integer, ForeignKey("job.id"),nullable=False)
    sequence = Column(VARCHAR(23),nullable=False)
    guide = Column(VARCHAR(20), nullable = False)
    nrg = Column(VARCHAR(3),nullable = False)
    strand = Column(Integer, nullable = False)
    position = Column(Integer, nullable = False)

    score = Column(Float,nullable = True)
    mismatch = Column(Integer,nullable = True)
    mismatch_pos = Column(String,nullable = True)
    gene = Column(String, nullable = True)

    computing_hits = Column(Boolean, nullable = False, default = False)
    computed_hits = Column(Boolean, nullable = False, default = False)
    
    @property
    def start(self):
        return self.position

    def jsonAttributes(self):
        return ["jobid", "sequence", "guide", "nrg", "strand", "position",
                "computing_hits", "computed_hits", "id", "start",
                "score", "mismatch", "mismatch_pos", "gene"]

    



