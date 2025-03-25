from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.summary import Summary
from backend.schemas.summary import SummaryCreate
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
