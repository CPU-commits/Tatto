import uuid
import os
# AWS S3
import boto3
# Settings
from app.core.settings import settings
# FastAPI
import fastapi
from fastapi import UploadFile
from fastapi.exceptions import HTTPException

status = fastapi.status

# AWS
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)
bucket = settings.AWS_BUCKET

class Files():
    def __init__(self) -> None:
        s3_client.put_bucket_cors(
            Bucket=bucket,
            CORSConfiguration={
                "CORSRules": [
                    {
                        "ID": "tatto",
                        "AllowedHeaders": [
                            "*"
                        ],
                        "AllowedMethods": [
                            "GET"
                        ],
                        "AllowedOrigins": [
                            "*"
                        ],
                        "ExposeHeaders": []
                    },
                ],
            },
        )

    def upload_file(self, key: str, file: UploadFile) -> str:
        try:
            file.file.seek(0)
            s3_client.upload_fileobj(file.file, bucket, key)
            return key
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='No se pudo subir el archivo',
            )
        finally:
            file.file.close()

    def get_file(self, key: str) -> str:
        try:
            return s3_client.generate_presigned_url(
                "get_object",
                ExpiresIn=60 * 5,
                Params={
                    "Bucket": bucket,
                    "Key": key,
                },
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='No se encontró el archivo',
            )

    def delete_file(self, key: str) -> str:
        try:
            s3_client.delete_object(
                Bucket=bucket,
                Key=key,
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail='No se pudo eliminar el archivo',
            )

files_service = Files()
