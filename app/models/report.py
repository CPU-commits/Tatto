from mongoengine import *
from app.dependencies import uri
from enum import Enum

REPORT_COLLECTION = 'reports'

connect(host=uri)

class Reasons(Enum):
    OTHER = 'other'

class Report(Document):
    user = ReferenceField('User', required=True)
    profile = ReferenceField('Profile', required=True)
    reason = EnumField(Reasons, default=Reasons.OTHER)
    content = StringField(required=True, max_length=500)
    date = DateField(required=True)
