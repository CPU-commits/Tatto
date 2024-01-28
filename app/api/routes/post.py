# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses
status = fastapi.status
from fastapi import Form, Query

# Interfaces
from app.dependencies import Res

import json
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
async def create_post(
                    #   tattos : list  = Form(...), 
                      content : str = Form(...),
                      tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    posts_service.create_post(content,tokenData)    
    return responses.JSONResponse(
        status_code=200,
        content = { 
            'success': True,
            'body': 'El post fue creado con exito',
        }
    )

@router.get(
    '/{nickname}',
    response_model=Res[str],
)
async def get_posts(nickname: str,page:int = Query(default=1,ge=1),items_per_page :int = Query(default=100,ge=1)) -> Res:
    inserted_posts = posts_service.get_posts_by_perfil(page,items_per_page,nickname)    

    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': {
                "posts" : inserted_posts
            },
        }
    )
