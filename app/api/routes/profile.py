# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses
status = fastapi.status
from fastapi import UploadFile

# Interfaces
from app.dependencies import Res
from app.interfaces.profile import ProfileUpdate


# JWT
from app.dependencies import TokenData, UserTypes
# Services

from app.dependencies import auth_service
from app.services.profiles import profiles_service
# Settings

from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/profiles',
)

@router.patch(
    '/update',
    response_model=Res[None],
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST])),
    ],
)
async def update_profile(profileUpdate: ProfileUpdate ,tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    profiles_service.update_profile(profileUpdate,tokenData)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': '',
        }
    )

@router.patch(
    '/avatar',
    response_model=Res[None],
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST])),
    ],
)
async def update_avatar(
    avatar: UploadFile,
    tokenData: TokenData = fastapi.Depends(auth_service.decode_token),
) -> Res:
    img_url = profiles_service.update_avatar(avatar,tokenData)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': img_url,
        }
    )

@router.get(
    '/{nickname}',
    response_model=Res[str],
    dependencies=[],
)
async def perfil(nickname : str) -> Res:
    profile = profiles_service.get_by_nick(nickname, return_json=True)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': profile
        }
    )
