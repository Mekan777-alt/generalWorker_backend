import random
from typing import Optional, Tuple
from urllib.parse import urlencode, quote_plus
import aiohttp
import jwt

from api.dependency.encryption import encrypt_phone
from datetime import datetime, timedelta, timezone
from models.entity import AuthModel, UsersModel, UserRolesModel
from fastapi import Depends, HTTPException
from starlette import status
from api.repositories.auth_repository import get_auth_repository, AuthRepository
from api.dto.auth_dto import VerifyCode, AuthUserDTO, TokensCreateResponseDTO, AuthRefreshTokenDTO, UpdateRoleRequestDTO
from core.config import settings


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository


    async def auth_user(self, request: AuthUserDTO):
        encrypted_phone = await encrypt_phone(request.phoneNumber)
        auth = await self.auth_repository.get_user_by_phone_number(encrypted_phone)
        verification_code = str(random.randint(1000, 9999))

        if not auth:

            user = AuthModel(
                phoneNumber=encrypted_phone,
                otpCode=verification_code,
                otpExpiry=datetime.utcnow() + timedelta(minutes=5),
            )

            auth_model = await self.auth_repository.create_user(user)

            profile = UsersModel(
                auth_id=auth_model.id
            )

            await self.auth_repository.create_profile(profile)

            roles = await self.auth_repository.get_roles()
            user_role = []

            for role in roles:
                is_use = False

                if role.name == request.role:
                    is_use = True

                new_role = UserRolesModel(
                    auth_id=auth_model.id,
                    role_id=role.id,
                    is_use=is_use,
                )
                user_role.append(new_role)

            await self.auth_repository.create_role_to_user(user_role)

            return VerifyCode(verificationCode=verification_code)

        # send_message = await self.__send_message(request.phoneNumber[1:], verification_code)
        #
        # if not send_message:
        #     raise HTTPException(
        #         detail="Не удалось отправить SMS",
        #         status_code=status.HTTP_400_BAD_REQUEST
        #     )

        auth.otpCode = verification_code
        auth.otpExpiry = datetime.utcnow() + timedelta(minutes=5)

        await self.auth_repository.update_user(auth)

        return VerifyCode(verificationCode=verification_code)

    async def __send_message(self, phone_number: str, verification_code: str):
        url = f"{settings.devino_telecom_settings.devino_telecom_api_url}/Sms/Send"
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
        auth = await self.auth_repository.get_user_by_verify_code(request.verificationCode)

        if not auth:
            raise HTTPException(detail="Пользователь не найден", status_code=status.HTTP_404_NOT_FOUND)

        if auth.otpCode != request.verificationCode:
            raise HTTPException(detail="Неверный код подтверждения", status_code=status.HTTP_400_BAD_REQUEST)

        if datetime.utcnow() > auth.otpExpiry:
            raise HTTPException(detail="Код подтверждения истек", status_code=status.HTTP_400_BAD_REQUEST)

        auth.otpCode = None
        auth.otpExpiry = None
        auth.isActive = True

        await self.auth_repository.update_user(auth)

        user_role = await self.auth_repository.get_auth_roles(auth.id)

        access_token, refresh_token = await self.__create_tokens({"id": auth.id,
                                                                  "phoneNumber": auth.phoneNumber,
                                                                  "role_id": user_role.role_id})

        return TokensCreateResponseDTO(access_token=access_token, refresh_token=refresh_token)

    async def __create_tokens(self, data: dict) -> Tuple[str, str]:
        # Время жизни токенов
        access_expires_delta = timedelta(hours=1)  # Время жизни access_token
        refresh_expires_delta = timedelta(days=7)  # Время жизни refresh_token

        # Создаем access_token
        access_payload = data.copy()
        access_payload.update({"exp": datetime.utcnow() + access_expires_delta})
        access_token = jwt.encode(access_payload, settings.jwt_settings.secret_key,
                                  algorithm=settings.jwt_settings.algorithm)

        # Создаем refresh_token
        refresh_payload = data.copy()
        refresh_payload.update({"exp": datetime.utcnow() + refresh_expires_delta})
        refresh_token = jwt.encode(refresh_payload, settings.jwt_settings.secret_key,
                                   algorithm=settings.jwt_settings.algorithm)

        return access_token, refresh_token

    async def __decode_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.jwt_settings.secret_key, algorithms=[settings.jwt_settings.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def refresh_token_service(self, data: AuthRefreshTokenDTO):
        # Декодируем токен
        decode_refresh_token = await self.__decode_token(data.refresh_token)

        # Проверяем, что токен был успешно декодирован
        if decode_refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный или просроченный токен обновления.",
            )

        # Проверка на истечение времени токена
        current_timestamp = datetime.now(tz=timezone.utc).timestamp()
        if decode_refresh_token['exp'] < current_timestamp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен обновления истек."
            )

        # Проверка, что пользователь из токена существует и данные совпадают
        user_from_token = await self.auth_repository.check_user_from_token(
            auth_id=decode_refresh_token.get('id'), phone_number=decode_refresh_token.get('phoneNumber'))
        if user_from_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден или данные токена не совпадают."
            )
        user_role = await self.auth_repository.get_auth_roles(user_from_token.id)
        # Генерируем новые токены (например, создаем новые access и refresh токены)
        user_data = {"id": user_from_token.id, "phoneNumber": user_from_token.phoneNumber, "role_id": user_role.role_id}
        new_access_token, new_refresh_token = await self.__create_tokens(user_data)

        # Возвращаем новые токены
        return TokensCreateResponseDTO(access_token=new_access_token, refresh_token=new_refresh_token)


    async def update_role_service(self, current_user: dict, data: UpdateRoleRequestDTO):
        auth_id = int(current_user.get('id'))
        phone_number = current_user.get('phoneNumber')

        use_role = await self.auth_repository.get_auth_roles(auth_id)

        if use_role:
            use_role.is_use = False
            await self.auth_repository.update_roles(use_role)

        new_role = await self.auth_repository.get_role_by_name(data.role)

        if new_role:

            new_role_relation = await self.auth_repository.get_auth_and_role_id_model(auth_id, new_role.id)

            new_role_relation.is_use = True
            await self.auth_repository.update_roles(new_role)

        user_data = {"id": auth_id, "phoneNumber": phone_number, "role_id": new_role.id}
        new_access_token, new_refresh_token = await self.__create_tokens(user_data)

        # Возвращаем новые токены
        return TokensCreateResponseDTO(access_token=new_access_token, refresh_token=new_refresh_token)

def get_auth_service(auth_repository: AuthRepository = Depends(get_auth_repository)):
    return AuthService(auth_repository=auth_repository)
