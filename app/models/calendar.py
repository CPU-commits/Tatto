from mongoengine import *
from app.dependencies import uri

CALENDAR_COLLECTION = 'calendars'

connect(host=uri)

class Day(EmbeddedDocument):
    day = DateField(required=True)
    hour_start = DateField(required=True)
    hour_finish = DateField(required=True)

class Calendar(Document):
    profile = ReferenceField('Profile', required=True)
    days = ListField(EmbeddedDocumentField(Day), required=True)
    exceptions = ListField(EmbeddedDocumentField(Day))
    date = DateField(required=True)
