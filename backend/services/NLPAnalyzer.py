# 📁 backend/services/NLPAnalyzer.py

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from transformers import AutoTokenizer
from difflib import SequenceMatcher

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

def truncate_text(text, max_tokens=512):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)

class NLPAnalyzer:
    def __init__(self, responses):
        self.responses = responses
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = pipeline("text-classification", model="roberta-large-mnli")
        self.ner = pipeline("ner", grouped_entities=True)
        self.sentiment = pipeline("sentiment-analysis")

    def analyze_semantic_similarity(self):
        ai_names = list(self.responses.keys())
        results = []

        for i in range(len(ai_names)):
            for j in range(i + 1, len(ai_names)):
                ai1, ai2 = ai_names[i], ai_names[j]
                emb1 = self.model.encode(self.responses[ai1], convert_to_tensor=True)
                emb2 = self.model.encode(self.responses[ai2], convert_to_tensor=True)
                score = util.cos_sim(emb1, emb2).item()
                results.append({"ai1": ai1, "ai2": ai2, "score": score})

        return results

    def detect_contradictions(self):
        ai_names = list(self.responses.keys())
        results = []

        for i in range(len(ai_names)):
            for j in range(i + 1, len(ai_names)):
                ai1, ai2 = ai_names[i], ai_names[j]
                max_length = 512
                text1 = self.responses[ai1][:max_length // 2]
                text2 = self.responses[ai2][:max_length // 2]
                input_text = f"{text1} [SEP] {text2}"

                result = self.classifier(input_text)[0]

                results.append({"ai1": ai1, "ai2": ai2, "label": result['label'], "score": result['score']})

        return results

    def extract_named_entities(self):
        results = {}
        for ai, response in self.responses.items():
            results[ai] = self.ner(response)
        return results

    def analyze_sentiment(self):
        results = {}
        for ai, response in self.responses.items():
            if not response:
                continue
            text = truncate_text(response)
            results[ai] = self.sentiment(text)
        return results

