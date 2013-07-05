from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float, UniqueConstraint
from sqlalchemy.types import VARCHAR

from cfront.models import Session, Base

class Hit(Base):
    __tablename__ = 'hit'
    __table_args__ = (
        UniqueConstraint('spacerid', 'chr', 'start', 'strand'),
    )
    
    id = Column(Integer, primary_key = True)
    spacerid = Column(Integer, ForeignKey("spacer.id"), nullable =False)
    ontarget = Column(Boolean, nullable = False)
    similarity = Column(Float, nullable = False)
    chr = Column(VARCHAR(3), nullable = False)
    start = Column(Integer, nullable = False)
    strand = Column(Integer, nullable = False)
    
