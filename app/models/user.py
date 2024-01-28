from mongoengine import *
from app.dependencies import uri
# Interfaces
from app.interfaces.user_types import UserTypes, UserStates

USER_COLLECTION = 'users'

connect(host=uri)

class User(Document):
    role = EnumField(UserTypes, default=UserTypes.CLIENT)
    state = EnumField(UserStates, default=UserStates.ACTIVE)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True, max_length=100)
    date = DateField(required=True)
