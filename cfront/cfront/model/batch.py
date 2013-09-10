from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Unicode, DateTime, ForeignKey, Index, Boolean, Float
from cfront.models import Session, Base
import calendar, os, random, re
from sqlalchemy.types import VARCHAR


class Batch(Base):
    __tablename__ = "batch"
    id = Column(BigInteger, primary_key = True)
    date_submitted = Column(DateTime, nullable = False)
    genome = Column(Integer, nullable = False)
    key = Column(String, nullable = False, index = True, unique = True)
    original_filename = Column(Unicode, nullable = True)

    name = Column(Unicode, nullable = True)
    email = Column(Unicode, nullable = True)

    #ITS POSSIBLE THAT NONE OF THIS WILL BE USED....
    date_completed = Column(DateTime, nullable = True)
    failed = Column(Boolean, nullable = False, default = False)
    date_failed = Column(DateTime, nullable = True)
    error_traceback = Column(Unicode, nullable = True)
    error_message = Column(Unicode, nullable = True)
    email_complete = Column(Boolean, nullable = False, default = True)
    has_emailed = Column(Boolean, nullable = False, default = False)
        
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            self.__setattr__(k,v)
        if not "key" in kwargs:
            self.key = "{0}".format(long(random.random() * 1e16))

    def save_input_file(self, file_buffer):
        fpath = os.path.join(self.path, "input_file.txt")
        with open(fpath,'w') as f:
            file_buffer.seek(0)
            f.write(file_buffer.read())

                        
    @property
    def genome_name(self):
        from cfront.models import Job
        for k,v in Job.GENOMES.items():
            if v == self.genome:
                return k
        raise Exception("Genome not found")


    @property
    def path(self):
        from cfront import cfront_settings
        jobpath = cfront_settings["jobs_directory"]
        path =   os.path.join(jobpath,"batch_{0}").format(self.key)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    @staticmethod
    def get_batch_by_key(batch_key):
        b =  Session.query(Batch).filter(Batch.key == batch_key).first()
        if b is None:
            from cfront.models import BatchNOTFOUND
            raise BatchNOTFOUND("batch not found {0}".format(batch_key), None)
        return b
        
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


    def jsonAttributes(self):
        return ["id", 
                "submitted_ms", "completed_ms", 
                "genome","original_filename", "email",
                "email_complete",
                "key","genome_name"]
