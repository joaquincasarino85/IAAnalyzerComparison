from pydantic import BaseModel

class SentimentCreate(BaseModel):
    question_id: int
    ai_name: str
    label: str
    score: float