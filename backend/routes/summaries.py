from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.summary import Summary
from schemas.summary import SummaryCreate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SummaryCreate)
def create_summary(summary: SummaryCreate, db: Session = Depends(get_db)):
    db_summary = Summary(
        question_id=summary.question_id,
        summary_text=summary.summary_text
    )
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

@router.get("/", response_model=List[SummaryCreate])
def get_summaries(db: Session = Depends(get_db)):
    return db.query(Summary).all()

@router.get("/by-question/{question_id}", response_model=List[SummaryCreate])
def get_summaries_by_question(question_id: int, db: Session = Depends(get_db)):
    summaries = db.query(Summary).filter(Summary.question_id == question_id).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No summaries found for this question_id")
    return summaries
