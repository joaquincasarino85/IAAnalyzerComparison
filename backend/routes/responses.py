from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.response import Response
from backend.schemas.response import ResponseCreate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ResponseCreate)
def create_response(response: ResponseCreate, db: Session = Depends(get_db)):
    db_response = Response(
        question_id=response.question_id,
        ai_name=response.ai_name,
        response_text=response.response_text
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

@router.get("/", response_model=List[ResponseCreate])
def get_responses(db: Session = Depends(get_db)):
    return db.query(Response).all()
