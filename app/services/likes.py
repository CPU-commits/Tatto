# Responses
from fastapi.exceptions import HTTPException

import fastapi
import json

status = fastapi.status
# Models
from app.models.like import Like
from app.dependencies import TokenData
from app.models.post import Post

# Interfaces
from app.interfaces.likes import Like as LikeBody

#Services
from app.services.profiles import profiles_service
from app.services.users import users_service
from app.services.posts import posts_service
class Likes():
    #recibe los likes de un usuario a traves de su id
    def get_likes_by_user(self, id: str,return_json=False) ->list[Like]: 
        like = Like.objects(user=id)
        if id is not None and return_json is True:
            return json.loads(like.to_json())
        return like
    #comprueba si el like ya existe, si existe lo elimina y return False sino return True, 
    def comprobation(self,post : Post, tokenData:TokenData) -> Like | None: 
        likes = self.get_likes_by_user(tokenData.id)
        for like in likes:
            if (like.post.id == post.id):
                like.post.update(**{"likes" : like.post.likes - 1})
                like.delete()
                return False
        post.update(**{"likes" : post.likes + 1})
        return True
    #Recibir id y con eso sacar user y profile
    def like_post(self,id_post : str,tokenData: TokenData) -> Like:
        user = users_service.get_by_id(tokenData.id)
        profile = profiles_service.get_by_id_user(tokenData.id)
        post = posts_service.get_post_by_id(id_post)

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        if  user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid user',
            )
        if  post is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid post',
            )
        like = LikeBody(user = str(user.id), profile=str(profile.id),post=str(post.id))
        res = self.comprobation(post,tokenData)
        
        print(res, like)    
        if res:
            Like(**like.to_model()).save()
      
        likes = self.get_likes_by_user(tokenData.id)
        profile.likes = likes
        profile.save()
        return 


likes_service = Likes()
