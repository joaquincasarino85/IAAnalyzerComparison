from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import SessionLocal
from backend.models.semantic_similarity import SemanticSimilarity
from backend.schemas.semantic_similarity import SemanticSimilarityCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SemanticSimilarityCreate)
def create_semantic_similarity(sim: SemanticSimilarityCreate, db: Session = Depends(get_db)):
    db_similarity = SemanticSimilarity(
        question_id=sim.question_id,
        ai1=sim.ai1,
        ai2=sim.ai2,
        similarity_score=sim.similarity_score
    )
    db.add(db_similarity)
    db.commit()
    db.refresh(db_similarity)
    return db_similarity

@router.get("/", response_model=List[SemanticSimilarityCreate])
def get_all_semantic_similarities(db: Session = Depends(get_db)):
    return db.query(SemanticSimilarity).all()

@router.get("/by-question/{question_id}", response_model=List[SemanticSimilarityCreate])
def get_semantic_similarities_by_question(question_id: int, db: Session = Depends(get_db)):
    sims = db.query(SemanticSimilarity).filter(SemanticSimilarity.question_id == question_id).all()
    if not sims:
        raise HTTPException(status_code=404, detail="No semantic similarities found for this question_id")
    return sims
