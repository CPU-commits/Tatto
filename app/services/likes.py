# Responses
import fastapi
import json

status = fastapi.status
# Models
from app.models.like import Like
from app.dependencies import TokenData

# Interfaces


#Services
from app.services.profiles import profiles_service
from app.services.posts import posts_service
class Likes():

    def like_post(self,id_post : str,tokenData: TokenData) -> Like:
        #recibe post del usuario y id del usuario que da like
        bool = profiles_service.like(id_post,tokenData)
        posts_service.like_post(bool,id_post)
        return 

likes_service = Likes()
