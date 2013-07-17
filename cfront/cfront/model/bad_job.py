from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base

class BadJob(Base):
    __tablename__ = 'badjob'
    
    #pkey
    id = Column(Integer, primary_key = True)

    #nonnull
    sequence = Column(Unicode, nullable = False)
    date_submitted = Column(DateTime, nullable = False)
    date_failed = Column(DateTime, nullable = False)
    genome = Column(Integer, nullable = False)

    #nullable
    name = Column(Unicode, nullable = False)
    email = Column(Unicode, nullable = False)
    error_message=Column(Unicode, nullable = False)
    traceback = Column(Unicode, nullable = False)
