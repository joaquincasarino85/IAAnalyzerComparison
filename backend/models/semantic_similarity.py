from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class SemanticSimilarity(Base):
    __tablename__ = "semantic_similarities"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai1 = Column(String, nullable=False)
    ai2 = Column(String, nullable=False)
    similarity_score = Column(Float, nullable=False)  # Ej: cosine similarity

    question = relationship("Question")
