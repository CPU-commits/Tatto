from mongoengine import *
from app.dependencies import uri
from enum import Enum
from app.models.calendar import Day

MEETING_COLLECTION = 'meetings'

connect(host=uri)

class Who(Enum):
    TATTO_ARTIST = 'tatto'
    CLIENT = 'client'

class State(Enum):
    SUCCESS = 'success'
    FAILED = 'failed'
    NEGOTIATING = 'negotiating'
    REFUSED = 'refused'
    ACCEPTED = 'accepted'

class Response(EmbeddedDocument):
    content = StringField(required=True, max_length=300)
    who = EnumField(Who, default=Who.CLIENT)
    files = ListField(StringField())
    date = DateField(required=True)
    offer = EmbeddedDocumentField(Day)

class Meeting(Document):
    responses = ListField(EmbeddedDocumentField(Response), required=True)
    profile = ReferenceField('Profile', required=True)
    user = ReferenceField('User', required=True)
    state = EnumField(State, default=State.NEGOTIATING)
    scheduled = EmbeddedDocumentField(Day)
    date = DateField(required=True)
    update_date = DateField(required=True)
