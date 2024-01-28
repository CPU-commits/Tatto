from mongoengine import *
from app.dependencies import uri

CATEGORY_COLLECTION = 'categories'

connect(host=uri)

class Category(Document):
    name = StringField(required=True, max_length=100, unique=True)
    # slug = StringField(required=True, max_length=100, unique=True)
    state = BooleanField(default=True)
    description = StringField(required=False, max_length=500)
    date = DateField(required=True)
