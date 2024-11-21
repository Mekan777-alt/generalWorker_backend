from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.session import get_session
from fastapi import Depends

from models.entity import AuthModel, RoleModel, CustomerProfileModel, ExecutorProfileModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_customer_profile(self, auth_id: int):
        new_profile = CustomerProfileModel(auth_id=auth_id)
        self.session.add(new_profile)
        await self.session.commit()
        await self.session.refresh(new_profile)
        return new_profile

    async def create_executor_profile(self, auth_id: int):
        new_profile = ExecutorProfileModel(auth_id=auth_id)
        self.session.add(new_profile)
        await self.session.commit()
        await self.session.refresh(new_profile)
        return new_profile

    async def get_role_by_id(self, role_id: int):
        result = await self.session.execute(
            select(RoleModel).where(RoleModel.id == role_id)
        )

        return result.scalar_one_or_none()

    async def get_customer_profile(self, auth_id: int):
        result = await self.session.execute(
            select(CustomerProfileModel).where(CustomerProfileModel.auth_id == auth_id)
        )

        return result.scalar_one_or_none()


    async def get_executor_profile(self, auth_id: int):
        result = await self.session.execute(
            select(ExecutorProfileModel).where(ExecutorProfileModel.auth_id == auth_id)
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
