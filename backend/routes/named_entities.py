from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import SessionLocal
from backend.models.named_entity import NamedEntity
from backend.schemas.named_entity import NamedEntityCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=NamedEntityCreate)
def create_named_entity(entity: NamedEntityCreate, db: Session = Depends(get_db)):
    db_entity = NamedEntity(
        question_id=entity.question_id,
        ai_name=entity.ai_name,
        entity=entity.entity,
        label=entity.label
    )
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

@router.get("/", response_model=List[NamedEntityCreate])
def get_all_named_entities(db: Session = Depends(get_db)):
    return db.query(NamedEntity).all()

@router.get("/by-question/{question_id}", response_model=List[NamedEntityCreate])
def get_named_entities_by_question(question_id: int, db: Session = Depends(get_db)):
    entities = db.query(NamedEntity).filter(NamedEntity.question_id == question_id).all()
    if not entities:
        raise HTTPException(status_code=404, detail="No named entities found for this question_id")
    return entities