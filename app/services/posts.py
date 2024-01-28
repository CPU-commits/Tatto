# Responses
import fastapi
from fastapi.exceptions import HTTPException

import json

status = fastapi.status

# Models

from app.models.post import Post
# Interfaces
from app.interfaces.post import Post as PostBody


# from app.services.tattoos import tattoos_service
from app.services.profiles import profiles_service


# Token
from app.dependencies import TokenData

class Posts():
    def get_by_profile(self, profile: str) -> Post:
        return Post.objects(profile=profile)
    def create_post(self,content:str , tokenData : TokenData) -> Post:
        profile = profiles_service.get_by_id_user(tokenData.id)
        # inserted_tattoos = []
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        
        post = PostBody(profile = str(profile.id), content = content)
        Post(**post.to_model()).save()

    def get_posts_by_perfil(self, page: int, items_per_page: int, nickname: str) -> Post:
        start = (page - 1) * items_per_page
        end = start + items_per_page
        profile = profiles_service.get_by_nick(nickname)
        posts = self.get_by_profile(profile.id)
        if not posts:
            return []
        return json.loads(posts.to_json())[start:end]

posts_service = Posts()