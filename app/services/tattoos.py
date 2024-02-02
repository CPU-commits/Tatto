# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
status = fastapi.status
from uuid import uuid4
import json
from concurrent import futures

# Models
from app.models.tatto import Tatto
from app.models.profile import Profile
# Interfaces
from app.interfaces.tatto import Tatto as TattoBody
# Services
from app.services.categories import categories_service
from app.services.image import image_service
from app.services.profiles import profiles_service
# Token
from app.dependencies import TokenData

class Tattoos():
    def get_by_id(self,id : str) -> Tatto | None:
        return Tatto.objects(id=id).first()
    
    def count_max_tattoos(self, nickname: str) -> int:
        profile = profiles_service.get_by_nick(nickname)

        return Tatto.objects(profile=profile.id).count()

    def get_tattoos_by_nickname(self, nickname: str, page: int) -> list[Tatto]:
        profile = profiles_service.get_by_nick(nickname)

        # Search
        limit_tattoos = 20
        skip_tattoos = limit_tattoos * page

        tattoos_db = Tatto.objects(profile=profile.id).order_by('-date')[skip_tattoos:limit_tattoos+skip_tattoos]
        # Set tattoo image
        tattoos = []
        for tattoo in tattoos_db:
            tattoo.image = image_service.get_signed_url(tattoo.image)
            tattoos.append(json.loads(tattoo.to_json()))

        return tattoos
    
    def get_latest_tattoos_by_nickname(self, nickname: str) -> list[Tatto]:
        profile = profiles_service.get_by_nick(nickname)

        # Search
        tattoos_db = Tatto.objects(profile=profile.id).order_by('-date')[:6]
        # Set tattoo image
        tattoos = []
        for tattoo in tattoos_db:
            tattoo.image = image_service.get_signed_url(tattoo.image)
            tattoos.append(json.loads(tattoo.to_json()))

        return tattoos

    def _upload_tattoo(
        self,
        file: UploadFile,
        profile: Profile,
        categories: list,
    ) -> Tatto:
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

        tattoo = TattoBody(profile = str(profile.id), image = image_key, categories = categories)
        return Tatto(**tattoo.to_model()).save()

    def create_tattoo(self, files: list[UploadFile], categories: list, tokenData: TokenData) -> Tatto:
        profile = profiles_service.get_by_id_user(tokenData.id)

        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        result = []
        for category_slug in categories:
            category = categories_service.get_by_slug(category_slug)
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Category doesn't exists",
                )
            result.append(category.id)

        if len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid categories',  
            )
        # Upload all files to image repo
        tattoos = []
        with futures.ThreadPoolExecutor(10) as executor:
            futures_to_process = []
            for file in files:
                futures_to_process.append(
                    executor.submit(
                        self._upload_tattoo,
                        file,
                        profile,
                        result,
                    ),
                )
            for future in futures.as_completed(futures_to_process):
                tattoos.append(future.result())
        return tattoos

tattoos_service = Tattoos()
