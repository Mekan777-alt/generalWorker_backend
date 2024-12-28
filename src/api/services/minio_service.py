from typing import Type

from minio import Minio
from starlette import status
from fastapi import HTTPException, UploadFile
from core.config import settings


class MinioClient:
    client = Minio(
        endpoint=settings.s3_settings.s3_url,
        access_key=settings.s3_settings.s3_access_key,
        secret_key=settings.s3_settings.s3_secret_key,
        secure=False
    )

    @classmethod
    def upload_photo(cls, prefix: str, user: str, image: UploadFile):
        bucket_name = settings.s3_settings.s3_bucket_name
        bucket_exists = cls.client.bucket_exists(bucket_name)

        if not bucket_exists:
            raise HTTPException(
                detail=f"Bucket {bucket_name} does not exist",
                status_code=status.HTTP_404_NOT_FOUND
            )

        file_path = f"{user}/{prefix}/{image.filename}"
        try:
            cls.client.put_object(
                bucket_name=bucket_name,
                object_name=file_path,
                data=image.file,  # Передаем файловый объект
                length=-1,  # Указываем длину как -1 для работы с потоками
                part_size=10 * 1024 * 1024  # Размер частей (10 MB)
            )
        except Exception as e:
            raise HTTPException(
                detail=f"Failed to upload file to MinIO: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return file_path

def get_minio_client() -> Type[MinioClient]:
    return MinioClient