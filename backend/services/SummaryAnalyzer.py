import openai
import os

class SummaryAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("SUMMARY_API_KEY")  # Obtiene la API Key desde .env

    def generate_summary(self, observations, lang="en"):
        if lang == "es":
            prompt = "Resuma las siguientes observaciones de manera concisa:\n\n" + "\n".join(observations)
        elif lang == "en":
            prompt = "Summarize the following observations concisely:\n\n" + "\n".join(observations)
        else:
            prompt = "Summarize the following observations concisely:\n\n" + "\n".join(observations)

        client = openai.OpenAI(api_key=self.api_key)  # Usa el nuevo cliente de OpenAI

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # También puedes usar "gpt-3.5-turbo" si no tienes acceso a GPT-4
            messages=[{"role": "system", "content": prompt}]
        )

        return response.choices[0].message.content  # Nuevo formato de respuesta en OpenAI 1.0.0
