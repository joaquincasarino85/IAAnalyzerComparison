from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.IAManager import IAManager
from models.question import Question as QuestionModel
from models.response import Response as Answer
from database import get_db
from schemas.question import QuestionRequest
from utils.lang import detect_language
from typing import Dict, Any
import asyncio

router = APIRouter()

@router.post("/query-single-ai")
async def query_single_ai(question_request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Consulta una IA específica y retorna su respuesta
    """
    lang = detect_language(question_request.text)
    
    # Guardar la pregunta si no existe
    existing_question = db.query(QuestionModel).filter(
        QuestionModel.text == question_request.text
    ).first()
    
    if not existing_question:
        new_question = QuestionModel(text=question_request.text, language=lang)
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        question_id = new_question.id
    else:
        question_id = existing_question.id

    # Consultar la IA específica
    manager = IAManager()
    ai_name = question_request.ai_name  # Debe venir en el request
    response_text = await manager.query_single_ai(question_request.text, ai_name, lang)
    
    # Guardar la respuesta
    answer = Answer(question_id=question_id, ai_name=ai_name, response_text=response_text)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    
    return {
        "question_id": question_id,
        "ai_name": ai_name,
        "response": response_text,
        "status": "completed"
    }

@router.post("/query-all-ais")
async def query_all_ais(question_request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Consulta todas las IAs en paralelo
    """
    lang = detect_language(question_request.text)
    
    # Guardar la pregunta
    new_question = QuestionModel(text=question_request.text, language=lang)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    # Consultar todas las IAs en paralelo
    manager = IAManager()
    responses = await manager.query_all_ias_parallel(question_request.text, lang)
    
    # Guardar todas las respuestas
    for ai_name, response_text in responses.items():
        answer = Answer(question_id=new_question.id, ai_name=ai_name, response_text=response_text)
        db.add(answer)
    db.commit()
    
    return {
        "question_id": new_question.id,
        "responses": responses,
        "status": "completed"
    } 