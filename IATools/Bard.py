
import google.generativeai as genai
import os


from IATools.IA import IA

class Bard(IA):
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("No API Key Gemini")
        genai.configure(api_key=self.api_key)

    def get_response(self, question: str) -> str:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error Bard: {e}"