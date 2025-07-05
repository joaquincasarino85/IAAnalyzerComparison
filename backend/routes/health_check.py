from fastapi import APIRouter, HTTPException
from typing import Dict, List
import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.IAManager import IAManager

router = APIRouter(prefix="/health", tags=["Health Check"])

@router.get("/ai-status")
async def check_ai_status():
    """Verifica el estado de todas las IAs configuradas"""
    try:
        # Crear una instancia temporal del IAManager para verificar
        manager = IAManager()
        
        # Obtener información de las IAs disponibles
        available_ais = list(manager.ias.keys())
        
        # Verificar API keys
        api_keys_status = {}
        api_keys = {
            "OPENAI_API_KEY": "ChatGPT",
            "ANTHROPIC_API_KEY": "Claude",
            "GEMINI_API_KEY": "Gemini", 
            "MISTRAL_API_KEY": "Mistral",
            "COHERE_API_KEY": "Cohere",
            "PERPLEXITY_API_KEY": "Perplexity"
        }
        
        for env_key, ai_name in api_keys.items():
            api_key = os.getenv(env_key)
            if api_key and api_key.strip() and len(api_key.strip()) > 10:
                api_keys_status[ai_name] = {
                    "configured": True,
                    "status": "available" if ai_name in available_ais else "error"
                }
            else:
                api_keys_status[ai_name] = {
                    "configured": False,
                    "status": "missing_key"
                }
        
        return {
            "status": "healthy" if available_ais else "degraded",
            "available_ais": available_ais,
            "total_available": len(available_ais),
            "api_keys_status": api_keys_status,
            "recommendations": _generate_recommendations(available_ais, api_keys_status)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar estado: {str(e)}")

@router.get("/test-connection")
async def test_ai_connections():
    """Prueba la conexión con las IAs disponibles"""
    try:
        manager = IAManager()
        
        if not manager.ias:
            return {
                "status": "no_ais_configured",
                "message": "No hay IAs configuradas correctamente"
            }
        
        # Probar con una pregunta simple
        test_question = "Hello, this is a test. Please respond with 'OK' if you can read this."
        
        results = {}
        for ai_name, ia in manager.ias.items():
            try:
                response = ia.get_response(test_question)
                if response and not response.startswith("Error:"):
                    results[ai_name] = {
                        "status": "connected",
                        "response_preview": response[:100] + "..." if len(response) > 100 else response
                    }
                else:
                    results[ai_name] = {
                        "status": "error",
                        "error": response
                    }
            except Exception as e:
                results[ai_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        successful_connections = sum(1 for result in results.values() if result["status"] == "connected")
        
        return {
            "status": "test_completed",
            "total_tested": len(results),
            "successful_connections": successful_connections,
            "failed_connections": len(results) - successful_connections,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al probar conexiones: {str(e)}")

def _generate_recommendations(available_ais: List[str], api_keys_status: Dict) -> List[str]:
    """Genera recomendaciones basadas en el estado actual"""
    recommendations = []
    
    if not available_ais:
        recommendations.append("No hay IAs disponibles. Configura al menos una API key válida.")
    
    if len(available_ais) < 2:
        recommendations.append("Solo una IA disponible. Considera configurar más para comparaciones.")
    
    # Verificar IAs con API keys pero sin conexión
    configured_but_unavailable = [
        ai_name for ai_name, status in api_keys_status.items()
        if status["configured"] and status["status"] == "error"
    ]
    
    if configured_but_unavailable:
        recommendations.append(f"IAs con API key pero sin conexión: {', '.join(configured_but_unavailable)}")
    
    # Verificar IAs populares no configuradas
    popular_ais = ["ChatGPT", "Gemini", "Claude"]
    missing_popular = [ai for ai in popular_ais if ai not in available_ais]
    
    if missing_popular:
        recommendations.append(f"IAs populares no configuradas: {', '.join(missing_popular)}")
    
    return recommendations 