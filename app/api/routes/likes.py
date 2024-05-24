# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
# Services
from app.services.likes import likes_service
from app.dependencies import auth_service
#jwt
from app.dependencies import TokenData

# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/likes',
)

@router.get(
    '',
    response_model=Res[str],
    dependencies=[fastapi.Depends(auth_service.is_auth)]
)
async def get_likes_user(
    tokenData: TokenData = fastapi.Depends(auth_service.decode_token)
) -> Res:
    likes = likes_service.get_likes_by_user(tokenData.id,return_json=True)

    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': {
                "likes" : likes
            }
        }
    )