from api.dependency.encryption import decrypt_phone
from api.dto.user_dto import UserPartialUpdateDTO, UserResponseDTO
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends, UploadFile
from api.services.s3_service import s3_client


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_info_service(self, current_user: dict):
        auth_id = current_user.get('id')
        user_phone_number = await self.user_repository.get_phone_number(auth_id)
        user_info = await self.user_repository.get_user_info(auth_id)

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
        user_info = await self.user_repository.get_user_info(auth_id)
        user_phone_number = await self.user_repository.get_phone_number(auth_id)

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

        return update_user


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
