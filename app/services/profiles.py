# Responses
import fastapi
from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from uuid import uuid4
from bson import json_util
import json
status = fastapi.status

# Models
from app.models.profile import Profile
from app.models.user import User
# Interfaces
from app.interfaces.profile import Profile as ProfileBody
from app.interfaces.profile import ProfileUpdate
from app.services.categories import categories_service
from app.services.files import files_service
# Token
from app.dependencies import TokenData

class Profiles():
    #Buscar perfil por el user id 
    def get_by_id_user(self, id: str) -> Profile | None:
        return Profile.objects(user=id).first()

    #Buscar perfil por nick
    def get_by_nick(self, nickname: str, return_json=False) -> Profile | None | str:
        profile: Profile = Profile.objects(nickname=nickname).first()
        # Set profile avatar
        profile.avatar = files_service.get_file(profile.avatar)

        if profile is not None and return_json is True:
            profile_data = profile.to_mongo()
            # Get user
            user = User.objects(id=profile.user.id).only('email', 'name').first()
            profile_data['user'] = user.to_mongo()

            return json.loads(json_util.dumps(profile_data))
        return profile

    #Crea un perfil al crear el usuario de tipo Tatuador b
    def create_profile(self,id : str, name : str) -> Profile:
        user_profile = ProfileBody(user = str(id), nickname = f'{name}-{uuid4().hex}')
        return Profile(**user_profile.to_model()).save()

    #Actualizar datos nickname, description o categories
    def update_profile(self,profileUpdate: ProfileUpdate,tokenData : TokenData) -> Profile:
        profile = self.get_by_id_user(tokenData.id)
        if profileUpdate.nickname is not None:
            profile.update(**{"nickname": profileUpdate.nickname})
        if profileUpdate.description is not None:
            profile.update(**{"description": profileUpdate.description})
        if profileUpdate.categories is not None:
            profile.update(**{"unset__categories": 1})
            for category in profileUpdate.categories:
                inserte_category = categories_service.get_by_name(category)
                if inserte_category is  None:  
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Not a valid category',
                    )
                profile.update(**{"push__categories" : inserte_category.id})
        return

    # Cambia el avatar del perfil. Retorna la URL de la imagen
    def update_avatar (self,file : UploadFile,tokenData : TokenData) -> str:
        profile = self.get_by_id_user(tokenData.id)
        type_split = file.content_type.split("/")
        type = type_split[len(type_split) - 1]

        if "image" not in file.content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid type',
            )
        image_key = files_service.upload_file(f"Avatars/{profile.nickname}_avatar-{str(uuid4())}.{type}",file)
        if profile is not None:
            profile.update(**{"avatar": image_key})
            # Delete and return file
            files_service.delete_file(profile.avatar)

            return files_service.get_file(image_key)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No existe el usuario',
            )

profiles_service = Profiles()
