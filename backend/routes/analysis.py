from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.SimilarityAnalyzer import SimilarityAnalyzer
from services.SummaryAnalyzer import SummaryAnalyzer
from services.NLPAnalyzer import NLPAnalyzer
from models.question import Question as QuestionModel
from models.response import Response as Answer
from models.summary import Summary as Summary
from models.similarity import Similarity as Similarity
from models.semantic_similarity import SemanticSimilarity as SemanticSimilarity
from models.contradiction import Contradiction as Contradiction
from models.named_entity import NamedEntity as NamedEntity
from models.sentiment import Sentiment as Sentiment
from database import get_db
from pydantic import BaseModel
from typing import Dict, List
import numpy as np

router = APIRouter()

class AnalysisRequest(BaseModel):
    question_id: int

def convert_np(obj):
    """Convierte recursivamente np.float32 a float, para que FastAPI lo pueda serializar."""
    if isinstance(obj, dict):
        return {k: convert_np(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np(v) for v in obj]
    elif isinstance(obj, np.float32) or isinstance(obj, np.float64):
        return float(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    return obj

@router.post("/generate-summary")
async def generate_summary(analysis_request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Genera el resumen de todas las respuestas
    """
    # Obtener todas las respuestas
    responses = db.query(Answer).filter(Answer.question_id == analysis_request.question_id).all()
    response_texts = [r.response_text for r in responses]
    
    # Generar resumen
    summary_analyzer = SummaryAnalyzer()
    summary_text = summary_analyzer.generate_summary(response_texts)
    
    # Guardar resumen
    new_summary = Summary(question_id=analysis_request.question_id, summary_text=summary_text)
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    
    return {
        "question_id": analysis_request.question_id,
        "summary": summary_text,
        "status": "completed"
    }

@router.post("/full-analysis")
async def full_analysis(analysis_request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Realiza el análisis completo: similitud, contradicciones, entidades, sentimientos
    """
    # Obtener todas las respuestas
    responses = db.query(Answer).filter(Answer.question_id == analysis_request.question_id).all()
    responses_dict = {r.ai_name: r.response_text for r in responses}
    
    # 1. Análisis de similitudes básicas
    similarity_results = SimilarityAnalyzer.analyze(responses_dict)
    for pair, score in similarity_results.items():
        ai1, ai2 = pair.split(" vs ")
        db.add(Similarity(
            question_id=analysis_request.question_id,
            ai1=ai1,
            ai2=ai2,
            similarity_score=score
        ))
    
    # 2. Análisis NLP completo
    nlp_analyzer = NLPAnalyzer(responses_dict)
    
    # 2.1 Similitud semántica
    semantic_similarities = nlp_analyzer.analyze_semantic_similarity()
    for result in semantic_similarities:
        similarity_record = SemanticSimilarity(
            question_id=analysis_request.question_id,
            ai1=result["ai1"],
            ai2=result["ai2"],
            similarity_score=float(result["score"])
        )
        db.add(similarity_record)
    
    # 2.2 Contradicciones
    contradictions = nlp_analyzer.detect_contradictions()
    for result in contradictions:
        contradiction_record = Contradiction(
            question_id=analysis_request.question_id,
            ai1=result["ai1"],
            ai2=result["ai2"],
            label=result["label"],
            score=float(result["score"])
        )
        db.add(contradiction_record)
    
    # 2.3 Entidades nombradas
    named_entities = nlp_analyzer.extract_named_entities()
    for ai_name, entities in named_entities.items():
        for entity in entities:
            entity_record = NamedEntity(
                question_id=analysis_request.question_id,
                ai_name=ai_name,
                entity=entity["word"],
                label=entity["entity_group"]
            )
            db.add(entity_record)
    
    # 2.4 Análisis de sentimiento
    sentiments = nlp_analyzer.analyze_sentiment()
    for ai_name, results in sentiments.items():
        for result in results:
            sentiment_record = Sentiment(
                question_id=analysis_request.question_id,
                ai_name=ai_name,
                label=result["label"],
                score=float(result["score"])
            )
            db.add(sentiment_record)
    
    # 3. Generar resumen
    summary_analyzer = SummaryAnalyzer()
    summary_text = summary_analyzer.generate_summary(list(responses_dict.values()))
    
    new_summary = Summary(question_id=analysis_request.question_id, summary_text=summary_text)
    db.add(new_summary)
    
    # Guardar todo
    db.commit()
    
    return convert_np({
        "question_id": analysis_request.question_id,
        "similarities": similarity_results,
        "semantic_similarities": semantic_similarities,
        "contradictions": contradictions,
        "named_entities": named_entities,
        "sentiments": sentiments,
        "summary": summary_text,
        "status": "completed"
    }) 