"""
Configuración para las integraciones de IA
"""
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AIConfig:
    """Configuración para un modelo de IA específico"""
    name: str
    api_key_env: str
    enabled: bool = True
    max_tokens: int = 1000
    temperature: float = 0.7
    model_name: Optional[str] = None
    description: str = ""
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []

class AIConfigManager:
    """Gestor de configuración para todos los modelos de IA"""
    
    def __init__(self):
        self.ai_configs = {
            "ChatGPT": AIConfig(
                name="ChatGPT",
                api_key_env="OPENAI_API_KEY",
                model_name="gpt-3.5-turbo",
                description="Modelo conversacional de OpenAI, excelente para respuestas detalladas y creativas",
                strengths=["Creatividad", "Respuestas detalladas", "Flexibilidad"],
                weaknesses=["Puede ser verboso", "Costos variables"]
            ),
            "Claude": AIConfig(
                name="Claude",
                api_key_env="ANTHROPIC_API_KEY",
                model_name="claude-3-sonnet-20240229",
                description="Modelo de Anthropic con excelente razonamiento y análisis",
                strengths=["Razonamiento lógico", "Análisis profundo", "Precisión"],
                weaknesses=["Respuestas más conservadoras", "Menos creativo"]
            ),
            "Gemini": AIConfig(
                name="Gemini",
                api_key_env="GEMINI_API_KEY",
                model_name="gemini-pro",
                description="Modelo de Google con buen equilibrio entre creatividad y precisión",
                strengths=["Equilibrio", "Bien estructurado", "Multimodal"],
                weaknesses=["Limitaciones en ciertos temas", "Menos personalizable"]
            ),
            "Mistral": AIConfig(
                name="Mistral",
                api_key_env="MISTRAL_API_KEY",
                model_name="mistral-large-latest",
                description="Modelo técnico y preciso, excelente para análisis detallados",
                strengths=["Precisión técnica", "Análisis detallado", "Eficiencia"],
                weaknesses=["Menos conversacional", "Respuestas más secas"]
            ),
            "Cohere": AIConfig(
                name="Cohere",
                api_key_env="COHERE_API_KEY",
                model_name="command",
                description="Modelo basado en comandos, ideal para tareas específicas",
                strengths=["Respuestas directas", "Eficiencia", "Control"],
                weaknesses=["Menos conversacional", "Limitado en creatividad"]
            ),
            "Perplexity": AIConfig(
                name="Perplexity",
                api_key_env="PERPLEXITY_API_KEY",
                model_name="llama-3.1-sonar-small-128k-online",
                description="Modelo con acceso a internet y fuentes, excelente para información actualizada",
                strengths=["Información actualizada", "Fuentes verificables", "Investigación"],
                weaknesses=["Dependiente de fuentes", "Puede ser lento"]
            )
        }
    
    def get_enabled_ais(self) -> List[str]:
        """Retorna la lista de IAs habilitadas"""
        enabled = []
        for name, config in self.ai_configs.items():
            if config.enabled and self._has_api_key(config):
                enabled.append(name)
        return enabled
    
    def get_config(self, ai_name: str) -> Optional[AIConfig]:
        """Obtiene la configuración de una IA específica"""
        return self.ai_configs.get(ai_name)
    
    def is_available(self, ai_name: str) -> bool:
        """Verifica si una IA está disponible (habilitada y con API key)"""
        config = self.get_config(ai_name)
        if not config:
            return False
        return config.enabled and self._has_api_key(config)
    
    def _has_api_key(self, config: AIConfig) -> bool:
        """Verifica si existe la API key para una configuración"""
        api_key = os.getenv(config.api_key_env)
        return api_key is not None and api_key.strip() != ""
    
    def get_api_key(self, ai_name: str) -> Optional[str]:
        """Obtiene la API key de una IA específica"""
        config = self.get_config(ai_name)
        if not config:
            return None
        return os.getenv(config.api_key_env)
    
    def enable_ai(self, ai_name: str) -> bool:
        """Habilita una IA específica"""
        config = self.get_config(ai_name)
        if config:
            config.enabled = True
            return True
        return False
    
    def disable_ai(self, ai_name: str) -> bool:
        """Deshabilita una IA específica"""
        config = self.get_config(ai_name)
        if config:
            config.enabled = False
            return True
        return False
    
    def get_ai_info(self) -> Dict[str, Dict]:
        """Retorna información detallada de todas las IAs"""
        info = {}
        for name, config in self.ai_configs.items():
            info[name] = {
                "name": config.name,
                "enabled": config.enabled,
                "available": self.is_available(name),
                "description": config.description,
                "strengths": config.strengths or [],
                "weaknesses": config.weaknesses or [],
                "model_name": config.model_name,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            }
        return info
    
    def update_config(self, ai_name: str, **kwargs) -> bool:
        """Actualiza la configuración de una IA específica"""
        config = self.get_config(ai_name)
        if not config:
            return False
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return True

# Instancia global del gestor de configuración
ai_config_manager = AIConfigManager() 