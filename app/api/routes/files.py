# FastAPI
from app.dependencies import fastapi
from app.dependencies import responses

status = fastapi.status
# Interfaces
from app.dependencies import Res
# FastAPI
from starlette.background import BackgroundTasks
# Services
from app.services.files import files_service
# Settings
from app.core.config import configuration

router = fastapi.APIRouter(
    prefix=f'{configuration.default_api}/files',
)

@router.get(
    '/{key}',
    response_class=responses.FileResponse,
    response_description='Download file from AWS S3',
)
def get_file(key: str, background_tasks: BackgroundTasks):
    file = files_service.get_file(key)

    background_tasks.add_task(file.remove_file)
    return responses.FileResponse(
        file.get_path(),
        filename=file.get_filename(),
    )
