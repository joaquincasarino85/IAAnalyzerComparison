# models/named_entity.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NamedEntity(Base):
    __tablename__ = "named_entities"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    ai_name = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    label = Column(String, nullable=False)  # e.g., PERSON, ORG, GPE

    question = relationship("Question", back_populates="named_entities")
