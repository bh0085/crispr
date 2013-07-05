from sqlalchemy.orm import relation, backref
from ..models import metadata
from job import Job
from spacer import Spacer
from hit import Hit

Spacer.job = relation(Job, backref = "spacers")
Hit.spacer = relation(Spacer, backref = "hits")
