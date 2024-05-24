from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class Post(BaseModel):
    profile: str 
    images : Optional[list]
    content : str
    def to_model(self):
        return {
            'profile': self.profile,
            'images': self.images,
            'likes' : 0,   
            'content' : self.content,
            'date': datetime.utcnow(),
        }

class PostUpdate(BaseModel):
    content: Optional[str]
    is_visible: Optional[bool]
   

