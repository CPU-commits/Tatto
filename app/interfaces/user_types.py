from enum import Enum

class UserStates(Enum):
    DISABLED = 'deactivate'
    ACTIVE = 'active'

class UserTypes(Enum):
    ADMIN = 'd'
    STUDIO_OWNER = 'c'
    TATTO_ARTIST = 'b'
    CLIENT = 'a'
