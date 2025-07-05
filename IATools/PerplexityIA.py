# IATools/PerplexityIA.py

import requests

class PerplexityIA:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.perplexity.ai/chat/completions"

    def get_response(self, prompt, language: str = "en"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "r1-1776",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"🚨 Perplexity Error: {response.status_code}")
            print(response.text)
            return f"[Perplexity ERROR {response.status_code}] {response.json().get('error', {}).get('message', 'Unknown error')}"

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

