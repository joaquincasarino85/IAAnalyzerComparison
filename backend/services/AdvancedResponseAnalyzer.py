import re
from typing import Dict, List, Tuple
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class AdvancedResponseAnalyzer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def analyze_responses(self, responses: Dict[str, str]) -> Dict[str, Dict]:
        """Analiza todas las respuestas y retorna métricas detalladas"""
        analysis_results = {}
        
        for ai_name, response in responses.items():
            if not response or response.startswith("Error:"):
                continue
                
            analysis_results[ai_name] = {
                "readability": self._calculate_readability(response),
                "conciseness": self._calculate_conciseness(response),
                "structure": self._analyze_structure(response),
                "vocabulary": self._analyze_vocabulary(response),
                "factual_indicators": self._detect_factual_indicators(response),
                "confidence_indicators": self._detect_confidence_indicators(response),
                "response_quality_score": 0.0
            }
            
            # Calcular score de calidad general
            analysis_results[ai_name]["response_quality_score"] = self._calculate_quality_score(
                analysis_results[ai_name]
            )
            
        return analysis_results
    
    def _calculate_readability(self, text: str) -> Dict[str, float]:
        """Calcula métricas de legibilidad"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha()]
        
        if not sentences or not words:
            return {"flesch_score": 0, "avg_sentence_length": 0, "avg_word_length": 0}
        
        # Flesch Reading Ease Score
        syllables = self._count_syllables(text)
        flesch_score = 206.835 - (1.015 * len(sentences) / len(words) * 100) - (84.6 * syllables / len(words))
        flesch_score = max(0, min(100, flesch_score))
        
        return {
            "flesch_score": round(flesch_score, 2),
            "avg_sentence_length": round(len(words) / len(sentences), 2),
            "avg_word_length": round(sum(len(word) for word in words) / len(words), 2)
        }
    
    def _calculate_conciseness(self, text: str) -> Dict[str, float]:
        """Calcula métricas de concisión"""
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha()]
        
        # Eliminar palabras de relleno
        content_words = [word for word in words if word not in self.stop_words]
        
        return {
            "content_word_ratio": round(len(content_words) / len(words) if words else 0, 3),
            "words_per_sentence": round(len(words) / len(sentences) if sentences else 0, 2),
            "redundancy_score": self._calculate_redundancy(text)
        }
    
    def _analyze_structure(self, text: str) -> Dict[str, any]:
        """Analiza la estructura del texto"""
        sentences = sent_tokenize(text)
        
        # Detectar listas y bullet points
        bullet_patterns = [r'^\s*[-•*]\s+', r'^\s*\d+\.\s+']
        bullet_count = sum(len(re.findall(pattern, text, re.MULTILINE)) for pattern in bullet_patterns)
        
        # Detectar párrafos
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Detectar conectores lógicos
        logical_connectors = [
            'however', 'therefore', 'furthermore', 'moreover', 'consequently',
            'additionally', 'nevertheless', 'nonetheless', 'thus', 'hence'
        ]
        connector_count = sum(1 for connector in logical_connectors if connector.lower() in text.lower())
        
        return {
            "bullet_points": bullet_count,
            "paragraphs": len(paragraphs),
            "logical_connectors": connector_count,
            "has_introduction": self._has_introduction(text),
            "has_conclusion": self._has_conclusion(text)
        }
    
    def _analyze_vocabulary(self, text: str) -> Dict[str, any]:
        """Analiza el vocabulario usado"""
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha()]
        
        # Diversidad léxica
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Palabras complejas (más de 6 letras)
        complex_words = [word for word in words if len(word) > 6]
        complex_word_ratio = len(complex_words) / len(words) if words else 0
        
        # Palabras técnicas (detectar patrones)
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acrónimos
            r'\b\w+[a-z]+[A-Z]\w+\b',  # camelCase
            r'\b\w+_\w+\b'  # snake_case
        ]
        technical_terms = set()
        for pattern in technical_patterns:
            technical_terms.update(re.findall(pattern, text))
        
        return {
            "lexical_diversity": round(lexical_diversity, 3),
            "complex_word_ratio": round(complex_word_ratio, 3),
            "technical_terms": len(technical_terms),
            "vocabulary_richness": self._calculate_vocabulary_richness(words)
        }
    
    def _detect_factual_indicators(self, text: str) -> Dict[str, int]:
        """Detecta indicadores de factualidad"""
        factual_phrases = [
            'according to', 'research shows', 'studies indicate', 'data suggests',
            'evidence shows', 'statistics show', 'reports indicate', 'analysis reveals',
            'findings show', 'results indicate', 'survey shows', 'experts say'
        ]
        
        uncertainty_phrases = [
            'might be', 'could be', 'possibly', 'perhaps', 'maybe', 'potentially',
            'it seems', 'appears to', 'suggests', 'indicates', 'may be'
        ]
        
        factual_count = sum(1 for phrase in factual_phrases if phrase.lower() in text.lower())
        uncertainty_count = sum(1 for phrase in uncertainty_phrases if phrase.lower() in text.lower())
        
        return {
            "factual_indicators": factual_count,
            "uncertainty_indicators": uncertainty_count,
            "factual_confidence": max(0, factual_count - uncertainty_count)
        }
    
    def _detect_confidence_indicators(self, text: str) -> Dict[str, int]:
        """Detecta indicadores de confianza"""
        confident_phrases = [
            'definitely', 'certainly', 'clearly', 'obviously', 'undoubtedly',
            'without doubt', 'absolutely', 'positively', 'assuredly'
        ]
        
        cautious_phrases = [
            'i think', 'in my opinion', 'it seems', 'appears', 'might',
            'could', 'possibly', 'perhaps', 'maybe', 'i believe'
        ]
        
        confident_count = sum(1 for phrase in confident_phrases if phrase.lower() in text.lower())
        cautious_count = sum(1 for phrase in cautious_phrases if phrase.lower() in text.lower())
        
        return {
            "confidence_indicators": confident_count,
            "cautious_indicators": cautious_count,
            "confidence_level": max(0, confident_count - cautious_count)
        }
    
    def _calculate_quality_score(self, metrics: Dict) -> float:
        """Calcula un score de calidad general basado en todas las métricas"""
        score = 0.0
        
        # Readability (25%)
        readability = metrics.get("readability", {})
        if readability.get("flesch_score", 0) > 60:
            score += 0.25
        
        # Conciseness (20%)
        conciseness = metrics.get("conciseness", {})
        if conciseness.get("content_word_ratio", 0) > 0.6:
            score += 0.20
        
        # Structure (20%)
        structure = metrics.get("structure", {})
        if structure.get("bullet_points", 0) > 0 or structure.get("logical_connectors", 0) > 0:
            score += 0.20
        
        # Vocabulary (15%)
        vocabulary = metrics.get("vocabulary", {})
        if vocabulary.get("lexical_diversity", 0) > 0.6:
            score += 0.15
        
        # Factual indicators (10%)
        factual = metrics.get("factual_indicators", {})
        if factual.get("factual_confidence", 0) > 0:
            score += 0.10
        
        # Confidence (10%)
        confidence = metrics.get("confidence_indicators", {})
        if confidence.get("confidence_level", 0) >= 0:
            score += 0.10
        
        return round(score, 3)
    
    def _count_syllables(self, text: str) -> int:
        """Cuenta sílabas aproximadas en el texto"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return count
    
    def _calculate_redundancy(self, text: str) -> float:
        """Calcula un score de redundancia"""
        sentences = sent_tokenize(text)
        if len(sentences) < 2:
            return 0.0
        
        # Comparar similitud entre oraciones
        similarities = []
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                similarity = self._sentence_similarity(sentences[i], sentences[j])
                similarities.append(similarity)
        
        return round(np.mean(similarities) if similarities else 0.0, 3)
    
    def _sentence_similarity(self, sent1: str, sent2: str) -> float:
        """Calcula similitud entre dos oraciones"""
        words1 = set(word_tokenize(sent1.lower()))
        words2 = set(word_tokenize(sent2.lower()))
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _has_introduction(self, text: str) -> bool:
        """Detecta si el texto tiene una introducción"""
        intro_indicators = [
            'introduction', 'overview', 'summary', 'in this', 'this article',
            'this response', 'let me', 'i will', 'we will'
        ]
        first_sentence = sent_tokenize(text)[0].lower() if sent_tokenize(text) else ""
        return any(indicator in first_sentence for indicator in intro_indicators)
    
    def _has_conclusion(self, text: str) -> bool:
        """Detecta si el texto tiene una conclusión"""
        conclusion_indicators = [
            'conclusion', 'summary', 'in conclusion', 'to summarize',
            'therefore', 'thus', 'finally', 'in summary'
        ]
        last_sentence = sent_tokenize(text)[-1].lower() if sent_tokenize(text) else ""
        return any(indicator in last_sentence for indicator in conclusion_indicators)
    
    def _calculate_vocabulary_richness(self, words: List[str]) -> float:
        """Calcula la riqueza del vocabulario"""
        if not words:
            return 0.0
        
        # Usar la fórmula de Yule's K
        word_freq = Counter(words)
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        sum_fi2 = sum(freq ** 2 for freq in word_freq.values())
        yules_k = 10000 * (sum_fi2 - total_words) / (total_words ** 2)
        
        # Normalizar (valores más bajos son mejores)
        return max(0, 1 - (yules_k / 100)) 