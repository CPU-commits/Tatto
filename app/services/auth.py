from app.dependencies import settings
from app.core.config import configuration
from app.dependencies import typing
from app.dependencies import jwt, JWTError
from app.dependencies import security
from app.dependencies import exceptions
from app.dependencies import status
from app.dependencies import TokenData, UserTypes
import bcrypt
# FastAPI
from app.dependencies import fastapi
from app.dependencies import context
from datetime import datetime, timedelta
# Services
from app.services.users import users_service
from app.services.profiles import profiles_service
# Interfaces
from app.interfaces.auth import Auth as AuthBody
from app.interfaces.token import TokenRes


schema = security.OAuth2PasswordBearer(
    tokenUrl="token",
)

class Auth():
    TOKEN_DATA_KEY = 'token_data'
    _exception = exceptions.HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )

    async def is_auth(self, token: str = fastapi.Depends(schema)) -> None:
        try:
            payload = jwt.decode(
                token.replace('Bearer ', ''),
                settings.JWT_SECRET_KEY,
                algorithms=[configuration.jwt_algotithm],
            )
            context.setdefault(
                self.TOKEN_DATA_KEY,
                TokenData(
                    user_type=UserTypes(payload['user_type']),
                    id=payload['id'],
                    sub=payload['sub']
                ),
            )
        except JWTError:
            raise self._exception
    
    def roles(self, roles: typing.List[str]):
        
        def manageRoles():
            tokenData: TokenData = context.data.get(self.TOKEN_DATA_KEY)
            if all(role != tokenData.user_type for role in roles):
                raise self._exception
        return manageRoles

    def decode_token(self, token: str = fastapi.Depends(schema)) -> TokenData:
        return context.data.get(self.TOKEN_DATA_KEY)
    
    def __create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=configuration.access_token_expire_minutes)
        to_encode.update({ 'exp': expire ,'sub' : "jwtTokenTatto"})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=configuration.jwt_algotithm,
        )
        return encoded_jwt

    def login(self, auth: AuthBody) -> TokenRes:
        user = users_service.get_by_email(auth.email)
        if user is None:
            raise exceptions.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email o contraseña no coinciden',
            )
        is_pass = bcrypt.checkpw(
            bytes(auth.password, 'utf-8'),
            bytes(user.password, 'utf-8'),
        )
        if is_pass is False:
            raise exceptions.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email o contraseña no coinciden',
            )
        # If user is tatto artist get profile
        nickname = user.name
        if user.role.value is UserTypes.TATTO_ARTIST.value:
            profile = profiles_service.get_by_id_user(user.id)
            nickname = profile.nickname
        # Build token
        return TokenRes(
            token=self.__create_access_token(
                { 'id': str(user.id), 'user_type': user.role.value },
            ),
            user={
                'email': user.email,
                'name': user.name,
                'id': str(user.id),
                'role': user.role.value,
                'nickname': nickname,
            },
        )

auth_service = Auth()
