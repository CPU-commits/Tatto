# Responses
import fastapi
from fastapi.exceptions import HTTPException

import json
from bson import json_util

status = fastapi.status

# Models

from app.models.post import Post
from app.models.profile import Profile
from app.models.user import User
# Interfaces
from app.interfaces.post import Post as PostBody


# from app.services.tattoos import tattoos_service
from app.services.profiles import profiles_service


# Token
from app.dependencies import TokenData

class Posts():
    def get_by_profile(self, profile: str) -> Post:
        return list(Post.objects().aggregate([
            {
                "$match": {
                    "profile": profile,
                },
            },
            {
                "$lookup": {
                    "from": Profile._get_collection_name(),
                    "localField": "profile",
                    "foreignField": "_id",
                    "as": "profile",
                    "pipeline": [
                        {
                            "$lookup": {
                                "from": User._get_collection_name(),
                                "localField": "user",
                                "foreignField": "_id",
                                "as": "user",
                                "pipeline": [{
                                    "$project": {
                                        "name": 1,
                                    },
                                }]
                            },
                        },
                        {
                            "$project": {
                                "user": 1,
                                "avatar": 1,
                            }
                        },
                        {
                            "$addFields": {
                                "user": {
                                    "$arrayElemAt": ["$user", 0],
                                },
                            },
                        },
                    ]
                },
            },
            {
                "$addFields": {
                    "profile": {
                        "$arrayElemAt": ["$profile", 0],
                    },
                },
            },
        ]))

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

    def count_posts_profile(self, nickname: str) -> int:
        profile = profiles_service.get_by_nick(nickname)

        return Post.objects(profile=profile.id).count()

    def get_posts_by_perfil(
        self,
        page: int,
        items_per_page: int,
        nickname: str,
    ) -> list[Post]:
        start = (page - 1) * items_per_page
        end = start + items_per_page
        profile = profiles_service.get_by_nick(nickname)
        posts = self.get_by_profile(profile.id)
        if not posts:
            return []
        return json.loads(json_util.dumps(posts[start:end]))

posts_service = Posts()
