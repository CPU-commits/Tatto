from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime


class Profile(BaseModel):
    user: str 
    nickname: str
    def to_model(self):
        return {
            'user': self.user,
            'nickname': self.nickname,
            'categories' : [],
            'date': datetime.utcnow(),
        }


class ProfileUpdate(BaseModel):
    nickname: Optional[str]
    description : Optional[str]
    categories : Optional[List[str]] 
    likes : Optional[List[str]]
