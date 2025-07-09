import anthropic
from IATools.IA import IA

class Claude(IA):
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def get_response(self, question, lang="en"):
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}" 