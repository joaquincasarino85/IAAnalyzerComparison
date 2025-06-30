from IATools.ChatGPT import ChatGPT
from IATools.Bard import Bard
from IATools.PerplexityIA import PerplexityIA

class IAFactory:
    @staticmethod
    def create_ia(ai_type: str, api_key=None):
        if ai_type == "ChatGPT":
            return ChatGPT(api_key)
        elif ai_type == "Bard":
            return Bard(api_key)
        elif ai_type == "Perplexity":
            return PerplexityIA(api_key)
        else:
            raise ValueError("IA not supported")