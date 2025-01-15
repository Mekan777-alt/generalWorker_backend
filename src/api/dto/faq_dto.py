from pydantic import BaseModel, Field

class FAQResponseDTO(BaseModel):
    question: str = Field(..., description="Заголовок вопроса")
    answer: str = Field(..., description="Ответ на вопрос")
