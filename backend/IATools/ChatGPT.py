import openai
import os

from IATools.IA import IA

class ChatGPT(IA):
    def __init__(self, api_key):
        self.client = openai.Client(api_key=api_key)

    def get_response(self, question: str, language: str = "en") -> str:
        try:
            # Mensaje de sistema: instrucciones de idioma y estilo de respuesta
            system_message = {
                "role": "system",
                "content": (
                    f"You are a helpful assistant. Always respond in {language.upper()}. "
                    "Keep answers concise, direct, and structured. Avoid introductions. "
                    "Use bullet points if possible."
                )
            }

            user_message = {"role": "user", "content": question}

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[system_message, user_message]
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Error in ChatGPT: {e}"
