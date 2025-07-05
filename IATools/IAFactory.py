from IATools.ChatGPT import ChatGPT
from IATools.Bard import Bard
from IATools.PerplexityIA import PerplexityIA
from IATools.Claude import Claude
from IATools.Gemini import Gemini
from IATools.Mistral import Mistral
from IATools.Cohere import Cohere

class IAFactory:
    @staticmethod
    def create_ia(ai_type: str, api_key=None):
        if ai_type == "ChatGPT":
            return ChatGPT(api_key)
        elif ai_type == "Bard":
            return Bard(api_key)
        elif ai_type == "Perplexity":
            return PerplexityIA(api_key)
        elif ai_type == "Claude":
            return Claude(api_key)
        elif ai_type == "Gemini":
            return Gemini(api_key)
        elif ai_type == "Mistral":
            return Mistral(api_key)
        elif ai_type == "Cohere":
            return Cohere(api_key)
        else:
            raise ValueError(f"IA not supported: {ai_type}")