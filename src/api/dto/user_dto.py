from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class UserResponseDTO(BaseModel):
    id: int = Field(..., description="Id пользлователя")
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


class ReviewDTO(BaseModel):
    comment: str = Field(..., description="Комментарий к отзыву")
    rating: str = Field(..., description="Рейтинг: 'positive' или 'negative'")
    created_at: datetime = Field(..., description="Дата создания отзыва")
    author_name: str = Field(..., description="Имя автора отзыва")
    author_photo: Optional[str] = Field(None, description="Фото автора отзыва")

class ExecutorRatingDTO(BaseModel):
    rating: str = Field(..., description="Рейтинг исполнителя")
    tasks_completed: int = Field(..., description="Количество выполненных задач")
    total_earnings: float = Field(..., description="Общий заработок исполнителя")
    reviews: Optional[List[ReviewDTO]] = Field([], description="Список отзывов исполнителя")

class CustomerRatingDTO(BaseModel):
    rating: str = Field(..., description="Рейтинг заказчика")
    tasks_created: int = Field(..., description="Количество созданных задач")
    # positive_reviews: int = Field(..., description="Количество положительных отзывов")
    # negative_reviews: int = Field(..., description="Количество отрицательных отзывов")