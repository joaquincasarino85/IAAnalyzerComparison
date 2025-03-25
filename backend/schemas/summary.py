from pydantic import BaseModel
from datetime import datetime

class SummaryCreate(BaseModel):
    question_id: int
    summary_text: str

class SummaryData(BaseModel):
    id: int
    question_id: int
    summary_text: str
    created_at: datetime

    class Config:
        from_attributes = True
