# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses
status = fastapi.status
from fastapi import Form,UploadFile

# Interfaces
from app.dependencies import Res


# JWT
from app.dependencies import TokenData, UserTypes
# Services

from app.dependencies import auth_service
from app.services.tattoos import tattoos_service
# Settings

from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/tattoos',
)

@router.get(
    '/user/{nickname}',
)
async def get_user_tattoos(
    nickname: str,
    page: int | None = 0,
    count: bool | None = False,
) -> Res:
    tattoos = tattoos_service.get_tattoos_by_nickname(nickname, page)
    total_tattoos = None
    if count:
        total_tattoos = tattoos_service.count_max_tattoos(nickname)

    return responses.JSONResponse(
        status_code=200,
        content={
            'success': True,
            'body': {
                'tattoos': tattoos,
            },
        },
        headers={
            'X-Count': str(total_tattoos if total_tattoos is not None else 0),
        },
    )

@router.get(
    '/user/{nickname}/latest',
)
async def get_latest_user_tattoos(nickname: str) -> Res:
    tattoos = tattoos_service.get_latest_tattoos_by_nickname(nickname)
    return responses.JSONResponse(
        status_code=200,
        content={
            'success': True,
            'body': {
                'tattoos': tattoos,
            },
        },
    )

@router.post(
    '',
    response_model=Res[None],
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST])),
    ],
)
async def create_tattoo(
    files: list[UploadFile],
    categories: list = Form(...),
    tokenData: TokenData = fastapi.Depends(auth_service.decode_token),
) -> Res:
    tattoos_service.create_tattoo(files,categories,tokenData)
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': '',
        }
    )
