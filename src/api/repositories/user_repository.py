from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.session import get_session
from fastapi import Depends

from models import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_info_by_uid(self, uid: str) -> Users:
        result = await self.session.execute(select(Users).where(Users.firebase_uid == uid))
        return result.scalar_one_or_none()

    async def update_user_info(self, user: Users) -> Users:
        await self.session.commit()
        await self.session.refresh(user)
        return user

def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
