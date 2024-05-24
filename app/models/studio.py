from mongoengine import *
from app.dependencies import uri
# Interfaces
from app.interfaces.user_types import UserTypes, UserStates

STUDIO_COLLECTION = 'studios'

connect(host=uri)

class Direction(EmbeddedDocument):
    name = StringField(required=True)
    lat = FloatField(required=True)
    lng = FloatField(required=True)

class Studio(Document):
    users = ListField(ReferenceField('User'), required=False)
    description = StringField(required=False, max_length=500)
    direction = EmbeddedDocumentField(Direction, required=False)
    email = EmailField(required=True)
    phone = StringField(required=False, max_length=15)
    owners = ListField(ReferenceField('User', required=True), required=True)
    date = DateField(required=True)
