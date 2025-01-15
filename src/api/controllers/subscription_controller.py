from typing import Annotated, List
from api.dependency.current_user import get_user_from_token
from fastapi import Depends, APIRouter

from api.dto.subscription_dto import SubscriptionHistoryResponseDTO
from api.services.subscription_service import get_subscription_service, SubscriptionService
from starlette import status

router = APIRouter(
    tags=["Подписка"]
)

@router.get("/subscription/plan",
            status_code=status.HTTP_200_OK,
            summary="Планы подписок")
async def subscription_plan(service: SubscriptionService = Depends(get_subscription_service)):
    return await service.subscribe_plan_service()


@router.get("/subscription/history",
            status_code=status.HTTP_200_OK,
            summary="История покупок",
            response_model=List[SubscriptionHistoryResponseDTO])
async def subscription_history(current_user: Annotated[dict, Depends(get_user_from_token)],
                               service: SubscriptionService = Depends(get_subscription_service)):
    return await service.subscribe_history_executor_history(current_user)