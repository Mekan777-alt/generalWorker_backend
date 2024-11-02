from api.repositories.verify_user_repository import get_verify_user_repository, VerifyUserRepository
from api.dto.verify_user_dto import VerifySMSRequest
from models import Users
from firebase_admin import auth
from fastapi import Depends

class VerifyUserService:
    def __init__(self, verify_user_repository: VerifyUserRepository):
        self.verify_user_repository = verify_user_repository

    async def verify_user(self, data: VerifySMSRequest):
        decoded_token = auth.verify_id_token(data.id_token)
        user_uid = decoded_token['uid']

        existing_user = await self.verify_user_repository.get_user_by_uid(user_uid)

        if not existing_user:

            new_user = Users(
                firebase_uid=user_uid
            )

            user = await self.verify_user_repository.create_user(new_user)
            return user

        return existing_user


def get_verify_user_service(
        verify_user_repository: VerifyUserRepository = Depends(get_verify_user_repository)):
    return VerifyUserService(verify_user_repository)
