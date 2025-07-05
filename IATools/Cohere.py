import cohere
from IATools.IA import IA

class Cohere(IA):
    def __init__(self, api_key):
        if not api_key or not api_key.strip():
            raise ValueError("API key de Cohere es requerida")
        try:
            self.co = cohere.Client(api_key)
        except Exception as e:
            raise ValueError(f"Error al inicializar cliente de Cohere: {str(e)}")
        
    def get_response(self, question, lang="en"):
        try:
            response = self.co.generate(
                model='command',
                prompt=question,
                max_tokens=1000,
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            return response.generations[0].text
        except Exception as e:
            return f"Error: {str(e)}" 