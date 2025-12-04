from pydantic import BaseModel, Field
from datetime import datetime

class AdBase(BaseModel):
    title: str
    description: str
    price: float = Field(..., ge=0)
    owner: str

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(None, ge=0)
    owner: str | None = None

class AdResponse(AdBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
