# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
from app.interfaces.auth import Auth
from app.interfaces.token import TokenRes
# Services
from app.dependencies import auth_service
# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/auth',
)

@router.post(
    '',
    response_model=Res[TokenRes],
)
async def login(auth: Auth) -> Res:
    token = auth_service.login(auth)
    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            'success': True,
            'body': token.dict(),
        }
    )
