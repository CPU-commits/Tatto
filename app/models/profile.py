from mongoengine import *
from app.db.db import uri

PROFILE_COLLECTION = 'profiles'

connect(host=uri)

class Profile(Document):
    user = ReferenceField('User', required=True)
    description = StringField(required=False, max_length=150)
    avatar = StringField(required=False)
    likes = IntField(min_value=0, default=0)
    categories = ListField(ReferenceField('Category', required=False))
    nickname = StringField(required=True, max_length=50, unique=True)
    date = DateField(required=True)
