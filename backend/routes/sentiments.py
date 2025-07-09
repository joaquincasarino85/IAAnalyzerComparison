from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.sentiment import Sentiment
from schemas.sentiment import SentimentCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SentimentCreate)
def create_sentiment(sentiment: SentimentCreate, db: Session = Depends(get_db)):
    db_sentiment = Sentiment(
        question_id=sentiment.question_id,
        ai_name=sentiment.ai_name,
        label=sentiment.label,
        score=sentiment.score
    )
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment

@router.get("/", response_model=List[SentimentCreate])
def get_all_sentiments(db: Session = Depends(get_db)):
    return db.query(Sentiment).all()

@router.get("/by-question/{question_id}", response_model=List[SentimentCreate])
def get_sentiments_by_question(question_id: int, db: Session = Depends(get_db)):
    sentiments = db.query(Sentiment).filter(Sentiment.question_id == question_id).all()
    if not sentiments:
        raise HTTPException(status_code=404, detail="No sentiments found for this question_id")
    return sentiments
