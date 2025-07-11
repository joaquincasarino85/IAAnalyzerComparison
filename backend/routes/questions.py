from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.IAManager import IAManager
from services.SimilarityAnalyzer import SimilarityAnalyzer
from services.SummaryAnalyzer import SummaryAnalyzer
from models.question import Question as QuestionModel
from models.response import Response as Answer
from models.summary import Summary as Summary
from models.similarity import Similarity as Similarity
from models.semantic_similarity import SemanticSimilarity as SemanticSimilarity
from models.contradiction import Contradiction as Contradiction
from models.named_entity import NamedEntity as NamedEntity
from models.sentiment import Sentiment as Sentiment
from database import get_db
from schemas.question import QuestionRequest
from services.NLPAnalyzer import NLPAnalyzer
from utils.lang import detect_language

import numpy as np
import sys

router = APIRouter()

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

@router.post("/")
async def ask_question(question_request: QuestionRequest, db: Session = Depends(get_db)):
    print('aca esta')

    lang = detect_language(question_request.text)

    # 1️⃣ Guardar la pregunta en la base de datos
    new_question = QuestionModel(text=question_request.text, language=lang)
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # 2️⃣ Llamar al IA Manager
    manager = IAManager()
    manager.query_ias(question_request.text, lang)
    responses = manager.get_responses()

    # 3️⃣ Guardar las respuestas en la base de datos
    for ai_name, response_text in responses.items():
        answer = Answer(question_id=new_question.id, ai_name=ai_name, response_text=response_text)
        db.add(answer)
    db.commit()


    # 4️⃣ Analizar similitudes
    similarity_results = SimilarityAnalyzer.analyze(responses)
    for pair, score in similarity_results.items():
        ai1, ai2 = pair.split(" vs ")
        db.add(Similarity(
            question_id=new_question.id,
            ai1=ai1,
            ai2=ai2,
            similarity_score=score
        ))
    db.commit()

    # 6️⃣ NLP Analysis
    nlp_analyzer = NLPAnalyzer(responses)

    # 6.1 Análisis de similitud semántica
    semantic_similarities = nlp_analyzer.analyze_semantic_similarity()
    for result in semantic_similarities:
        similarity_record = SemanticSimilarity(
            question_id=new_question.id,
            ai1=result["ai1"],
            ai2=result["ai2"],
            similarity_score=float(result["score"])
        )
        db.add(similarity_record)

    # 6.2 Análisis de contradicciones (NLI)
    contradictions = nlp_analyzer.detect_contradictions()
    for result in contradictions:
        contradiction_record = Contradiction(
            question_id=new_question.id,
            ai1=result["ai1"],
            ai2=result["ai2"],
            label=result["label"],
            score=float(result["score"])
        )
        db.add(contradiction_record)

    # 6.3 Extracción de entidades nombradas
    named_entities = nlp_analyzer.extract_named_entities()
    for ai_name, entities in named_entities.items():
        for entity in entities:
            entity_record = NamedEntity(
                question_id=new_question.id,
                ai_name=ai_name,
                entity=entity["word"],
                label=entity["entity_group"]
            )
            db.add(entity_record)

    # 6.4 Análisis de sentimiento
    sentiments = nlp_analyzer.analyze_sentiment()
    for ai_name, results in sentiments.items():
        for result in results:
            sentiment_record = Sentiment(
                question_id=new_question.id,
                ai_name=ai_name,
                label=result["label"],
                score=float(result["score"])
            )
            db.add(sentiment_record)

    db.commit()

    # 6️⃣  Generar y guardar el resumen en la base de datos
    summary_analyzer = SummaryAnalyzer()
    summary_text = summary_analyzer.generate_summary(list(responses.values()), lang)

    new_summary = Summary(question_id=new_question.id, summary_text=summary_text)  # ⬅ Creando el objeto
    db.add(new_summary)  # ⬅ Agregando a la base de datos
    db.commit()  # ⬅ Guardando cambios en la base de datos
    db.refresh(new_summary)  # ⬅ Refrescando el objeto para obtener ID

    return convert_np({
        "question": new_question.text,
        "question_id": new_question.id,
        "responses": responses,
        "similarities": similarity_results,
        "semantic_similarities": semantic_similarities,
        "contradictions": contradictions,
        "named_entities": named_entities,
        "sentiments": sentiments,
        "summary": summary_text
    })

