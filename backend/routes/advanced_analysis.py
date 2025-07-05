from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import os

# Agregar el directorio padre al path para importar servicios
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.AdvancedResponseAnalyzer import AdvancedResponseAnalyzer
from services.IntelligentComparator import IntelligentComparator
from services.IAManager import IAManager
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(prefix="/advanced-analysis", tags=["Advanced Analysis"])

@router.post("/analyze-responses")
async def analyze_responses(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Analiza las respuestas de una pregunta específica con métricas avanzadas"""
    try:
        # Obtener respuestas de la base de datos
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if not responses_db:
            raise HTTPException(status_code=404, detail="No se encontraron respuestas para esta pregunta")
        
        # Convertir a formato esperado por el analizador
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Realizar análisis avanzado
        analyzer = AdvancedResponseAnalyzer()
        analysis_results = analyzer.analyze_responses(responses)
        
        return {
            "question_id": question_id,
            "analysis": analysis_results,
            "summary": {
                "total_responses": len(responses),
                "average_quality_score": sum(
                    result.get("response_quality_score", 0) for result in analysis_results.values()
                ) / len(analysis_results) if analysis_results else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

@router.post("/compare-intelligently")
async def compare_responses_intelligently(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Compara inteligentemente las respuestas de una pregunta"""
    try:
        # Obtener respuestas de la base de datos
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if len(responses_db) < 2:
            raise HTTPException(status_code=400, detail="Se necesitan al menos 2 respuestas para comparar")
        
        # Convertir a formato esperado
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Realizar comparación inteligente
        comparator = IntelligentComparator()
        comparison_results = comparator.compare_responses(responses)
        
        return {
            "question_id": question_id,
            "comparison": comparison_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la comparación: {str(e)}")

@router.post("/quality-assessment")
async def assess_response_quality(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Evalúa la calidad de las respuestas con métricas detalladas"""
    try:
        # Obtener respuestas
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if not responses_db:
            raise HTTPException(status_code=404, detail="No se encontraron respuestas")
        
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Análisis de calidad
        analyzer = AdvancedResponseAnalyzer()
        quality_analysis = analyzer.analyze_responses(responses)
        
        # Ranking de calidad
        quality_rankings = []
        for ai_name, analysis in quality_analysis.items():
            quality_rankings.append({
                "ai_name": ai_name,
                "quality_score": analysis.get("response_quality_score", 0),
                "readability": analysis.get("readability", {}),
                "conciseness": analysis.get("conciseness", {}),
                "structure": analysis.get("structure", {}),
                "vocabulary": analysis.get("vocabulary", {}),
                "factual_indicators": analysis.get("factual_indicators", {}),
                "confidence_indicators": analysis.get("confidence_indicators", {})
            })
        
        # Ordenar por score de calidad
        quality_rankings.sort(key=lambda x: x["quality_score"], reverse=True)
        
        return {
            "question_id": question_id,
            "quality_rankings": quality_rankings,
            "best_response": quality_rankings[0] if quality_rankings else None,
            "average_quality": sum(r["quality_score"] for r in quality_rankings) / len(quality_rankings) if quality_rankings else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la evaluación: {str(e)}")

@router.post("/consensus-analysis")
async def analyze_consensus(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Analiza el consenso entre las respuestas de diferentes AI"""
    try:
        # Obtener respuestas
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if len(responses_db) < 2:
            raise HTTPException(status_code=400, detail="Se necesitan al menos 2 respuestas para analizar consenso")
        
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Análisis de consenso
        comparator = IntelligentComparator()
        comparison = comparator.compare_responses(responses)
        
        consensus_analysis = comparison.get("consensus_analysis", {})
        
        return {
            "question_id": question_id,
            "consensus_analysis": consensus_analysis,
            "agreement_level": consensus_analysis.get("agreement_level", 0),
            "consensus_score": consensus_analysis.get("consensus_score", 0),
            "consensus_points": consensus_analysis.get("consensus_points", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis de consenso: {str(e)}")

@router.post("/divergence-analysis")
async def analyze_divergence(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Analiza las divergencias entre las respuestas"""
    try:
        # Obtener respuestas
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if len(responses_db) < 2:
            raise HTTPException(status_code=400, detail="Se necesitan al menos 2 respuestas para analizar divergencias")
        
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Análisis de divergencia
        comparator = IntelligentComparator()
        comparison = comparator.compare_responses(responses)
        
        divergence_analysis = comparison.get("divergence_analysis", {})
        
        return {
            "question_id": question_id,
            "divergence_analysis": divergence_analysis,
            "divergence_score": divergence_analysis.get("divergence_score", 0),
            "unique_points": divergence_analysis.get("unique_points", {}),
            "contradictions": divergence_analysis.get("contradictions", []),
            "different_approaches": divergence_analysis.get("different_approaches", {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis de divergencia: {str(e)}")

@router.get("/recommendations/{question_id}")
async def get_recommendations(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene recomendaciones basadas en el análisis de respuestas"""
    try:
        # Obtener respuestas
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if not responses_db:
            raise HTTPException(status_code=404, detail="No se encontraron respuestas")
        
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Generar recomendaciones
        comparator = IntelligentComparator()
        comparison = comparator.compare_responses(responses)
        
        recommendations = comparison.get("recommendations", {})
        
        return {
            "question_id": question_id,
            "recommendations": recommendations,
            "best_overall": recommendations.get("best_overall", []),
            "most_concise": recommendations.get("most_concise", []),
            "most_detailed": recommendations.get("most_detailed", []),
            "improvement_suggestions": recommendations.get("improvement_suggestions", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")

@router.get("/detailed-comparison/{question_id}")
async def get_detailed_comparison(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene comparaciones detalladas entre pares de AI"""
    try:
        # Obtener respuestas
        from models.response import Response
        responses_db = db.query(Response).filter(Response.question_id == question_id).all()
        
        if len(responses_db) < 2:
            raise HTTPException(status_code=400, detail="Se necesitan al menos 2 respuestas para comparar")
        
        responses = {resp.ai_name: resp.content for resp in responses_db}
        
        # Comparación detallada
        comparator = IntelligentComparator()
        comparison = comparator.compare_responses(responses)
        
        detailed_comparisons = comparison.get("detailed_comparisons", {})
        
        return {
            "question_id": question_id,
            "detailed_comparisons": detailed_comparisons,
            "total_comparisons": len(detailed_comparisons)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la comparación detallada: {str(e)}") 