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
from app.services.posts import posts_service
# Settings

from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/posts',
)

@router.post(
    '',
    response_model=Res[None],
    dependencies=[fastapi.Depends(auth_service.is_auth),fastapi.Depends(auth_service.roles([UserTypes.TATTO_ARTIST]))],

)
async def create_post(files : list[UploadFile] = None ,
                      tattos : list  = Form(...), 
                      categories : list = Form(...),
                      content : str = Form(...) ,
                      tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    posts_service.create_post(files,tattos,categories,content,tokenData)    
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': '',
        }
    )

@router.get(
    '/{nickname}',
    response_model=Res[str],
    dependencies=[],

)
async def create_post(nickname: str)     -> Res:
    inserted_posts = posts_service.get_posts_by_perfil(nickname)    
    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': inserted_posts,
        }
    )

