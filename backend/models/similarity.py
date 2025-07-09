from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class Similarity(Base):
    __tablename__ = "similarities"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai1 = Column(String, nullable=False)
    ai2 = Column(String, nullable=False)
    similarity_score = Column(Float, nullable=False)

    question = relationship("Question")
