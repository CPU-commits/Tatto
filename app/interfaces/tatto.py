from pydantic import BaseModel
from datetime import datetime


class Tatto(BaseModel):
    profile: str 
    image : str
    categories : list

    def to_model(self):
        return {
            'profile': self.profile,
            'image': self.image,
            'likes' : 0,   
            'categories' : self.categories,
            'date': datetime.utcnow(),
        }
