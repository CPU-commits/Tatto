# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
from app.dependencies import UserTypes
from app.dependencies import TokenData
from app.interfaces.block import CalendarBlock
# Services
from app.services.calendar import calendar_service
from app.services.auth import auth_service
# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/calendars',
)

@router.get(
    '',
    response_model=Res[None],
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST])),
    ],
)
async def get_settings(tokenData: TokenData = fastapi.Depends(auth_service.decode_token)):
    calendar = calendar_service.get_calendar(
        tokenData.id,
    )
    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'body': calendar,
        },
    )

@router.post(
    '/blocks',
    response_model=Res[None],
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST])),
    ],
)
async def add_calendar_blocks(
    calendar_block: CalendarBlock,
    token_data: TokenData = fastapi.Depends(auth_service.decode_token),
):
    calendar = calendar_service.add_calendar_block(
        calendar_block,
        token_data.id,
    )
    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'success': True,
            'body': calendar,
        },
    )
