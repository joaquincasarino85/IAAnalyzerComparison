# backend/models.py o donde tengas el modelo

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    language = Column(String, nullable=True)  # ✅ Agregado
    created_at = Column(DateTime, default=func.now())

    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")
    summary = relationship("Summary", back_populates="question", uselist=False, cascade="all, delete-orphan")
    similarities = relationship("Similarity", back_populates="question", cascade="all, delete-orphan")
    semantic_similarities = relationship("SemanticSimilarity", back_populates="question", cascade="all, delete-orphan")
    contradictions = relationship("Contradiction", back_populates="question", cascade="all, delete-orphan")
    named_entities = relationship("NamedEntity", back_populates="question", cascade="all, delete-orphan")
    sentiments = relationship("Sentiment", back_populates="question", cascade="all, delete-orphan")
