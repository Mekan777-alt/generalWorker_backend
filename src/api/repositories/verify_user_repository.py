from models import Users
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

class VerifyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user_by_uid(self, uid: str) -> Users:
        result = await self.session.execute(select(Users).where(Users.firebase_uid == uid))

        return result.scalar_one_or_none()

    async def create_user(self, user: Users) -> Users:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user


def get_verify_user_repository(session: AsyncSession = Depends(get_session)) -> VerifyUserRepository:
    return VerifyUserRepository(session)
