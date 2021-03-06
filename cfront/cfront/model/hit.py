from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float, UniqueConstraint
from sqlalchemy.types import VARCHAR, SmallInteger

from cfront.models import Session, Base

class Hit(Base):
    __tablename__ = 'hit'
    __table_args__ = (
        UniqueConstraint('spacerid', 'chr', 'start', 'strand'),
    )
    
    id = Column(BigInteger, primary_key = True)
    spacerid = Column(BigInteger, ForeignKey("spacer.id"), nullable =False)
    n_mismatches = Column(SmallInteger, nullable = False, index = True)
    score = Column(Float, nullable = True, index = True)
    chr = Column(VARCHAR(6), nullable = False)
    start = Column(BigInteger, nullable = False)
    strand = Column(SmallInteger, nullable = False)
    sequence = Column(VARCHAR(23), nullable = False)
    gene = Column(String, nullable = True, index = True)
    ontarget = Column(Boolean, nullable = False)

    @property
    def jobid(self):
        return self.spacer.job.id
    def jsonAttributes(self):
        return ["id","jobid", "spacerid", "ontarget", "chr", "start", "strand", "sequence", "n_mismatches", "score", "gene"]
