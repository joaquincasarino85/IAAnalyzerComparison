from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.contradiction import Contradiction
from schemas.contradiction import ContradictionCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ContradictionCreate)
def create_contradiction(contradiction: ContradictionCreate, db: Session = Depends(get_db)):
    db_contradiction = Contradiction(
        question_id=contradiction.question_id,
        ai1=contradiction.ai1,
        ai2=contradiction.ai2,
        label=contradiction.label,
        score=contradiction.score
    )
    db.add(db_contradiction)
    db.commit()
    db.refresh(db_contradiction)
    return db_contradiction

@router.get("/", response_model=List[ContradictionCreate])
def get_all_contradictions(db: Session = Depends(get_db)):
    return db.query(Contradiction).all()

@router.get("/by-question/{question_id}", response_model=List[ContradictionCreate])
def get_contradictions_by_question(question_id: int, db: Session = Depends(get_db)):
    contradictions = db.query(Contradiction).filter(Contradiction.question_id == question_id).all()
    if not contradictions:
        raise HTTPException(status_code=404, detail="No contradictions found for this question_id")
    return contradictions