from mongoengine import *
from app.dependencies import uri

PROFILE_COLLECTION = 'profiles'

connect(host=uri)

class Profile(Document):
    user = ReferenceField('User', required=True)
    description = StringField(required=False, max_length=150)
    avatar = StringField(required=False)
    likes = ListField(ReferenceField('Like', required=False))
    categories = ListField(ReferenceField('Category', required=False))
    nickname = StringField(required=True, max_length=50, unique=True)
    date = DateField(required=True)
