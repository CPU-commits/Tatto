from mongoengine import *
from app.dependencies import uri

TATTO_COLLECTION = 'tattos'

connect(host=uri)

class Tatto(Document):
    profile = ReferenceField('Profile', required=True)
    image = StringField(required=True)
    categories = ListField(ReferenceField('Category', required=True), required=True)
    likes = IntField(default=0)
    date = DateField(required=True)
