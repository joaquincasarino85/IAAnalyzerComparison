from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai_name = Column(String, nullable=False)
    response_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    question = relationship("Question")
