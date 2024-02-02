# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
from app.interfaces.category import Category
# JWT
from app.dependencies import UserTypes
# FastAPI
# Services
from app.services.categories import categories_service
from app.services.auth import auth_service
# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/categories',
)

@router.get(
    '',
    response_model=Res[str],
    response_description='Obtener todas las categorías',
)
async def get_categories():
    categories = categories_service.get_categories()

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'body': {
                'categories': categories,
            },
        },
    )

@router.post(
    '',
    response_model=Res[str],
    response_description='Crear categoria',
    dependencies=[
        fastapi.Depends(auth_service.is_auth),
        fastapi.Depends(auth_service.roles([UserTypes.ADMIN])),
    ],
)
async def create_category(category: Category):
    inserted_category = categories_service.create_category(category)

    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'success': True,
            'body': str(inserted_category),
        },
    )
