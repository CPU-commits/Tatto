from mongoengine import *
from app.dependencies import uri

FOLLOW_COLLECTION = 'likes'

connect(host=uri)

class Like(Document):
    user = ReferenceField('User',required=True)
    profile = ReferenceField('Profile',required=True,unique=False)
    post = ReferenceField('Post',required=True)
    date = DateField(required=True)
