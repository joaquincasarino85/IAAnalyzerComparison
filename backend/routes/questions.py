from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.IAManager import IAManager
from backend.services.SimilarityAnalyzer import SimilarityAnalyzer
from backend.services.SummaryAnalyzer import SummaryAnalyzer
from backend.models.question import Question as QuestionModel
from backend.models.response import Response as Answer
from backend.models.summary import Summary as Summary
#from backend.models.similariry import Similarity as Similarity
from backend.database import get_db
from backend.schemas.question import QuestionRequest

router = APIRouter()

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

    # 5️⃣ Generar y guardar el resumen en la base de datos
    summary_analyzer = SummaryAnalyzer()
    summary_text = summary_analyzer.generate_summary(list(responses.values()))

    new_summary = Summary(question_id=new_question.id, summary_text=summary_text)  # ⬅ Creando el objeto
    db.add(new_summary)  # ⬅ Agregando a la base de datos
    db.commit()  # ⬅ Guardando cambios en la base de datos
    db.refresh(new_summary)  # ⬅ Refrescando el objeto para obtener ID

    return {
        "question": new_question.text,
        "responses": responses,
        "similarities": similarity_results,
        "summary": summary_text
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
            "answers": [{"ai_name": a.ai_name, "response": a.response_text} for a in answers]
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
