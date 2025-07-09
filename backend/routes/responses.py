from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.response import Response
from schemas.response import ResponseCreate
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

@router.get("/by-question/{question_id}", response_model=List[ResponseCreate])
def get_responses_by_question(question_id: int, db: Session = Depends(get_db)):
    responses = db.query(Response).filter(Response.question_id == question_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for this question_id")
    return responses