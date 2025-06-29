# models/contradiction.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai1 = Column(String, nullable=False)
    ai2 = Column(String, nullable=False)
    label = Column(String, nullable=False)  # "entailment", "neutral", "contradiction"
    score = Column(Float, nullable=False)

    question = relationship("Question", back_populates="contradictions")
