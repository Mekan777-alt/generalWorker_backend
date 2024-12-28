from sqlalchemy.util import await_only

from api.dependency.encryption import decrypt_phone
from api.dto.user_dto import UserPartialUpdateDTO, UserResponseDTO
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends, UploadFile

from api.services.minio_service import MinioClient
from models.enums import RolesEnum


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

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

    async def get_user_info_service(self, current_user: dict):
        auth_id = current_user.get('id')
        role_id = current_user.get('role_id')

        user_phone_number = await self.user_repository.get_phone_number(auth_id)
        user_info = await self._get_user_info_by_role(auth_id, role_id)

        return UserResponseDTO(
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
            user_phone_number.phoneNumber = phone
            await self.user_repository.update_auth_model(user_phone_number)
        if photo:
            photo_url = await minio_client.upload_photo(user=user_info.id, prefix="photos", image=photo)
            user_info.photo = photo_url


        update_user = await self.user_repository.update_user_info(user_info)

        return UserResponseDTO(
            firstName=update_user.firstName if update_user.firstName else "",
            lastName=update_user.lastName if update_user.lastName else "",
            phoneNumber=await decrypt_phone(user_phone_number.phoneNumber),
            location=update_user.location if update_user.location else "",
            aboutMySelf=update_user.aboutMySelf if update_user.aboutMySelf else "",
        )

    async def upload_photo_service(self, photo: UploadFile, current_user: dict, minio_client: MinioClient):
        auth_id = current_user.get('id')
        role_id = current_user.get('role_id')

        user = await self._get_user_info_by_role(auth_id, role_id)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
