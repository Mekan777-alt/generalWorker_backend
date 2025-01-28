from pydantic import BaseModel, ValidationError, field_validator, Field
import re


class BasicTokenDTO(BaseModel):
    token: str = Field(..., examples=["Basic <KEY>"], description="Токен авторизации")


class UserInfoDTO(BaseModel):
    id: int = Field(..., examples=[1], description='id пользователя')
    phoneNumber: str = Field(..., examples=['+71234567890'], description='Номер телефона')


class UserResponse(BaseModel):
    user: UserInfoDTO
    token: BasicTokenDTO

    class Config:
        from_attributes = True


class VerifyCode(BaseModel):
    verificationCode: str = Field(..., examples=["123456"])


class AuthResponse(BaseModel):
    message: str = Field(..., examples=["SMS отправлено успешно."],
                         description="При успешной отправки СМС возвращает ответ")


class AuthUserDTO(BaseModel):
    role: str = Field(..., examples=["Customer", "Executor"],
                             description="Выбранная роль при авторизации пользователя")
    phoneNumber: str = Field(..., examples=["+71234567890"],
                             description="Номер телефона в формате +7 и 10 цифр")
    token: str = Field(..., examples=["Токен приложения"],)

    @field_validator('phoneNumber')
    def validate_phone_number(cls, v):
        # Проверка на соответствие формату +7 и наличие 11 цифр
        if not re.fullmatch(r'^\+7\d{10}$', v):
            raise ValidationError('Номер телефона должен начинаться с +7 и содержать 11 цифр')
        return v

class TokensCreateResponseDTO(BaseModel):
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."], description="Токен доступа для авторизации пользователя")
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Токен для обновления доступа пользователя")


class AuthRefreshTokenDTO(BaseModel):
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Текущий refresh_token пользователя")


class UpdateRoleRequestDTO(BaseModel):
    role: str = Field(..., examples=["Customer", "Executor"],
                      description="Смена роли")
