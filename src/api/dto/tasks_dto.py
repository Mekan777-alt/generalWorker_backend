from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class TaskRequestDescriptionDTO(BaseModel):
    taskDescription: str = Field(..., description="Описание задачи")


class CustomerResponseDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")
    firstName: str = Field(..., description="Имя заказчика")
    lastName: str = Field(..., description="Фамилия заказчика")
    photo: Optional[str] = Field(None, description="Uri на фотографию")


class TaskRequestDTO(BaseModel):
    taskName: str = Field(..., description="Название задания")
    taskDescription: Optional[str] = Field(None, description="Описание задачи")
    taskPrice: float = Field(..., description="Цена задания")
    taskTerm: datetime = Field(..., description="Срок выполнение задания")
    taskCity: str = Field(..., description="Город выполнение задания")


class TaskResponseDTO(BaseModel):
    id: int = Field(..., description="Идентификатор задачи")
    taskName: str = Field(..., description="Название задание")
    taskDescription: Optional[str] = Field(None, description="Описание задачи")
    taskPrice: float = Field(..., description="Цена задание")
    taskTerm: str = Field(..., description="Срок выполнение задание")
    taskCreated: Optional[str] = Field(None, description="Дата создание")
    taskCity: str = Field(..., description="Город выполнение задание")
    taskStatus: Optional[str] = Field(..., description="Статус задания")
    isPublic: bool = Field(..., description="Флаг то что опубликовано ли задание")
    roomUUID: Optional[str] = Field(None, description="UUID комнаты общения")
    customer: Optional[CustomerResponseDTO] = Field(None, description="Данные заказчика")


class ResponseByTaskIdDTO(BaseModel):
    id: int = Field(..., description="Идентификатор исполнителя")
    firstName: str = Field(..., description="Имя исполнителя")
    lastName: str = Field(..., description="Фамилия исполнителя")
    rating: int = Field(..., description="Рейтинг исполнителя")
    photo: Optional[str] = Field(..., description="Фото исполнителя")
    created_at: str = Field(..., description="Время отклика")
    text: str = Field(..., description="Текст отклика")
    roomUUID: Optional[str] = Field(None, description="ID комнаты")


class CreateResponseTaskByIdDTO(BaseModel):
    text: str = Field(..., description="Текст для отклика")