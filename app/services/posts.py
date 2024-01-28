# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from typing import Optional

status = fastapi.status

# Models

from app.models.post import Post
# Interfaces
from app.interfaces.post import Post as PostBody


from app.services.tattoos import tattoos_service
from app.services.profiles import profiles_service


# Token
from app.dependencies import TokenData

class Posts():
    def get_by_profile(self, profile: str) -> Post:
        return Post.objects(profile=profile)

    def create_post(self,files : list[UploadFile],tattos :list  ,categories: list,content:str , tokenData : TokenData) -> Post:
        profile = profiles_service.get_by_id_user(tokenData.id)
        inserted_tattoos = []
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        
        #Subir post con imagenes del post, todas las categorias se aplican a todas las imagenes del post
        if files is not None:
            inserted_tattoos = tattoos_service.create_tatto(files,categories,tokenData)
        
        if len(tattos) > 0:
            for i in tattos:
                tatto = tattoos_service.get_by_id(i)
                if tatto is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Not valid id tatto',
                    )
                if profile.id == tatto.profile.id:
                    inserted_tattoos.append(tatto)
        post = PostBody(profile = str(profile.id), tatto = inserted_tattoos, content = content)
        Post(**post.to_model()).save()

    def get_posts_by_perfil(self, nickname : str)    -> Post:
        profile = profiles_service.get_by_nick(nickname)
        posts = self.get_by_profile(profile.id)
        return posts.to_json()

posts_service = Posts()
