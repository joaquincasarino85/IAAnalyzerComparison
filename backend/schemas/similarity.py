from pydantic import BaseModel
from typing import Optional

class SimilarityCreate(BaseModel):
    question_id: int
    ai1: str
    ai2: str
    similarity_score: float

    class Config:
        orm_mode = True

class SimilarityResponse(SimilarityCreate):
    id: int

class SimilarityData(BaseModel):
    id: int
    question_id: int
    ai1: str
    ai2: str
    similarity_score: float