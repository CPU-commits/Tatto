from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    profile: str 
    # tatto : list
    content : str
    def to_model(self):
        return {
            'profile': self.profile,
            # 'tatto': self.tatto,
            'likes' : 0,   
            'content' : self.content,
            'date': datetime.utcnow(),
        }


