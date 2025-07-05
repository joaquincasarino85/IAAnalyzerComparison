from pydantic import BaseModel

class SemanticSimilarityCreate(BaseModel):
    question_id: int
    ai1: str
    ai2: str
    similarity_score: float