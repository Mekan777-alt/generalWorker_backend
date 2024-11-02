from starlette import status
from api.dto.user_dto import UserPartialUpdateDTO
from api.repositories.user_repository import get_user_repository, UserRepository
from fastapi import Depends, HTTPException


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_info_service(self, current_user: dict):
        user_uid = current_user.get('uid')

        user = await self.user_repository.get_user_info_by_uid(user_uid)

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User does not exist'
            )

        return user


    async def partial_update_service(self, current_user: dict, data: UserPartialUpdateDTO):
        user_uid = current_user.get('uid')

        user = await self.user_repository.get_user_info_by_uid(user_uid)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User does not exist'
            )

        if data.firstName:
            user.firstName = data.firstName
        if data.lastName:
            user.lastName = data.lastName
        if data.location:
            user.location = data.location
        if data.aboutMySelf:
            user.aboutMySelf = data.aboutMySelf
        if data.phoneNumber:
            user.phoneNumber = data.phoneNumber
        if data.photo:
            user.photo = data.photo

        update_user = await self.user_repository.update_user_info(user)

        return update_user


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
