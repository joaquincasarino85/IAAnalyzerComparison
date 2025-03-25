from pydantic import BaseModel
from datetime import datetime

class ResponseCreate(BaseModel):
    question_id: int
    ai_name: str
    response_text: str

class ResponseData(BaseModel):
    id: int
    question_id: int
    ai_name: str
    response_text: str
    created_at: datetime

    class Config:
        from_attributes = True
