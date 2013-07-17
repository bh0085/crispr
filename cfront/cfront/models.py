#Database Model
from sqlalchemy import MetaData
metadata = MetaData()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Unicode, DateTime, ForeignKey, Boolean, UniqueConstraint
import traceback, datetime, StringIO

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(metadata = metadata)

def __init__(self, **kwargs):
    for k,v in kwargs.iteritems():
        self.__setattr__(k,v)
        
def toJSON(self):
    return dict([(k,getattr(self,k)) for k in self.jsonAttributes()])
Base.__init__ = __init__
Base.toJSON = toJSON

def JobERR(job, msg):
    s = StringIO.StringIO()
    traceback.print_stack(None, None, s)
    s.seek(0)
    tb_content = s.read()
    print tb_content

    if job.id:

        #prints error message and a strack trace to the BadJob table
        Session.add(BadJob(sequence = job.sequence,
                           date_submitted = job.date_submitted,
                           date_failed = datetime.datetime.utcnow(),
                           error_message = msg,
                           id = job.id,
                           traceback = tb_content,
                           genome=job.genome,
                           name = job.name,
                           email = job.email))
    Session.delete(job)


import model
from model import *
