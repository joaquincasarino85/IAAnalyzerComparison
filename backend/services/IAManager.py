from IATools.IAFactory import IAFactory
from dotenv import load_dotenv
import os
load_dotenv()


class IAManager:
    def __init__(self):
        self.ias = {
            "ChatGPT": IAFactory.create_ia("ChatGPT", os.getenv("OPENAI_API_KEY")),
            "Bard": IAFactory.create_ia("Bard", os.getenv("GEMINI_API_KEY")),
            "Perplexity": IAFactory.create_ia("Perplexity", os.getenv("PERPLEXITY_API_KEY"))
        }
        self.responses = {}

    def query_ias(self, question: str):
        self.responses = {name: ia.get_response(question) for name, ia in self.ias.items()}

    def get_responses(self):
        return self.responses
