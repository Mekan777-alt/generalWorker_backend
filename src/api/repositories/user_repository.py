from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.session import get_session
from fastapi import Depends

from models.entity import UsersModel, AuthModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_phone_number(self, auth_id: int):
        result = await self.session.execute(select(AuthModel).where(AuthModel.id == auth_id))
        return result.scalar_one_or_none()

    async def get_user_info(self, auth_id: int):
        result = await self.session.execute(select(UsersModel).where(UsersModel.auth_id == auth_id))
        return result.scalar_one_or_none()


    async def update_user_info(self, user: UsersModel) -> UsersModel:
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_auth_model(self, model: AuthModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
