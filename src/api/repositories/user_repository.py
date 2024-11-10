from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.session import get_session
from fastapi import Depends

from models.entity import UsersModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_info_by_uid(self, user_id: int) -> UsersModel:
        result = await self.session.execute(select(UsersModel).where(UsersModel.firebase_uid == uid))
        return result.scalar_one_or_none()

    async def update_user_info(self, user: UsersModel) -> UsersModel:
        await self.session.commit()
        await self.session.refresh(user)
        return user

def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
