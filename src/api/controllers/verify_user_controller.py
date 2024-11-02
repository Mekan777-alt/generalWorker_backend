from fastapi import APIRouter, Depends
from starlette import status
from api.services.verify_user_service import get_verify_user_service, VerifyUserService
from api.dto.verify_user_dto import VerifySMSRequest, VerifySMSResponse

router = APIRouter(
    tags=['Верификация пользователя'],
    prefix='/api',
)

@router.post('/verify-user', status_code=status.HTTP_201_CREATED, summary="Верификация и создание пользователя",
             response_model=VerifySMSResponse)
async def verify_create_user(data: VerifySMSRequest,
                             service: VerifyUserService = Depends(get_verify_user_service)):
    return await service.verify_user(data)
