from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from database.session import get_session
from fastapi import Depends

from models.entity import AuthModel, RoleModel, UserProfileModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, auth_id: int):
        result = await self.session.execute(
            select(AuthModel)
            .where(AuthModel.id == auth_id)
        )
        return result.scalar_one_or_none()

    async def delete_user(self, auth_id: int):
        await self.session.execute(
            delete(AuthModel)
            .where(AuthModel.id == auth_id)
        )
        await self.session.commit()

    async def get_role_by_id(self, role_id: int):
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.id == role_id)
        )

        return result.scalar_one_or_none()

    async def get_customer_profile(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel).where(UserProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()

    async def get_customer_by_id(self, customer_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .options(joinedload(UserProfileModel.auth))
            .where(UserProfileModel.id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_executor_by_id(self, executor_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .options(joinedload(UserProfileModel.auth))
            .where(UserProfileModel.id == executor_id)
        )
        return result.scalar_one_or_none()

    async def get_executor_profile(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .where(UserProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()

    async def get_phone_number(self, auth_id: int):
        result = await self.session.execute(
            select(AuthModel).where(AuthModel.id == auth_id)
        )

        return result.scalar_one_or_none()

    async def update_user_info(self, model):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def update_auth_model(self, model: AuthModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
