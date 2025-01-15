from pydantic import BaseModel, Field
from datetime import date

class SubscriptionHistoryResponseDTO(BaseModel):
    price: str = Field(..., description="Цена подписки")
    create_date: str = Field(..., description="Дата покупки")
