from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.session import get_session
from fastapi import Depends
from models.entity import FAQModel, QuestionRequestModel, QuestionRequestPhotoModel


class FAQRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_faqs(self):
        result = await self.session.execute(
            select(FAQModel)
        )
        return result.scalars().all()

    async def create_question(self, model: QuestionRequestModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def add_photo(self, models: List[QuestionRequestPhotoModel]):
        self.session.add_all(models)
        await self.session.commit()

def get_faqs_repository(session: AsyncSession = Depends(get_session)) -> FAQRepository:
    return FAQRepository(session)
