from sqlalchemy.orm import selectinload, joinedload
from database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import List
from models.entity import AuthModel, RoleModel, UserRolesModel, UserProfileModel


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_profile_by_auth_id(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .where(UserProfileModel.auth_id == auth_id)
        )
        return result.scalar_one_or_none()

    async def get_auth_and_role_id_model(self, auth_id: int, role_id: int):
        result = await self.session.execute(
            select(UserRolesModel).where(UserRolesModel.user_id == auth_id,
                                         UserRolesModel.role_id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_role_by_name(self, role_name: str):
        result = await self.session.execute(select(RoleModel).where(RoleModel.name == role_name))
        return result.scalar_one_or_none()

    async def update_roles(self, model: UserRolesModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_role_by_id(self, role_id: int):
        result = await self.session.execute(select(RoleModel).where(RoleModel.id == role_id))
        return result.scalar_one_or_none()

    async def get_auth_roles(self, profile_id: int):
        result = await self.session.execute(
            select(UserRolesModel)
            .where(UserRolesModel.user_id == profile_id,
                   UserRolesModel.is_use == True))
        return result.scalar_one_or_none()

    async def create_role_to_user(self, models: List[UserRolesModel]):
        self.session.add_all(models)
        await self.session.commit()

    async def get_roles(self):
        result = await self.session.execute(select(RoleModel))
        return result.scalars()

    async def get_auth_with_user(self, auth_id: int):
        result = await self.session.execute(
            select(AuthModel)
            .options(selectinload(AuthModel.user))
            .where(AuthModel.id == auth_id)
        )
        return result.scalar_one_or_none()

    async def check_user_from_token(self, auth_id: int, phone_number: str) -> AuthModel:
        result = await self.session.execute(
            select(AuthModel).where(
                AuthModel.id == auth_id,
                AuthModel.phoneNumber == phone_number
            )
        )
        return result.scalar_one_or_none()

    async def check_user_phone(self, encrypted_phone_number: str) -> AuthModel:
        result = await self.session.execute(
            select(AuthModel).where(
                AuthModel.phoneNumber == encrypted_phone_number,
                AuthModel.isActive == True
            )
        )
        return result.scalar_one_or_none()

    async def get_user_by_verify_code(self, verify_code: str) -> AuthModel:
        result = await self.session.execute(
            select(AuthModel)
            .options(joinedload(AuthModel.user_profile))
            .where(AuthModel.otpCode == verify_code)
        )
        return result.scalar_one_or_none()

    async def get_user_by_phone_number(self, phone_number: str) -> AuthModel:
        result = await self.session.execute(
            select(AuthModel)
            .options(
                joinedload(AuthModel.user_profile)
                .joinedload(UserProfileModel.user_roles)
                .joinedload(UserRolesModel.role)
            )
            .where(AuthModel.phoneNumber == phone_number)
        )
        return result.unique().scalar_one_or_none()

    async def update_user(self, model: AuthModel):
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def create_user(self, model: AuthModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def create_profile(self, model: UserProfileModel):
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

def get_auth_repository(session: AsyncSession = Depends(get_session)) -> AuthRepository:
    return AuthRepository(session)
