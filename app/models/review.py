from mongoengine import *
from app.dependencies import uri

REVIEW_COLLECTION = 'reviews'

connect(host=uri)

class Review(Document):
    user = ReferenceField('User', required=True)
    profile = ReferenceField('Profile', required=True)
    content = StringField(required=True, max_length=500)
    stars = IntField(default=0)
    date = DateField(required=True)
