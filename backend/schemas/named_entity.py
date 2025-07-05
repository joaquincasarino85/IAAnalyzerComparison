from pydantic import BaseModel

class NamedEntityCreate(BaseModel):
    question_id: int
    ai_name: str
    entity: str
    label: str