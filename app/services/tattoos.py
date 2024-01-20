# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
status = fastapi.status
from uuid import uuid4

# Models

from app.models.tatto import Tatto
# Interfaces
from app.interfaces.tatto import Tatto as TattoBody

from app.services.categories import categories_service
from app.services.files import files_service
from app.services.profiles import profiles_service

# Token
from app.dependencies import TokenData

class Tattoos():
    def get_by_id(self,id : str) -> Tatto | None:
        return Tatto.objects(id=id).first()
    def get_tattoos_by_profile(self, id : str) -> Tatto :
        return Tatto.objects(profile=id)

    def create_tatto(self,files : list[UploadFile],categories:list, tokenData : TokenData) -> Tatto:
        profile = profiles_service.get_by_id_user(tokenData.id)
        inserted_categories = categories_service.get_categories().only("name").to_json()
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid profile',
            )
        result = []
        for x in categories:
            if x in inserted_categories:
                result.append(categories_service.get_by_name(x))
        if len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid categories',
            )
        tattoos = []
        for file in files:
            type = file.content_type.split("/")[1]
            valid_type = ["jpg","png"]
            
            if type not in valid_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Not valid types',
                )
            photo = files_service.upload_file(f"Tattoos/{uuid4().hex}.{type}",file)
            tatto = TattoBody(profile = str(profile.id), image = f"api/{photo}", categories = result)
            tattoos.append(Tatto(**tatto.to_model()).save())
        
        return tattoos

        

tattoos_service = Tattoos()