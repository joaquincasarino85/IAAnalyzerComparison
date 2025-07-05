from fastapi import APIRouter, HTTPException
from typing import Dict, List
import sys
import os

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.ai_config import ai_config_manager

router = APIRouter(prefix="/ai-info", tags=["AI Information"])

@router.get("/available")
async def get_available_ais():
    """Obtiene la lista de IAs disponibles (habilitadas y con API key)"""
    try:
        available_ais = ai_config_manager.get_enabled_ais()
        return {
            "available_ais": available_ais,
            "total_available": len(available_ais)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener IAs disponibles: {str(e)}")

@router.get("/all")
async def get_all_ai_info():
    """Obtiene información detallada de todas las IAs configuradas"""
    try:
        ai_info = ai_config_manager.get_ai_info()
        return {
            "ai_configurations": ai_info,
            "total_configured": len(ai_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información de IAs: {str(e)}")

@router.get("/{ai_name}")
async def get_ai_details(ai_name: str):
    """Obtiene información detallada de una IA específica"""
    try:
        config = ai_config_manager.get_config(ai_name)
        if not config:
            raise HTTPException(status_code=404, detail=f"IA '{ai_name}' no encontrada")
        
        return {
            "name": config.name,
            "enabled": config.enabled,
            "available": ai_config_manager.is_available(ai_name),
            "description": config.description,
            "strengths": config.strengths,
            "weaknesses": config.weaknesses,
            "model_name": config.model_name,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "has_api_key": ai_config_manager._has_api_key(config)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalles de la IA: {str(e)}")

@router.post("/{ai_name}/enable")
async def enable_ai(ai_name: str):
    """Habilita una IA específica"""
    try:
        success = ai_config_manager.enable_ai(ai_name)
        if not success:
            raise HTTPException(status_code=404, detail=f"IA '{ai_name}' no encontrada")
        
        return {
            "message": f"IA '{ai_name}' habilitada exitosamente",
            "ai_name": ai_name,
            "enabled": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al habilitar la IA: {str(e)}")

@router.post("/{ai_name}/disable")
async def disable_ai(ai_name: str):
    """Deshabilita una IA específica"""
    try:
        success = ai_config_manager.disable_ai(ai_name)
        if not success:
            raise HTTPException(status_code=404, detail=f"IA '{ai_name}' no encontrada")
        
        return {
            "message": f"IA '{ai_name}' deshabilitada exitosamente",
            "ai_name": ai_name,
            "enabled": False
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al deshabilitar la IA: {str(e)}")

@router.get("/status/summary")
async def get_ai_status_summary():
    """Obtiene un resumen del estado de todas las IAs"""
    try:
        ai_info = ai_config_manager.get_ai_info()
        
        total_configured = len(ai_info)
        total_enabled = sum(1 for info in ai_info.values() if info["enabled"])
        total_available = sum(1 for info in ai_info.values() if info["available"])
        
        # Agrupar por estado
        status_groups = {
            "available": [],
            "enabled_no_key": [],
            "disabled": []
        }
        
        for name, info in ai_info.items():
            if info["available"]:
                status_groups["available"].append(name)
            elif info["enabled"]:
                status_groups["enabled_no_key"].append(name)
            else:
                status_groups["disabled"].append(name)
        
        return {
            "summary": {
                "total_configured": total_configured,
                "total_enabled": total_enabled,
                "total_available": total_available,
                "total_unavailable": total_configured - total_available
            },
            "status_groups": status_groups,
            "recommendations": _generate_recommendations(ai_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener resumen de estado: {str(e)}")

def _generate_recommendations(ai_info: Dict) -> List[str]:
    """Genera recomendaciones basadas en el estado de las IAs"""
    recommendations = []
    
    available_count = sum(1 for info in ai_info.values() if info["available"])
    
    if available_count == 0:
        recommendations.append("No hay IAs disponibles. Configura al menos una API key.")
    elif available_count < 3:
        recommendations.append(f"Solo {available_count} IA(s) disponible(s). Considera agregar más para mejor comparación.")
    
    enabled_no_key = [name for name, info in ai_info.items() if info["enabled"] and not info["available"]]
    if enabled_no_key:
        recommendations.append(f"IAs habilitadas sin API key: {', '.join(enabled_no_key)}. Configura las API keys correspondientes.")
    
    return recommendations 