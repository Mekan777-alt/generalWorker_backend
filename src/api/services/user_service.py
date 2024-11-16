from sqlalchemy.util import await_only

from api.dependency.encryption import decrypt_phone
from api.dto.user_dto import UserPartialUpdateDTO, UserResponseDTO
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends, UploadFile
from api.services.s3_service import s3_client
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
            firstName=user_info.firstName,
            lastName=user_info.lastName,
            phoneNumber=await decrypt_phone(user_phone_number.phoneNumber),
            location=user_info.location,
            aboutMySelf=user_info.aboutMySelf
        )


    async def partial_update_service(self, current_user,
                                     first_name: str = None,
                                     last_name: str = None,
                                     phone: str = None,
                                     location: str = None ,
                                     about_my_self: str = None,
                                     photo: UploadFile = UploadFile(...)):
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
            photo_url = await s3_client.upload_file(photo)
            user_info.photo = photo_url


        update_user = await self.user_repository.update_user_info(user_info)

        return UserResponseDTO(
            firstName=update_user.firstName,
            lastName=update_user.lastName,
            phoneNumber=await decrypt_phone(user_phone_number.phoneNumber),
            location=update_user.location,
            aboutMySelf=update_user.aboutMySelf
        )


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
