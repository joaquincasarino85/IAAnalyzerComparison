from IATools.IAFactory import IAFactory
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
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

    async def query_single_ai(self, question: str, ai_name: str, lang: str = "en"):
        """
        Consulta una IA específica de forma asíncrona
        """
        if ai_name not in self.ias:
            raise ValueError(f"IA {ai_name} no está disponible")
        
        full_prompt = self._build_prompt(question, lang, ai_name)
        response = self.ias[ai_name].get_response(full_prompt, lang)
        return response

    async def query_all_ias_parallel(self, question: str, lang: str = "en"):
        """
        Consulta todas las IAs en paralelo de forma asíncrona
        """
        tasks = []
        for name, ia in self.ias.items():
            task = self._query_ai_async(question, lang, name, ia)
            tasks.append(task)
        
        # Ejecutar todas las tareas en paralelo
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados
        result = {}
        for i, (name, _) in enumerate(self.ias.items()):
            if isinstance(responses[i], Exception):
                result[name] = f"Error: {str(responses[i])}"
            else:
                result[name] = responses[i]
        
        return result

    async def _query_ai_async(self, question: str, lang: str, ai_name: str, ia):
        """
        Método auxiliar para consultar una IA de forma asíncrona
        """
        try:
            full_prompt = self._build_prompt(question, lang, ai_name)
            # Como las IAs actuales no son async, las ejecutamos en un thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, ia.get_response, full_prompt, lang)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
