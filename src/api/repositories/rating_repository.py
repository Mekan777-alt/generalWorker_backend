from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.session import get_session
from models.entity import RoleModel
from sqlalchemy import select


class RatingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role_by_id(self, role_id: int):
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.id == role_id)
        )

        return result.scalar_one_or_none()

def get_rating_repository(session: AsyncSession = Depends(get_session)) -> RatingRepository:
    return RatingRepository(session)
