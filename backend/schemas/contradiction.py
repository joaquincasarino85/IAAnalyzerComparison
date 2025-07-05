from pydantic import BaseModel

class ContradictionCreate(BaseModel):
    question_id: int
    ai1: str
    ai2: str
    label: str
    score: float