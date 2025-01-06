from fastapi import APIRouter, Depends, Form, UploadFile, File, Path
from typing import Annotated, Optional

from api.dto.user_dto import UserResponseDTO, ExecutorRatingDTO, CustomerRatingDTO
from api.dependency.current_user import get_user_from_token
from starlette import status

from api.services.minio_service import MinioClient, get_minio_client
from api.services.user_service import get_user_service, UserService

router = APIRouter(
    tags=['Пользователи']
)

@router.get('/user',
            status_code=status.HTTP_200_OK,
            summary="Возвращает информацию о пользователе",
            response_model=UserResponseDTO)
async def get_me_info_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                    service: UserService = Depends(get_user_service)):
    return await service.get_user_info_service(current_user)


@router.patch('/user',
              status_code=status.HTTP_200_OK,
              response_model=UserResponseDTO,
              summary="Частичное обновление информации о пользователе")
async def partial_update_user_endpoint(
    current_user: Annotated[dict, Depends(get_user_from_token)],
    firstName: Optional[str] = Form(None),
    lastName: Optional[str] = Form(None),
    phoneNumber: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    aboutMySelf: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    service: UserService = Depends(get_user_service),
    minio_client: MinioClient = Depends(get_minio_client)
):
    return await service.partial_update_service(current_user=current_user,
                                                first_name=firstName,
                                                last_name=lastName,
                                                phone=phoneNumber,
                                                location=location,
                                                about_my_self=aboutMySelf,
                                                photo=photo,
                                                minio_client=minio_client
                                                )

@router.get(
    "/user/executor/rating",
    status_code=status.HTTP_200_OK,
    summary="Рейтинг исполнителя",
    response_model=ExecutorRatingDTO
)
async def get_rating_by_executor_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                                 service: UserService = Depends(get_user_service)):
    return await service.get_executor_rating(current_user)

@router.get(
    "/user/customer/rating",
    status_code=status.HTTP_200_OK,
    summary="Рейтинг заказчика",
    response_model=CustomerRatingDTO
)
async def get_rating_by_customer_endpoint(
        current_user: Annotated[dict, Depends(get_user_from_token)],
        service: UserService = Depends(get_user_service)
):
    return await service.get_customer_rating(current_user)


@router.get('/user/customer/{customer_id}',
            status_code=status.HTTP_200_OK,
            response_model=UserResponseDTO,
            summary="Получение заказчика по ID")
async def get_customer_by_id_endpoint(customer_id: int,
                                  current_user: Annotated[dict, Depends(get_user_from_token)],
                                  service: UserService = Depends(get_user_service)):
    return await service.get_customer_by_id_service(customer_id, current_user)


@router.get('/user/executor/{executor_id}',
            status_code=status.HTTP_200_OK,
            response_model=UserResponseDTO,
            summary="Получение исполнителя по ID")
async def get_executor_by_id_endpoint(executor_id: int,
                                      current_user: Annotated[dict, Depends(get_user_from_token)],
                                      service: UserService = Depends(get_user_service)):
    return await service.get_executor_by_id_service(executor_id, current_user)


@router.delete(
    "/user",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление аккаунта",
)
async def delete_acc_for_user_endpoint(current_user: Annotated[dict, Depends(get_user_from_token)],
                              service: UserService = Depends(get_user_service)):
    return await service.delete_user(current_user)
