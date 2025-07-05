import requests

class PerplexityIA:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.perplexity.ai/chat/completions"

    def get_response(self, prompt: str, language: str = "en") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Mapa de idiomas
        lang_instruction = {
            "es": "en español",
            "en": "in English",
            "fr": "en français",
            "de": "auf Deutsch",
            "it": "in italiano"
        }.get(language, "in English")

        style_instruction = (
            "Responde de forma breve, directa, estructurada y clara. "
            "No uses introducciones ni explicaciones innecesarias. Usa viñetas si aplica."
        )

        # Construir mensaje con instrucciones explícitas
        full_prompt = (
            f"Responde {lang_instruction} la siguiente consulta de forma clara, concisa y estructurada. "
            f"Evita introducciones, contexto innecesario o reflexiones. "
            f"Limita la respuesta a 5 viñetas con los puntos clave. "
            f"No incluyas notas finales ni advertencias. Solo hechos relevantes.\n\n"
            f"{prompt}"
        )

        payload = {
            "model": "r1-1776",
            "messages": [
                {"role": "user", "content": full_prompt}
            ]
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"🚨 Perplexity Error: {response.status_code}")
            print(response.text)
            return f"[Perplexity ERROR {response.status_code}] {response.json().get('error', {}).get('message', 'Unknown error')}"

        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]

        # Opcional: eliminar secciones como <think> si aún aparecen
        if "<think>" in result:
            result = result.split("</think>")[-1].strip()

        return result
