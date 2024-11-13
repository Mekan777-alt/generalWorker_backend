from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskRequestDTO(BaseModel):
    taskName: str = Field(..., description="Название задания")
    taskDescription: str = Field(..., description="Описание задачи")
    taskPrice: float = Field(..., description="Цена задания")
    taskTerm: datetime = Field(..., description="Срок выполнение задания")
    taskCity: str = Field(..., description="Город выполнение задания")


class TaskResponseDTO(BaseModel):
    id: int = Field(..., description="Идентификатор задачи")
    taskName: str = Field(..., description="Название задание")
    taskDescription: str = Field(..., description="Описание задачи")
    taskPrice: float = Field(..., description="Цена задание")
    taskTerm: str = Field(..., description="Срок выполнение задание")
    taskCreated: Optional[str] = Field(None, description="Дата создание")
    taskCity: str = Field(..., description="Город выполнение задание")
    taskStatus: str = Field(..., description="Статус задания")
    isPublic: bool = Field(..., description="Флаг то что опубликовано ли задание")