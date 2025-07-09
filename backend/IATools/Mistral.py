import requests
from IATools.IA import IA

class Mistral(IA):
    def __init__(self, api_key):
        if not api_key or not api_key.strip():
            raise ValueError("API key de Mistral es requerida")
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1"
        
    def get_response(self, question, lang="en"):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "mistral-large-latest",
                "messages": [
                    {"role": "user", "content": question}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}" 