@router.get("/{question_id}")
async def get_question_by_id(question_id: int, db: Session = Depends(get_db)):
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        return {"detail": "Question not found"}

    responses = db.query(Answer).filter(Answer.question_id == question_id).all()
    summary = db.query(Summary).filter(Summary.question_id == question_id).first()
    similarities = db.query(Similarity).filter(Similarity.question_id == question_id).all()
    semantic_similarities = db.query(SemanticSimilarity).filter(SemanticSimilarity.question_id == question_id).all()
    contradictions = db.query(Contradiction).filter(Contradiction.question_id == question_id).all()
    named_entities = db.query(NamedEntity).filter(NamedEntity.question_id == question_id).all()
    sentiments = db.query(Sentiment).filter(Sentiment.question_id == question_id).all()

    return {
        "id": question.id,
        "text": question.text,
        "summary": summary.summary_text if summary else None,
        "similarity": [
            {"ai1": s.ai1, "ai2": s.ai2, "score": s.similarity_score} for s in similarities
        ],
        "semantic_similarity": [
            {"ai1": s.ai1, "ai2": s.ai2, "score": s.similarity_score} for s in semantic_similarities
        ],
        "contradictions": [
            {"ai1": c.ai1, "ai2": c.ai2, "label": c.label, "score": c.score} for c in contradictions
        ],
        "named_entities": {
            e.ai_name: [{"entity": e.entity, "label": e.label} for e in named_entities if e.ai_name == e.ai_name]
            for e in named_entities
        },
        "sentiments": {
            s.ai_name: [{"label": s.label, "score": s.score} for s in sentiments if s.ai_name == s.ai_name]
            for s in sentiments
        },
        "responses": [
            {"iaName": r.ai_name, "text": r.response_text} for r in responses
        ],
    }


@router.get("/")
async def get_questions(db: Session = Depends(get_db)):
    questions = db.query(QuestionModel).all()
    questions_with_answers = []
    
    for q in questions:
        answers = db.query(Answer).filter(Answer.question_id == q.id).all()
        questions_with_answers.append({
            "id": q.id,
            "text": q.text,
            "answers": [{"ai_name": a.ai_name, "response": a.response_text} for a in answers],
            "created_at": q.created_at
        })
    
    return questions_with_answers

@router.post("/seed")
async def seed_test_data(db: Session = Depends(get_db)):
    """Crea datos de prueba para testing"""
    try:
        # Verificar si ya hay datos
        existing_questions = db.query(QuestionModel).count()
        if existing_questions > 0:
            return {"message": f"Ya existen {existing_questions} preguntas en la base de datos"}
        
        # Datos de prueba
        test_questions = [
            {
                "text": "¿Cuál es la capital de Francia?",
                "language": "es",
                "responses": {
                    "ChatGPT": "La capital de Francia es París, una ciudad conocida por su rica historia, cultura y monumentos icónicos como la Torre Eiffel.",
                    "Gemini": "París es la capital de Francia. Es una ciudad importante en Europa conocida por su arte, moda y gastronomía.",
                    "Mistral": "La capital de Francia es París. Es una ciudad histórica y cultural muy importante en Europa."
                }
            },
            {
                "text": "¿Qué es la inteligencia artificial?",
                "language": "es", 
                "responses": {
                    "ChatGPT": "La inteligencia artificial es un campo de la informática que busca crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana.",
                    "Gemini": "La IA es tecnología que permite a las computadoras aprender y tomar decisiones como los humanos.",
                    "Mistral": "La inteligencia artificial es la simulación de procesos de inteligencia humana en máquinas."
                }
            }
        ]
        
        created_questions = []
        
        for test_data in test_questions:
            # Crear pregunta
            question = QuestionModel(text=test_data["text"], language=test_data["language"])
            db.add(question)
            db.commit()
            db.refresh(question)
            
            # Crear respuestas
            for ai_name, response_text in test_data["responses"].items():
                answer = Answer(question_id=question.id, ai_name=ai_name, response_text=response_text)
                db.add(answer)
            
            created_questions.append({
                "id": question.id,
                "text": question.text,
                "responses_count": len(test_data["responses"])
            })
        
        db.commit()
        
        return {
            "message": f"Se crearon {len(created_questions)} preguntas de prueba",
            "questions": created_questions
        }
        
    except Exception as e:
        db.rollback()
        return {"error": f"Error creando datos de prueba: {str(e)}"}

@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Eliminar respuestas asociadas
    db.query(Answer).filter(Answer.question_id == question_id).delete()

    # Eliminar similitudes asociadas
    #db.query(Similarity).filter(Similarity.question_id == question_id).delete()

    # Eliminar resumen asociado
    db.query(Summary).filter(Summary.question_id == question_id).delete()

    # Eliminar la pregunta
    db.delete(question)
    db.commit()

    return {"message": "Question and related data deleted successfully"}
