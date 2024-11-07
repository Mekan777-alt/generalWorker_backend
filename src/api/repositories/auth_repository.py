from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from models import Users

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user_phone(self, encrypted_phone_number: str) -> Users:
        user = await self.session.execute(
            select(Users).where(
                Users.phoneNumber == encrypted_phone_number,
                Users.isRegistered == True,
                Users.isActive == True
            ).limit(1)
        )
        return user.scalar_one_or_none()

    async def get_user_by_verify_code(self, verify_code: str) -> Users:
        user = await self.session.execute(select(Users).where(Users.verifyCode == verify_code))
        return user.scalar_one_or_none()

    async def get_user_by_phone_number(self, phone_number: str) -> Users:
        result = await self.session.execute(
            select(Users).where(Users.phoneNumber == phone_number)
        )
        return result.scalar_one_or_none()

    async def update_user(self, user: Users):
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_user(self, user: Users):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


def get_auth_repository(session: AsyncSession = Depends(get_session)) -> AuthRepository:
    return AuthRepository(session)
