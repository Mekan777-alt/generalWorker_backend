from fastapi import Depends, APIRouter
from starlette import status
from typing_extensions import Annotated
from api.dependency.current_user import get_user_from_token
from api.dto.auth_dto import AuthUserDTO, AuthResponse, UserResponse, VerifyCode, TokensCreateResponseDTO, \
    AuthRefreshTokenDTO, UpdateRoleRequestDTO
from api.services.auth_service import AuthService, get_auth_service

router = APIRouter(
    tags=["Авторизация"]
)


@router.post('/auth',
             status_code=status.HTTP_200_OK,
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
async def refresh_token_endpoint(
    data: AuthRefreshTokenDTO,
    service: AuthService = Depends(get_auth_service)
):
    return await service.refresh_token_service(data)


@router.post(
    '/update_role',
    summary="Смена ролей для пользователей",
    status_code=status.HTTP_200_OK,
    response_model=TokensCreateResponseDTO
)
async def update_rol_endpoint(
        current_user: Annotated[dict, Depends(get_user_from_token)],
        data: UpdateRoleRequestDTO,
        service: AuthService = Depends(get_auth_service),
):
    return await service.update_role_service(current_user, data)