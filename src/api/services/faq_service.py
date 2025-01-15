from typing import Optional, List
from starlette import status
from api.repositories.auth_repository import AuthRepository, get_auth_repository
from api.repositories.faq_repository import FAQRepository, get_faqs_repository
from api.dto.faq_dto import FAQResponseDTO
from fastapi import Depends, UploadFile, HTTPException

from api.services.minio_service import MinioClient
from core.config import settings
from models.entity import QuestionRequestModel, QuestionRequestPhotoModel


class FAQService:
    def __init__(self, faq_repository: FAQRepository, auth_repository: AuthRepository):
        self.faq_repository = faq_repository
        self.auth_repository = auth_repository

    async def get_faqs_service(self):
        faqs = await self.faq_repository.get_faqs()

        return [FAQResponseDTO(
            question=faq.question,
            answer=faq.answer
        ) for faq in faqs]

    async def create_faqs_service(self, text: str,
                                  files: List[Optional[UploadFile]],
                                  minio_client: MinioClient,
                                  current_user: dict):
        auth_id = int(current_user.get("id"))

        profile = await self.auth_repository.get_profile_by_auth_id(auth_id)

        if not profile:
            raise HTTPException(
                detail="Пользователь не найден",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        new_question = QuestionRequestModel(
            question=text,
            user_id=profile.id
        )
        await self.faq_repository.create_question(new_question)

        photo_array = []
        for file in files:
            photo_uri = minio_client.upload_photo(prefix="question", user=str(profile.id), image=file)

            photo = QuestionRequestPhotoModel(
                question_id=new_question.id,
                photo_url=f"http://{settings.s3_settings.s3_url}/{settings.s3_settings.s3_bucket_name}/{photo_uri}"
            )
            photo_array.append(photo)

        await self.faq_repository.add_photo(photo_array)

        return {"message": "OK"}


def get_faqs_service(faq_repository: FAQRepository = Depends(get_faqs_repository),
                     auth_repository: AuthRepository = Depends(get_auth_repository)) -> FAQService:
    return FAQService(faq_repository, auth_repository)