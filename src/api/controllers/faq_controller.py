from typing import List, Optional, Annotated
from api.services.faq_service import FAQService, get_faqs_service
from api.dependency.current_user import get_user_from_token
from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from api.dto.faq_dto import FAQResponseDTO
from api.services.minio_service import MinioClient, get_minio_client

router = APIRouter(
    tags=["Помощь"],
)

@router.get(
    "/faqs",
    summary="Возвращает массив вопросов и ответов",
    status_code=status.HTTP_200_OK,
    response_model=List[FAQResponseDTO]
)
async def get_help_array_endpoint(service: FAQService = Depends(get_faqs_service)):
    return await service.get_faqs_service()


@router.post(
    "/faqs",
    summary="Отправить обратную связь",
    status_code=status.HTTP_201_CREATED,
)
async def send_faq_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                            text: str = Form(...),
                            files: Optional[List[UploadFile]] = File(None),
                            service: FAQService = Depends(get_faqs_service),
                            minio_client: MinioClient = Depends(get_minio_client)):
    return await service.create_faqs_service(text, files, minio_client, current_user)
