# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses
status = fastapi.status
from fastapi import Form, Query,UploadFile

# Interfaces
from app.dependencies import Res

import json
# JWT
from app.dependencies import TokenData, UserTypes
# Services

from app.dependencies import auth_service
from app.services.posts import posts_service

from app.services.likes import likes_service
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
                    files: list[UploadFile] | None = None,
                    content : str = Form(...),
                    tokenData: TokenData = fastapi.Depends(auth_service.decode_token)) -> Res:
    posts_service.create_post(files,content,tokenData)    
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
async def get_posts(
    nickname: str,
    page: int = Query(default=1, ge=1),
    items_per_page: int = Query(default=10, ge=1),
    count: bool = Query(default=False),
) -> Res:
    inserted_posts = posts_service.get_posts_by_perfil(page,items_per_page,nickname)
    count_posts = 0
    if count:
        count_posts = posts_service.count_posts_profile(nickname)

    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': {
                "posts" : inserted_posts
            },
        },
        headers={
            'X-Count': str(count_posts),
        },
    )

@router.get(
    '/post/{id_post}',
    response_model=Res[str],
)
async def get_post(
    id_post: str,
    
) -> Res:
    inserted_post = posts_service.get_post_by_id(id_post,return_json=True)
    

    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': {
                "post" : inserted_post
            },
        },
    )

@router.post(
    '/like',
    response_model=Res[str],
    dependencies=[fastapi.Depends(auth_service.is_auth)]
)
async def like_post(
    id_post : str = Form(...),
    tokenData: TokenData = fastapi.Depends(auth_service.decode_token)
) -> Res:
    likes_service.like_post(id_post,tokenData)

    return responses.JSONResponse(
        status_code=200,
        content = {
            'success': True,
            'body': ""
        }
    )