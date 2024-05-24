# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
from app.interfaces.user import User, UserUpdate
# JWT
from app.dependencies import TokenData, UserTypes
# Services
from app.dependencies import auth_service
from app.services.users import users_service
# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/users',
)

@router.post(
    '',
    response_model=Res[str],
    response_description='El ID del dato insertado',
)
async def register(user: User):
    inserted_user = users_service.register(user)

    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'success': True,
            'body': str(inserted_user),
        },
    )

@router.post(
    '/x',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth),fastapi.Depends(auth_service.roles([UserTypes.STUDIO_OWNER]))],

)
async def get(tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    users = users_service.get_users()
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': users,
        }
    )

# Actualizar datos Email o contraseña
#Dejar como /user/update o /update?
@router.patch(
    '/update',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth)],

)
async def update(userUpdate : UserUpdate,tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    users_service.update(userUpdate,tokenData)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': '',
        }
    )

#Actualizar el estado del usuario 
#Dejar como /user/state o /state?
@router.patch(
    '/user/state',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth)],

)
async def update(userUpdate : UserUpdate,tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    users_service.state(userUpdate,tokenData)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': '',
        }
    )
