from difflib import SequenceMatcher

class SimilarityAnalyzer:
    @staticmethod
    def analyze(responses):
        ai_names = list(responses.keys())
        analysis = {}

        for i in range(len(ai_names)):
            for j in range(i + 1, len(ai_names)):
                ai1, ai2 = ai_names[i], ai_names[j]
                similarity = SequenceMatcher(None, responses[ai1], responses[ai2]).ratio()
                analysis[f"{ai1} vs {ai2}"] = similarity

        return analysis
