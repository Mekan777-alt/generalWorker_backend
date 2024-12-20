from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class TaskRequestDescriptionDTO(BaseModel):
    taskDescription: str = Field(..., description="Описание задачи")



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


class ResponseByTaskIdDTO(BaseModel):
    id: int = Field(..., description="Идентификатор исполнителя")
    rating: int = Field(..., description="Рейтинг исполнителя")
    photo: Optional[str] = Field(..., description="Фото исполнителя")
    created_at: str = Field(..., description="Время отклика")
    text: str = Field(..., description="Текст отклика")


class CreateResponseTaskByIdDTO(BaseModel):
    text: str = Field(..., description="Текст для отклика")