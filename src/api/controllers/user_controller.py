from fastapi import APIRouter, Depends
from typing import Annotated
from api.dto.user_dto import UserResponseDTO, UserPartialUpdateDTO

from api.dependency.current_user import get_user_from_token
from starlette import status
from api.services.user_service import get_user_service, UserService

router = APIRouter(
    tags=['Пользователи'],
    prefix='/api',
)

@router.get('/user', status_code=status.HTTP_200_OK, summary="Возвращает информацию о пользователе",
            response_model=UserResponseDTO)
async def get_me_info(current_user: Annotated[dict, Depends(get_user_from_token)],
                    service: UserService = Depends(get_user_service)):
    return await service.get_user_info_service(current_user)


@router.patch('/user', status_code=status.HTTP_200_OK, response_model=UserResponseDTO,
              summary="Частичное обновление информации о пользователе")
async def partial_update_user(current_user: Annotated[dict, Depends(get_user_from_token)],
                              data: UserPartialUpdateDTO,
                              service: UserService = Depends(get_user_service)):
    return await service.partial_update_service(current_user, data)