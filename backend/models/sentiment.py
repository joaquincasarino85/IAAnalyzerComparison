# models/sentiment.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai_name = Column(String, nullable=False)
    label = Column(String, nullable=False)  # POSITIVE / NEGATIVE / NEUTRAL
    score = Column(Float, nullable=False)

    question = relationship("Question", back_populates="sentiments")
