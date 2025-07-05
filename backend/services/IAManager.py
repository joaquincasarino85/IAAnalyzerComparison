from IATools.IAFactory import IAFactory
from dotenv import load_dotenv
import os
load_dotenv()


class IAManager:
    def __init__(self):
        self.ias = {}
        self.responses = {}
        
        # Crear instancias de IA solo si tienen API keys válidas
        ai_configs = [
            ("ChatGPT", "OPENAI_API_KEY"),
            #("Claude", "ANTHROPIC_API_KEY"),  # Comentado por ahora
            ("Gemini", "GEMINI_API_KEY"),
            ("Mistral", "MISTRAL_API_KEY"),
            ("Cohere", "COHERE_API_KEY"),
            ("Perplexity", "PERPLEXITY_API_KEY")
        ]
        
        for ai_name, env_key in ai_configs:
            api_key = os.getenv(env_key)
            if api_key and api_key.strip():  # Verificar que la API key existe y no está vacía
                try:
                    self.ias[ai_name] = IAFactory.create_ia(ai_name, api_key)
                    print(f"✅ {ai_name} inicializado correctamente")
                except Exception as e:
                    print(f"❌ Error al inicializar {ai_name}: {str(e)}")
            else:
                print(f"⚠️ {ai_name} no configurado (API key faltante)")

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
