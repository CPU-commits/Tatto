from mongoengine import *
from app.dependencies import uri

FOLLOW_COLLECTION = 'likes'

connect(host=uri)

class Like(Document):
    post = ReferenceField('Post',required=False)
