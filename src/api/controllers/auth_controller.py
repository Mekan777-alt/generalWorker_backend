from fastapi import Depends, APIRouter
from starlette import status

from api.dto.auth_dto import AuthUserDTO, AuthResponse, UserResponse, VerifyCode, TokensCreateResponseDTO, \
    AuthRefreshTokenDTO
from api.services.auth_service import AuthService, get_auth_service

router = APIRouter(
    tags=["Авторизация"]
)


@router.post('/auth', status_code=status.HTTP_200_OK, response_model=VerifyCode,
             summary="Авторизация пользователя")
async def auth_endpoint(request: AuthUserDTO, service: AuthService = Depends(get_auth_service)):
    return await service.auth_user(request)


@router.post('/verify', status_code=status.HTTP_200_OK, summary="Верификация кода",
             response_model=TokensCreateResponseDTO)
async def verify_endpoint(request: VerifyCode, service: AuthService = Depends(get_auth_service)):
    return await service.verify_code(request)


@router.post(
    '/refresh_token',
    summary="Обновление токена авторизации",
    status_code=status.HTTP_200_OK,
    response_model=TokensCreateResponseDTO
)
async def refresh_token(
    data: AuthRefreshTokenDTO,
    service: AuthService = Depends(get_auth_service)
):
    return await service.refresh_token_service(data)
