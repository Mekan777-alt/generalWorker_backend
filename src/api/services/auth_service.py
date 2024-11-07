import random
import base64
from urllib.parse import urlencode, quote_plus

import aiohttp
from api.dependency.encryption import encrypt_phone, decrypt_phone
from datetime import datetime, timedelta
from models import Users
from fastapi import Depends, HTTPException
from starlette import status
from api.repositories.auth_repository import get_auth_repository, AuthRepository
from api.dto.auth_dto import VerifyCode, UserResponse, AuthUserDTO, UserInfoDTO, BasicTokenDTO
from core.config import settings


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository


    async def auth_user(self, request: AuthUserDTO):
        encrypted_phone = await encrypt_phone(request.phoneNumber)
        user = await self.auth_repository.get_user_by_phone_number(encrypted_phone)

        verification_code = str(random.randint(100000, 999999))
        send_message = await self.__send_message(request.phoneNumber[1:], verification_code)

        if not send_message:
            raise HTTPException(
                detail="Не удалось отправить SMS",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.verifyCode = verification_code
        user.codeCreatedAt = datetime.utcnow()

        await self.auth_repository.update_user(user)

        return {"message": "SMS отправлено успешно."}

    async def __send_message(self, phone_number: str, verification_code: str):
        url = f"{settings.devino_settings.devino_telecom_api_url}/Sms/Send"
        params = {
            "Login": settings.devino_settings.devino_login,
            "Password": settings.devino_settings.devino_password,
            "DestinationAddress": phone_number,
            "Data": f"Ваш код подтверждения: {verification_code}",
            "SourceAddress": "generalWorker",
            "Validity": 0
        }

        encoded_params = urlencode(params, quote_via=quote_plus)

        full_url = f"{url}?{encoded_params}"

        async with aiohttp.ClientSession() as client:
            async with client.post(full_url) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    async def verify_code(self, request: VerifyCode):
        user = await self.auth_repository.get_user_by_verify_code(request.verificationCode)

        if not user:
            raise HTTPException(detail="Пользователь не найден", status_code=status.HTTP_404_NOT_FOUND)

        if user.verifyCode != request.verificationCode:
            raise HTTPException(detail="Неверный код подтверждения", status_code=status.HTTP_400_BAD_REQUEST)

        if datetime.utcnow() > user.codeCreatedAt + timedelta(minutes=5):
            raise HTTPException(detail="Код подтверждения истек", status_code=status.HTTP_400_BAD_REQUEST)

        token = await self.__generate_token(user)

        user.isActive = True
        user.isRegistered = True
        user.verifyCode = None
        user.codeCreatedAt = None

        await self.auth_repository.update_user(user)

        return {"message": "Success"}


    async def __generate_token(self, user: Users):
        token_str = f"{user.id}:{user.phoneNumber}"

        token_bytes = token_str.encode('ascii')
        base64_bytes = base64.b64encode(token_bytes)

        return base64_bytes.decode('ascii')


def get_auth_service(auth_repository: AuthRepository = Depends(get_auth_repository)):
    return AuthService(auth_repository=auth_repository)
