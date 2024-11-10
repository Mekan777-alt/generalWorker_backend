from typing import Annotated, Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette import status
from api.repositories.auth_repository import get_auth_repository, AuthRepository
from core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)

async def get_user_from_token(
        token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
        auth_repository: AuthRepository = Depends(get_auth_repository)
):
    try:
        if not token:
            raise ValueError("No token")
        # Декодируем и проверяем токен с использованием секретного ключа и алгоритма
        payload = jwt.decode(token.credentials, settings.jwt_settings.secret_key,
                             algorithms=[settings.jwt_settings.algorithm])
        auth_id = payload.get("id")
        phone_number = payload.get("phoneNumber")

        if not auth_id or not phone_number:
            raise ValueError("Token does not contain required user data")

        user = await auth_repository.get_auth_with_user(auth_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or invalid token data.",
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )