from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.IAManager import IAManager
from backend.services.SimilarityAnalyzer import SimilarityAnalyzer
from backend.services.SummaryAnalyzer import SummaryAnalyzer
from backend.models.question import Question as QuestionModel
from backend.models.response import Response as Answer
from backend.models.summary import Summary as Summary
from backend.models.similarity import Similarity as Similarity
from backend.models.semantic_similarity import SemanticSimilarity as SemanticSimilarity
from backend.models.contradiction import Contradiction as Contradiction
from backend.models.named_entity import NamedEntity as NamedEntity
from backend.models.sentiment import Sentiment as Sentiment
from backend.database import get_db
from backend.schemas.question import QuestionRequest
from backend.services.NLPAnalyzer import NLPAnalyzer
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

    # 1️⃣ Guardar la pregunta en la base de datos
    new_question = QuestionModel(text=question_request.text)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # 2️⃣ Llamar al IA Manager
    manager = IAManager()
    manager.query_ias(question_request.text)
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
    summary_text = summary_analyzer.generate_summary(list(responses.values()))

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
