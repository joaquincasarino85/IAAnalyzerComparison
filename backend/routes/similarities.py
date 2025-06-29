from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.similarity import Similarity
from backend.schemas.similarity import SimilarityCreate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SimilarityCreate)
def create_similarity(similarity: SimilarityCreate, db: Session = Depends(get_db)):
    db_similarity = Similarity(
        question_id=similarity.question_id,
        model_pair=similarity.model_pair,
        score=similarity.score
    )
    db.add(db_similarity)
    db.commit()
    db.refresh(db_similarity)
    return db_similarity

@router.get("/", response_model=List[SimilarityCreate])
def get_all_similarities(db: Session = Depends(get_db)):
    return db.query(Similarity).all()

@router.get("/by-question/{question_id}", response_model=List[SimilarityCreate])
def get_similarities_by_question(question_id: int, db: Session = Depends(get_db)):
    similarities = db.query(Similarity).filter(Similarity.question_id == question_id).all()
    if not similarities:
        raise HTTPException(status_code=404, detail="No similarities found for this question_id")
    return similarities
