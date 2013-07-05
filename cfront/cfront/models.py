#Database Model
from sqlalchemy import MetaData
metadata = MetaData()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Unicode, DateTime, ForeignKey, Boolean, UniqueConstraint


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

import model
from model import *
