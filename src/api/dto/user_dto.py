from typing import Optional, List
from pydantic import BaseModel, Field

class UserResponseDTO(BaseModel):
    firstName: Optional[str] = Field(None, description="Имя пользователя")
    lastName: Optional[str] = Field(None, description="Фамилия пользователя")
    phoneNumber: Optional[str] = Field(None, description="Телефонный номер пользователя")
    location: Optional[str] = Field(None, description="Местоположение пользователя")
    aboutMySelf: Optional[str] = Field(None, description="Краткая информация о пользователе")
    photo: Optional[str] = Field(None, description="URL или путь к фотографии пользователя")

    class Config:
        from_attributes = True

class UserPartialUpdateDTO(BaseModel):
    firstName: Optional[str] = Field(None, description="Имя пользователя")
    lastName: Optional[str] = Field(None, description="Фамилия пользователя")
    phoneNumber: Optional[str] = Field(None, description="Телефонный номер пользователя")
    location: Optional[str] = Field(None, description="Местоположение пользователя")
    aboutMySelf: Optional[str] = Field(None, description="Краткая информация о пользователе")
    photo: Optional[str] = Field(None, description="URL или путь к фотографии пользователя")