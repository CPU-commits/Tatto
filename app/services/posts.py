# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from concurrent import futures

import json
from bson import json_util

status = fastapi.status

# Models

from app.models.post import Post
from app.models.profile import Profile
from app.models.user import User
# Interfaces
from app.interfaces.post import Post as PostBody
from app.services.image import image_service


from app.services.profiles import profiles_service


# Token
from app.dependencies import TokenData

class Posts():
    def get_post_by_id(self,id :str,return_json=False)->Post:
        post = Post.objects(id=id).first()
        if id is not None and return_json is True:
            return json.loads(post.to_json())
        return post
       
    
    
    
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

    def _upload_image(
        self,
        file: UploadFile,

    ) -> Post:
        if "image" not in file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid types',
            )
        image_key = image_service.upload(file)
        if image_key is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pueden subir los tatuajes. Intente más tarde",
            )

        return image_key

    def create_post(self, files: list[UploadFile],content:str , tokenData : TokenData) -> Post:
        profile = profiles_service.get_by_id_user(tokenData.id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        inserted_images = []
        if files is not None:
            with futures.ThreadPoolExecutor(10) as executor:
                futures_to_process = []
                for file in files:
                    futures_to_process.append(
                        executor.submit(
                            self._upload_image,
                            file,
                        ),
                    )
                for future in futures.as_completed(futures_to_process):
                    inserted_images.append(future.result())
        
        post = PostBody(profile = str(profile.id), images=inserted_images,content = content)
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
        posts = self.get_by_profile(profile.id)[::-1]
        mod_post = []
    
        for post in posts:
            for i in range(len(post['images'])):
                post['images'][i] = image_service.get_signed_url(post['images'][i])
            mod_post.append(post)

        if not mod_post:
            return []
        return json.loads(json_util.dumps(mod_post[start:end]))

   
posts_service = Posts()
