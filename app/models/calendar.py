from mongoengine import *
from app.dependencies import uri

CALENDAR_COLLECTION = 'calendars'

connect(host=uri)

class CalendarBlock(EmbeddedDocument):
    day = EnumField(required=True, enum=['M', 'T', 'W', 'X', 'F', 'S', 'SU'])
    time_since = DateTimeField(required=True)
    time_until = DateTimeField(required=True)

class ExceptionDay(EmbeddedDocument):
    day = DateField(required=True)
    hour_start = DateField(required=True)
    hour_finish = DateField(required=True)

class Settings(EmbeddedDocument):
    days_advance = IntField(required=True, min_value=1, max_value=30)

class Calendar(Document):
    profile = ReferenceField('Profile', required=True)
    blocks = ListField(EmbeddedDocumentField(CalendarBlock))
    exceptions = ListField(EmbeddedDocumentField(ExceptionDay))
    settings = EmbeddedDocumentField(Settings)
    created_at = DateField(required=True)
    updated_at = DateField(required=True)
