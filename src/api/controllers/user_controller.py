from fastapi import APIRouter, Depends, Form, UploadFile, File
from typing import Annotated, Optional
from api.dto.user_dto import UserResponseDTO
from api.dependency.current_user import get_user_from_token
from starlette import status
from api.services.user_service import get_user_service, UserService

router = APIRouter(
    tags=['Пользователи']
)

@router.get('/user', status_code=status.HTTP_200_OK, summary="Возвращает информацию о пользователе",
            response_model=UserResponseDTO)
async def get_me_info_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                    service: UserService = Depends(get_user_service)):
    return await service.get_user_info_service(current_user)


@router.patch('/user', status_code=status.HTTP_200_OK, response_model=UserResponseDTO,
              summary="Частичное обновление информации о пользователе")
async def partial_update_user_endpoint(
    current_user: Annotated[dict, Depends(get_user_from_token)],
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    about_my_self: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    service: UserService = Depends(get_user_service)
):
    return await service.partial_update_service(current_user=current_user,
                                                first_name=first_name,
                                                last_name=last_name,
                                                phone=phone_number,
                                                location=location,
                                                about_my_self=about_my_self,
                                                photo=photo
                                                )