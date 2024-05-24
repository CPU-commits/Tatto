# Responses
import fastapi
from fastapi.exceptions import HTTPException
import bcrypt

status = fastapi.status
# Models
from app.models.user import User
# Interfaces
from app.interfaces.user import UserUpdate,User as UserBody
from app.interfaces.profile import Profile as ProfileBody
#User types
from app.interfaces.user_types import UserStates,UserTypes

from app.dependencies import TokenData
#Services
from app.services.profiles import profiles_service

class Users():
    def get_by_email(self, email: str) -> User | None:
        return User.objects(email=email).first()
    
    def get_by_id(self, id: str) -> User | None:
        return User.objects(id=id).first()

    def register(self, user: UserBody) -> User:
        valid_users = [
            UserTypes.CLIENT.value,
            UserTypes.TATTO_ARTIST.value,
            UserTypes.ADMIN.value,
        ]
        if user.role not in valid_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Not valid role',
            )
        # Exists user
        exists_user = User.objects(email=user.email).only('id').first()
        if exists_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='El usuario ya está registrado',
            )

        inserted_user = User(**user.to_model()).save()

        if user.role == UserTypes.TATTO_ARTIST.value:
            profiles_service.create_profile(inserted_user.id,inserted_user.name)
        return inserted_user.id
    

    def update(self, userUpdate: UserUpdate,tokenData : TokenData):
        valid_methods = ['email', 'password']
        if userUpdate.method not in valid_methods:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not a valid method',
            )
        user = self.get_by_id(tokenData.id)
        if userUpdate.method == 'email':
            user.update(**{userUpdate.method: userUpdate.data})
        else:
            is_pass = bcrypt.checkpw(
                bytes(userUpdate.data, 'utf-8'),
                bytes(user.password, 'utf-8'),
            )
            if is_pass is True:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='The password must not be the same as the previous one',
                )
            password = bcrypt.hashpw(
                password=bytes(userUpdate.data, 'utf-8'),
                salt=bcrypt.gensalt(),
            ).decode('utf-8')
            user.update(**{userUpdate.method: password})
            return user.reload()
        
    #Cambia el estado recibe  method : state 
    def state(self,userUpdate : UserUpdate,tokenData: TokenData):
        user = self.get_by_id(tokenData.id)
        if user.state == UserStates.ACTIVE:
            return user.update(**{userUpdate.method: UserStates.DISABLED})
        elif user.state == UserStates.DISABLED: 
            return user.update(**{userUpdate.method: UserStates.ACTIVE})

        

users_service = Users()
