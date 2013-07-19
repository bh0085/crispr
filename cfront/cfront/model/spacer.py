from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float, UniqueConstraint
from sqlalchemy.types import VARCHAR
from cfront.models import Session, Base
from sqlalchemy import desc

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

    score = Column(Float,nullable = True, index = True)
    computing_hits = Column(Boolean, nullable = False, default = False)
    
    @property
    def computed_hits(self):
        return False if self.score == None else True
    @property
    def start(self):
        return self.position

    @property
    def n_offtargets(self):
        from cfront.models import Hit
        return Session.query(Hit).join(Spacer).filter(Spacer.id==self.id).count()
    @property
    def top_hits(self):
        from cfront.models import Hit
        return [e.toJSON() for e in Session.query(Hit).join(Spacer).filter(Spacer.id == self.id).order_by(desc(Hit.score)).limit(50).all()]

    @property
    def genic_hits(self):
        from cfront.models import Hit
        return [e.toJSON() for e in Session.query(Hit).join(Spacer).filter(Spacer.id == self.id).filter(Hit.gene != None).all()]
        
    def jsonAttributes(self):
        return ["jobid", "sequence", "guide", "nrg", "strand", "position",
                "computing_hits", "computed_hits", "id", "start",
                "score", "n_offtargets"]

    



