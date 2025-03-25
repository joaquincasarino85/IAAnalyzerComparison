
import openai
import os

from IATools.IA import IA


class ChatGPT(IA):
    def __init__(self, api_key):
        self.client = openai.Client(api_key=api_key)

    def get_response(self, question: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Asegúrate de que tienes acceso a este modelo
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in ChatGPT: {e}"