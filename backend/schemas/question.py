from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QuestionRequest(BaseModel):
    text: str
    ai_name: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    text: str
    language: str | None
    created_at: datetime

    class Config:
        from_attributes = True

