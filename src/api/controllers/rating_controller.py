from fastapi import Depends, APIRouter
from starlette import status
from typing import Annotated
from api.services.rating_service import get_rating_service, RatingService
from api.dependency.current_user import get_user_from_token

router = APIRouter(
    tags=['Рейтинг заказчика и исполнителя']
)

@router.get('/rating',
            status_code=status.HTTP_200_OK,
            summary="Возвращает рейтинг пользователя в зависимости от переданного токена"
            )
async def get_rating_by_user_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
        service: RatingService = Depends(get_rating_service)):
    return await service.get_rating_current_user(current_user)