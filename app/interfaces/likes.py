from pydantic import BaseModel
from datetime import datetime


class Like(BaseModel):
    user: str 
    profile: str
    post: str
    def to_model(self):
        return {
            'user': self.user,
            'profile': self.profile,
            'post' : self.post,
            'date': datetime.utcnow(),
        }
