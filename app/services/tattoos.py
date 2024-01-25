# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
status = fastapi.status
from uuid import uuid4
from bson import json_util
import json

# Models
from app.models.tatto import Tatto
# Interfaces
from app.interfaces.tatto import Tatto as TattoBody
# Services
from app.services.categories import categories_service
from app.services.files import files_service
from app.services.profiles import profiles_service
# Token
from app.dependencies import TokenData

class Tattoos():
    def get_by_id(self,id : str) -> Tatto | None:
        return Tatto.objects(id=id).first()

    def get_tattoos_by_nickname(self, nickname: str) -> Tatto:
        profile = profiles_service.get_by_nick(nickname)

        return json.loads(
            json_util.dumps(Tatto.objects(profile=profile.id).order_by('-date')),
        )

    def create_tattoo(self, files: list[UploadFile], categories: list, tokenData: TokenData) -> Tatto:
        profile = profiles_service.get_by_id_user(tokenData.id)
        inserted_categories = categories_service.get_categories().only("name").to_json()
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        result = []
        for category in categories:
            if category in inserted_categories:
                result.append(categories_service.get_by_name(category))
        if len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid categories',
            )
        tattoos = []
        for file in files:
            type_split = file.content_type.split("/")
            type = type_split[len(type_split) - 1]

            if "image" not in type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Not valid types',
                )
            photo = files_service.upload_file(f"Tattoos/{uuid4().hex}.{type}",file)
            tattoo = TattoBody(profile = str(profile.id), image = f"api/{photo}", categories = result)
            tattoos.append(Tatto(**tattoo.to_model()).save())

        return tattoos

tattoos_service = Tattoos()
