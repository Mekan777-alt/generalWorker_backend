from grpc import services
from starlette import status

from api.dto.subscription_dto import SubscriptionHistoryResponseDTO
from models.enums import RolesEnum
from api.repositories.subscription_repository import get_subscription_repository, SubscriptionRepository
from fastapi import Depends, HTTPException

class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository):
        self.subscription_repository = subscription_repository

    async def _get_executor_profile(self, role_id: int, auth_id: int):
        role = await self.subscription_repository.get_role_by_id(role_id)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Роль не найдена",
            )

        if role.name == RolesEnum.EXECUTOR.value:
            return await self.subscription_repository.get_executor_profile_by_id(auth_id)
        else:
            raise HTTPException(
                detail="Авторизуйтесь как исполнитель",
                status_code=status.HTTP_400_BAD_REQUEST
            )


    async def subscribe_plan_service(self):
        return await self.subscription_repository.get_plans()

    async def subscribe_history_executor_history(self, current_user: dict):
        role_id = current_user.get("role_id")
        auth_id = current_user.get("id")

        profile = await self._get_executor_profile(role_id, auth_id)

        history = await self.subscription_repository.get_history_subscribe_for_executor(profile.id)

        return [SubscriptionHistoryResponseDTO(
            price=f"{history.plan.price} ₽",
            create_date=history.start_date.date().strftime("%d.%m.%Y"),
        ) for history in history]


def get_subscription_service(subscription_repository: SubscriptionRepository = Depends(get_subscription_repository)):
    return SubscriptionService(subscription_repository)