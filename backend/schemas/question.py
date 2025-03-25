from pydantic import BaseModel
from datetime import datetime

class QuestionRequest(BaseModel):
    text: str

class QuestionResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
