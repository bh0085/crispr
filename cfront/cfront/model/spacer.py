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
    
    id = Column(BigInteger, primary_key = True)
    jobid = Column(BigInteger, ForeignKey("job.id"),nullable=False)
    sequence = Column(VARCHAR(23),nullable=False)
    strand = Column(Integer, nullable = False)
    position = Column(BigInteger, nullable = False)

    score = Column(Float,nullable = True, index = True)
    computing_hits = Column(Boolean, nullable = False, default = False)
    n_offtargets = Column(Integer, nullable = True)
    n_genic_offtargets = Column(Integer, nullable = True)
    name = Column(Unicode, nullable = True)

    @property
    def guide(self):
        return self.sequence[:-3]

    @property
    def nrg(self):
        return self.sequence[-3:]
    
    @property
    def computed_hits(self):
        return False if self.score == None else True
    @property
    def start(self):
        return self.position

    @property 
    def chr_start(self):
        #subtracts one to account for one based indexing...
        if self.job.start is None:
            return -1
        return self.job.start + self.start +1

    @property
    def top_hits(self):
        from cfront.models import Hit
        return [e.toJSON() for e in Session.query(Hit).join(Spacer).filter(Spacer.id == self.id).order_by(desc(Hit.score)).limit(20).all()]

    @property
    def genic_hits(self):
        from cfront.models import Hit
        return [e.toJSON() for e in Session.query(Hit).join(Spacer).filter(Spacer.id == self.id).filter(Hit.gene != None).all()]
        
    def jsonAttributes(self):
        return ["jobid", "sequence", "guide", "nrg", "strand", "position",
                "computing_hits", "computed_hits", "id", "start",
                "score", "n_offtargets","n_genic_offtargets", "name"]
