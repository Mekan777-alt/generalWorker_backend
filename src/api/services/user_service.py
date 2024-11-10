from api.dependency.encryption import decrypt_phone
from api.dto.user_dto import UserPartialUpdateDTO, UserResponseDTO
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_info_service(self, current_user):
        user_info = current_user.user[0]

        return UserResponseDTO(
            firstName=user_info.firstName,
            lastName=user_info.lastName,
            phoneNumber=await decrypt_phone(current_user.phoneNumber),
            location=user_info.location,
            aboutMySelf=user_info.aboutMySelf
        )


    async def partial_update_service(self, current_user, data: UserPartialUpdateDTO):
        user_info = current_user.user[0]

        if data.firstName:
            user_info.firstName = data.firstName
        if data.lastName:
            user_info.lastName = data.lastName
        if data.location:
            user_info.location = data.location
        if data.aboutMySelf:
            user_info.aboutMySelf = data.aboutMySelf
        if data.phoneNumber:
            user_info.phoneNumber = data.phoneNumber
        if data.photo:
            user_info.photo = data.photo

        update_user = await self.user_repository.update_user_info(user_info)

        return update_user


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
