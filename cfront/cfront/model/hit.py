from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float, UniqueConstraint
from sqlalchemy.types import VARCHAR, SmallInteger

from cfront.models import Session, Base

class Hit(Base):
    __tablename__ = 'hit'
    __table_args__ = (
        UniqueConstraint('spacerid', 'chr', 'start', 'strand'),
    )
    
    id = Column(Integer, primary_key = True)
    spacerid = Column(Integer, ForeignKey("spacer.id"), nullable =False)
    n_mismatches = Column(SmallInteger, nullable = False, index = True)
    score = Column(Float, nullable = True, index = True)
    chr = Column(VARCHAR(6), nullable = False)
    start = Column(Integer, nullable = False)
    strand = Column(SmallInteger, nullable = False)
    sequence = Column(VARCHAR(23), nullable = False)

    @property
    def ontarget(self):
        return self.n_mismatches == 0
    @property
    def jobid(self):
        return self.spacer.job.id
    def jsonAttributes(self):
        return ["id","jobid", "spacerid", "ontarget", "chr", "start", "strand", "sequence", "n_mismatches", "score"]
