from starlette import status

from api.dependency.encryption import encrypt_phone
from api.dependency.encryption import decrypt_phone
from api.dto.user_dto import UserResponseDTO, ExecutorRatingDTO, ReviewDTO, CustomerRatingDTO
from api.repositories.tasks_repository import TasksRepository, get_tasks_repository
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends, UploadFile, HTTPException

from api.services.minio_service import MinioClient
from core.config import settings
from models.enums import RolesEnum


class UserService:
    def __init__(self, user_repository: UserRepository, task_repository: TasksRepository):
        self.user_repository = user_repository
        self.task_repository = task_repository

    async def _get_user_info_by_role(self, auth_id: int, role_id: int):
        """
        Метод для получения информации о пользователе в зависимости от его роли.
        """
        user_role = await self.user_repository.get_role_by_id(role_id)

        if user_role.name == RolesEnum.CUSTOMER.value:
            customer = await self.user_repository.get_customer_profile(auth_id)

            if not customer:

                return await self.user_repository.create_customer_profile(auth_id)

            return customer

        if user_role.name == RolesEnum.EXECUTOR.value:
            executor = await self.user_repository.get_executor_profile(auth_id)

            if not executor:

                return await self.user_repository.create_executor_profile(auth_id)

            return executor

        raise ValueError(f"Unexpected role: {user_role.name}")


    async def get_executor_rating(self, current_user: dict):
        auth_id = current_user.get('id')
        executor = await self.user_repository.get_executor_profile(auth_id)

        if not executor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No executor found"
            )

        completed_task_count = await self.task_repository.completed_task_count_executor(executor.id)
        total_earnings = await self.task_repository.total_earning_executor(executor.id)
        review_array = await self.task_repository.review_executor(executor.id)

        return ExecutorRatingDTO(
            rating="Супер (Топ-10)",
            tasks_completed=completed_task_count,
            total_earnings=total_earnings,
            review_array=[ReviewDTO(
                comment=review.comment,
                rating="positive" if review.rating else "negative",
                created_at=review.created_at.isoformat(),
                author_name=review.firstName,
                author_photo=review.photo,
            ) for review in review_array]
        )



    async def get_customer_rating(self, current_user: dict):
        auth_id = current_user.get('id')
        customer = await self.user_repository.get_customer_profile(auth_id)

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No customer found"
            )

        count_task_created = await self.task_repository.customer_create_task_count(customer.id)

        return CustomerRatingDTO(
            rating="Супер (Топ-10)",
            tasks_created=count_task_created,
        )

    async def get_user_info_service(self, current_user: dict):
        auth_id = current_user.get('id')
        role_id = current_user.get('role_id')

        user_phone_number = await self.user_repository.get_phone_number(auth_id)
        user_info = await self._get_user_info_by_role(auth_id, role_id)

        return UserResponseDTO(
            id=user_info.id,
            firstName=user_info.firstName if user_info.firstName else "",
            lastName=user_info.lastName if user_info.lastName else "",
            phoneNumber=await decrypt_phone(user_phone_number.phoneNumber),
            location=user_info.location if user_info.location else "",
            aboutMySelf=user_info.aboutMySelf if user_info.aboutMySelf else "",
        )


    async def partial_update_service(self, current_user,
                                     first_name: str = None,
                                     last_name: str = None,
                                     phone: str = None,
                                     location: str = None ,
                                     about_my_self: str = None,
                                     photo: UploadFile = UploadFile(...),
                                     minio_client: MinioClient = None):
        auth_id = current_user.get('id')
        role_id = current_user.get('role_id')

        user_phone_number = await self.user_repository.get_phone_number(auth_id)
        user_info = await self._get_user_info_by_role(auth_id, role_id)


        if first_name:
            user_info.firstName = first_name
        if last_name:
            user_info.lastName = last_name
        if location:
            user_info.location = location
        if about_my_self:
            user_info.aboutMySelf = about_my_self
        if phone:
            user_phone_number.phoneNumber = await encrypt_phone(phone)
            await self.user_repository.update_auth_model(user_phone_number)
        if photo:
            photo_url = await minio_client.upload_photo(user=user_info.id, prefix="photos", image=photo)
            user_info.photo = f"http://{settings.s3_settings.s3_url}/{settings.s3_settings.s3_bucket_name}/{photo_url}"


        update_user = await self.user_repository.update_user_info(user_info)

        return UserResponseDTO(
            id=update_user.id,
            firstName=update_user.firstName if update_user.firstName else "",
            lastName=update_user.lastName if update_user.lastName else "",
            phoneNumber=await decrypt_phone(user_phone_number.phoneNumber),
            location=update_user.location if update_user.location else "",
            aboutMySelf=update_user.aboutMySelf if update_user.aboutMySelf else "",
        )

    async def get_customer_by_id_service(self, customer_id: int, current_user: dict):
        customer = await self.user_repository.get_customer_by_id(customer_id)

        if not customer:
            raise HTTPException(
                detail="Заказчик не найден",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return UserResponseDTO(
            id=customer.id,
            firstName=customer.firstName,
            lastName=customer.lastName,
            phoneNumber=await decrypt_phone(customer.auth_info.phoneNumber),
            location=customer.location,
            aboutMySelf=customer.aboutMySelf,
            photo=customer.photo
        )

    async def get_executor_by_id_service(self, executor_id: int, current_user: dict):
        executor = await self.user_repository.get_executor_by_id(executor_id)

        if not executor:
            raise HTTPException(
                detail="Исполнитель не найден",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return UserResponseDTO(
            id=executor.id,
            firstName=executor.firstName,
            lastName=executor.lastName,
            phoneNumber=await decrypt_phone(executor.auth_info.phoneNumber),
            location=executor.location,
            aboutMySelf=executor.aboutMySelf,
            photo=executor.photo
        )

    async def delete_user(self, current_user: dict):
        auth_id = current_user.get('id')

        user = await self.user_repository.get_user_by_id(auth_id)

        if not user:
            raise HTTPException(
                detail="Пользователь не найден",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        await self.user_repository.delete_user(auth_id)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository),
                     task_repository: TasksRepository = Depends(get_tasks_repository)):
    return UserService(user_repository, task_repository)
