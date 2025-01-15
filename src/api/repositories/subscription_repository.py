from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.session import get_session
from models.entity import SubscriptionModel, SubscriptionPlanModel, RoleModel, UserProfileModel

class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_plans(self):
        result = await self.session.execute(
            select(SubscriptionPlanModel)
        )

        return result.scalars().all()

    async def get_role_by_id(self, role_id: int):
        result = await self.session.execute(
            select(RoleModel)
            .where(RoleModel.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_executor_profile_by_id(self, auth_id: int):
        result = await self.session.execute(
            select(UserProfileModel)
            .where(UserProfileModel.auth_id == auth_id)
        )
        return result.scalar_one_or_none()

    async def get_history_subscribe_for_executor(self, user_id: int):
        result = await self.session.execute(
            select(SubscriptionModel)
            .options(joinedload(SubscriptionModel.plan))
            .where(SubscriptionModel.user_id == user_id)
        )
        return result.scalars().all()

def get_subscription_repository(session: AsyncSession = Depends(get_session)) -> SubscriptionRepository:
    return SubscriptionRepository(session)