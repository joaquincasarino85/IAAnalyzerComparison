from IATools.IAFactory import IAFactory
from dotenv import load_dotenv
import os
load_dotenv()


class IAManager:
    def __init__(self):
        self.ias = {
            "ChatGPT": IAFactory.create_ia("ChatGPT", os.getenv("OPENAI_API_KEY")),
            # "Bard": IAFactory.create_ia("Bard", os.getenv("GEMINI_API_KEY")),
            "Perplexity": IAFactory.create_ia("Perplexity", os.getenv("PERPLEXITY_API_KEY"))
        }
        self.responses = {}

    def query_ias(self, question: str, lang: str = "en"):
        self.responses = {}
        for name, ia in self.ias.items():
            full_prompt = self._build_prompt(question, lang, name)
            self.responses[name] = ia.get_response(full_prompt, lang)

    def _build_prompt(self, question: str, lang: str, ia_name: str) -> str:
        if lang not in ["es", "en", "fr", "de", "it"]:
            lang = "en"

        lang_instruction = {
            "es": "en español",
            "en": "in English",
            "fr": "en français",
            "de": "auf Deutsch",
            "it": "in italiano"
        }.get(lang, "in English")

        # Prompt base estructurado y conciso
        style_instruction = (
            "Use a concise and structured format. "
            "Avoid introductions. Highlight only key points. Use bullet points when possible."
        )

        if ia_name == "Perplexity":
            return (
                f"Please answer {lang_instruction} the following question. "
                f"{style_instruction}\n\n{question}"
            )
        else:
            return (
                f"Please respond {lang_instruction} to the following question. "
                f"{style_instruction}\n\n{question}"
            )

    def get_responses(self):
        return self.responses
