from sqlalchemy.orm import relation, backref
from ..models import metadata
from batch import Batch
from job import Job
from spacer import Spacer
from hit import Hit
from bad_job import BadJob

Job.batch = relation(Batch, backref = backref("jobs", cascade = "all, delete, delete-orphan"))
Spacer.job = relation(Job,backref=backref("spacers", cascade="all, delete, delete-orphan"))
Hit.spacer = relation(Spacer,backref=backref("hits", cascade="all, delete, delete-orphan"))
