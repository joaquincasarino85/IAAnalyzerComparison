import google.generativeai as genai
from IATools.IA import IA

class Gemini(IA):
    def __init__(self, api_key):
        if not api_key or not api_key.strip():
            raise ValueError("API key de Gemini es requerida")
        try:
            genai.configure(api_key=api_key)
            # Usar el modelo correcto para la API v1beta
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise ValueError(f"Error al inicializar cliente de Gemini: {str(e)}")
        
    def get_response(self, question, lang="en"):
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}" 