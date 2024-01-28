from mongoengine import *
from app.db.db import uri

POST_COLLECTION = 'posts'

connect(host=uri)

class Post(Document):
    profile = ReferenceField('Profile', required=True)
    # tatto = ListField(ReferenceField('Tatto'))
    content = StringField(required=True, max_length=250)
    likes = IntField(default=0)
    date = DateField(required=True)
