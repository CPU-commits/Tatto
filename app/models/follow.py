from mongoengine import *
from app.db.db import uri

FOLLOW_COLLECTION = 'follows'

connect(host=uri)

class Follow(Document):
    user = ReferenceField('User', required=True)
    profile = ReferenceField('Profile', required=True)
    date = DateField(required=True)
