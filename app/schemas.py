from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Схема для создания объявления (в теле запроса)
class AdCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    owner: str

# Схема для ответа (API возвращает это)
class AdSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    owner: str
    created_at: datetime

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy
