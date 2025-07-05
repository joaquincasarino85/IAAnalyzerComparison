from typing import Dict, List, Tuple, Any
from collections import defaultdict
import re
from difflib import SequenceMatcher

class IntelligentComparator:
    def __init__(self):
        self.comparison_metrics = {}
        
    def compare_responses(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Compara inteligentemente todas las respuestas de AI"""
        if len(responses) < 2:
            return {"error": "Se necesitan al menos 2 respuestas para comparar"}
            
        comparison_results = {
            "overall_analysis": self._overall_analysis(responses),
            "consensus_analysis": self._consensus_analysis(responses),
            "divergence_analysis": self._divergence_analysis(responses),
            "quality_ranking": self._quality_ranking(responses),
            "recommendations": self._generate_recommendations(responses),
            "detailed_comparisons": self._detailed_pairwise_comparisons(responses)
        }
        
        return comparison_results
    
    def _overall_analysis(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Análisis general de todas las respuestas"""
        # Estadísticas básicas
        response_lengths = {ai: len(response) for ai, response in responses.items()}
        avg_length = sum(response_lengths.values()) / len(response_lengths)
        
        # Detectar temas principales
        common_themes = self._extract_common_themes(responses)
        
        # Análisis de cobertura
        coverage_analysis = self._analyze_coverage(responses)
        
        return {
            "total_responses": len(responses),
            "average_length": round(avg_length, 2),
            "length_variance": self._calculate_variance(list(response_lengths.values())),
            "common_themes": common_themes,
            "coverage_analysis": coverage_analysis,
            "consistency_score": self._calculate_consistency_score(responses)
        }
    
    def _consensus_analysis(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Analiza el consenso entre las respuestas"""
        # Extraer puntos clave de cada respuesta
        key_points = {}
        for ai, response in responses.items():
            key_points[ai] = self._extract_key_points(response)
        
        # Encontrar puntos de consenso
        consensus_points = self._find_consensus_points(key_points)
        
        # Calcular nivel de acuerdo
        agreement_level = self._calculate_agreement_level(key_points)
        
        return {
            "consensus_points": consensus_points,
            "agreement_level": agreement_level,
            "consensus_score": len(consensus_points) / max(len(key_points.values()), 1),
            "key_points_by_ai": key_points
        }
    
    def _divergence_analysis(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Analiza las divergencias entre respuestas"""
        # Encontrar puntos únicos de cada AI
        unique_points = {}
        for ai, response in responses.items():
            unique_points[ai] = self._find_unique_points(response, responses)
        
        # Detectar contradicciones
        contradictions = self._detect_contradictions(responses)
        
        # Análisis de enfoques diferentes
        approach_analysis = self._analyze_different_approaches(responses)
        
        return {
            "unique_points": unique_points,
            "contradictions": contradictions,
            "different_approaches": approach_analysis,
            "divergence_score": self._calculate_divergence_score(unique_points, contradictions)
        }
    
    def _quality_ranking(self, responses: Dict[str, str]) -> List[Dict[str, Any]]:
        """Ranking de calidad de las respuestas"""
        rankings = []
        
        for ai, response in responses.items():
            quality_score = self._calculate_response_quality(response)
            rankings.append({
                "ai_name": ai,
                "quality_score": quality_score,
                "strengths": self._identify_strengths(response),
                "weaknesses": self._identify_weaknesses(response),
                "length": len(response),
                "readability": self._calculate_readability_score(response)
            })
        
        # Ordenar por score de calidad
        rankings.sort(key=lambda x: x["quality_score"], reverse=True)
        
        return rankings
    
    def _generate_recommendations(self, responses: Dict[str, str]) -> Dict[str, List[str]]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = {
            "best_overall": [],
            "most_concise": [],
            "most_detailed": [],
            "most_balanced": [],
            "improvement_suggestions": []
        }
        
        # Encontrar la mejor respuesta general
        quality_rankings = self._quality_ranking(responses)
        if quality_rankings:
            recommendations["best_overall"].append(quality_rankings[0]["ai_name"])
        
        # Encontrar la más concisa
        conciseness_rankings = sorted(
            [(ai, len(response)) for ai, response in responses.items()],
            key=lambda x: x[1]
        )
        if conciseness_rankings:
            recommendations["most_concise"].append(conciseness_rankings[0][0])
        
        # Encontrar la más detallada
        if conciseness_rankings:
            recommendations["most_detailed"].append(conciseness_rankings[-1][0])
        
        # Sugerencias de mejora
        recommendations["improvement_suggestions"] = self._generate_improvement_suggestions(responses)
        
        return recommendations
    
    def _detailed_pairwise_comparisons(self, responses: Dict[str, str]) -> Dict[str, Dict]:
        """Comparaciones detalladas entre pares de AI"""
        comparisons = {}
        ai_names = list(responses.keys())
        
        for i in range(len(ai_names)):
            for j in range(i + 1, len(ai_names)):
                ai1, ai2 = ai_names[i], ai_names[j]
                comparison_key = f"{ai1}_vs_{ai2}"
                
                comparisons[comparison_key] = {
                    "similarity_score": self._calculate_similarity(responses[ai1], responses[ai2]),
                    "length_comparison": {
                        ai1: len(responses[ai1]),
                        ai2: len(responses[ai2]),
                        "difference": abs(len(responses[ai1]) - len(responses[ai2]))
                    },
                    "common_elements": self._find_common_elements(responses[ai1], responses[ai2]),
                    "unique_elements": {
                        ai1: self._find_unique_elements(responses[ai1], responses[ai2]),
                        ai2: self._find_unique_elements(responses[ai2], responses[ai1])
                    },
                    "style_comparison": self._compare_styles(responses[ai1], responses[ai2])
                }
        
        return comparisons
    
    def _extract_common_themes(self, responses: Dict[str, str]) -> List[str]:
        """Extrae temas comunes entre las respuestas"""
        # Implementación simplificada - en producción usar NLP más avanzado
        all_words = []
        for response in responses.values():
            words = re.findall(r'\b\w+\b', response.lower())
            all_words.extend(words)
        
        # Encontrar palabras más frecuentes
        word_freq = defaultdict(int)
        for word in all_words:
            if len(word) > 3:  # Filtrar palabras cortas
                word_freq[word] += 1
        
        # Retornar las palabras más comunes
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return [word for word, freq in common_words if freq > 1]
    
    def _analyze_coverage(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Analiza la cobertura de temas en las respuestas"""
        # Implementación simplificada
        total_length = sum(len(response) for response in responses.values())
        avg_length = total_length / len(responses)
        
        return {
            "total_content_length": total_length,
            "average_response_length": round(avg_length, 2),
            "coverage_variance": self._calculate_variance([len(r) for r in responses.values()]),
            "completeness_estimate": min(1.0, total_length / 1000)  # Estimación simplificada
        }
    
    def _calculate_consistency_score(self, responses: Dict[str, str]) -> float:
        """Calcula un score de consistencia entre respuestas"""
        if len(responses) < 2:
            return 1.0
        
        # Calcular similitud promedio entre todas las respuestas
        similarities = []
        responses_list = list(responses.values())
        
        for i in range(len(responses_list)):
            for j in range(i + 1, len(responses_list)):
                similarity = self._calculate_similarity(responses_list[i], responses_list[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extrae puntos clave de un texto"""
        # Implementación simplificada
        sentences = re.split(r'[.!?]+', text)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in ['key', 'important', 'main', 'primary', 'essential']):
                key_points.append(sentence)
        
        return key_points[:5]  # Limitar a 5 puntos clave
    
    def _find_consensus_points(self, key_points: Dict[str, List[str]]) -> List[str]:
        """Encuentra puntos de consenso entre las respuestas"""
        # Implementación simplificada
        all_points = []
        for points in key_points.values():
            all_points.extend(points)
        
        # Encontrar puntos similares
        consensus = []
        for i, point1 in enumerate(all_points):
            for j, point2 in enumerate(all_points[i+1:], i+1):
                if self._calculate_similarity(point1, point2) > 0.7:
                    consensus.append(point1)
                    break
        
        return list(set(consensus))
    
    def _calculate_agreement_level(self, key_points: Dict[str, List[str]]) -> float:
        """Calcula el nivel de acuerdo entre las respuestas"""
        if len(key_points) < 2:
            return 1.0
        
        total_comparisons = 0
        agreement_count = 0
        
        points_list = list(key_points.values())
        for i in range(len(points_list)):
            for j in range(i + 1, len(points_list)):
                for point1 in points_list[i]:
                    for point2 in points_list[j]:
                        total_comparisons += 1
                        if self._calculate_similarity(point1, point2) > 0.6:
                            agreement_count += 1
        
        return agreement_count / total_comparisons if total_comparisons > 0 else 0.0
    
    def _find_unique_points(self, response: str, all_responses: Dict[str, str]) -> List[str]:
        """Encuentra puntos únicos en una respuesta"""
        # Implementación simplificada
        sentences = re.split(r'[.!?]+', response)
        unique_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            is_unique = True
            for other_response in all_responses.values():
                if other_response != response:
                    if self._calculate_similarity(sentence, other_response) > 0.5:
                        is_unique = False
                        break
            
            if is_unique:
                unique_points.append(sentence)
        
        return unique_points[:3]  # Limitar a 3 puntos únicos
    
    def _detect_contradictions(self, responses: Dict[str, str]) -> List[Dict[str, str]]:
        """Detecta contradicciones entre respuestas"""
        contradictions = []
        responses_list = list(responses.items())
        
        for i, (ai1, response1) in enumerate(responses_list):
            for j, (ai2, response2) in enumerate(responses_list[i+1:], i+1):
                # Implementación simplificada - buscar palabras opuestas
                contradiction = self._find_contradictions_between(response1, response2)
                if contradiction:
                    contradictions.append({
                        "ai1": ai1,
                        "ai2": ai2,
                        "contradiction": contradiction
                    })
        
        return contradictions
    
    def _find_contradictions_between(self, text1: str, text2: str) -> str:
        """Encuentra contradicciones específicas entre dos textos"""
        # Palabras opuestas comunes
        opposites = [
            ("increase", "decrease"), ("high", "low"), ("good", "bad"),
            ("positive", "negative"), ("yes", "no"), ("true", "false"),
            ("beneficial", "harmful"), ("effective", "ineffective")
        ]
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        for word1, word2 in opposites:
            if word1 in text1_lower and word2 in text2_lower:
                return f"'{word1}' vs '{word2}'"
            elif word2 in text1_lower and word1 in text2_lower:
                return f"'{word2}' vs '{word1}'"
        
        return ""
    
    def _analyze_different_approaches(self, responses: Dict[str, str]) -> Dict[str, List[str]]:
        """Analiza diferentes enfoques en las respuestas"""
        approaches = {
            "technical": [],
            "practical": [],
            "analytical": [],
            "creative": []
        }
        
        for ai, response in responses.items():
            response_lower = response.lower()
            
            # Clasificar enfoque
            if any(word in response_lower for word in ["algorithm", "technical", "implementation", "code"]):
                approaches["technical"].append(ai)
            elif any(word in response_lower for word in ["practical", "real-world", "example", "case"]):
                approaches["practical"].append(ai)
            elif any(word in response_lower for word in ["analysis", "data", "statistics", "research"]):
                approaches["analytical"].append(ai)
            elif any(word in response_lower for word in ["creative", "innovative", "unique", "novel"]):
                approaches["creative"].append(ai)
        
        return approaches
    
    def _calculate_response_quality(self, response: str) -> float:
        """Calcula un score de calidad para una respuesta"""
        score = 0.0
        
        # Longitud apropiada (0-25 puntos)
        length = len(response)
        if 100 <= length <= 500:
            score += 25
        elif 50 <= length <= 1000:
            score += 20
        elif length > 1000:
            score += 15
        else:
            score += 10
        
        # Estructura (0-25 puntos)
        if re.search(r'[•\-\*]', response):  # Bullet points
            score += 10
        if re.search(r'\d+\.', response):  # Numbered lists
            score += 10
        if len(re.split(r'[.!?]+', response)) > 3:  # Multiple sentences
            score += 5
        
        # Vocabulario (0-25 puntos)
        words = re.findall(r'\b\w+\b', response)
        unique_words = set(words)
        if len(words) > 0:
            diversity = len(unique_words) / len(words)
            score += diversity * 25
        
        # Legibilidad (0-25 puntos)
        sentences = re.split(r'[.!?]+', response)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 10 <= avg_sentence_length <= 25:
                score += 25
            elif 5 <= avg_sentence_length <= 30:
                score += 20
            else:
                score += 10
        
        return min(100, score)
    
    def _identify_strengths(self, response: str) -> List[str]:
        """Identifica fortalezas de una respuesta"""
        strengths = []
        
        if len(response) > 200:
            strengths.append("Respuesta detallada")
        if re.search(r'[•\-\*]', response):
            strengths.append("Bien estructurada")
        if len(re.findall(r'\b\w+\b', response)) > 50:
            strengths.append("Vocabulario rico")
        if re.search(r'\d+', response):
            strengths.append("Incluye datos específicos")
        
        return strengths
    
    def _identify_weaknesses(self, response: str) -> List[str]:
        """Identifica debilidades de una respuesta"""
        weaknesses = []
        
        if len(response) < 50:
            weaknesses.append("Respuesta muy corta")
        if len(re.split(r'[.!?]+', response)) < 2:
            weaknesses.append("Falta estructura")
        if not re.search(r'[•\-\*]', response) and len(response) > 100:
            weaknesses.append("Podría beneficiarse de listas")
        
        return weaknesses
    
    def _calculate_readability_score(self, response: str) -> float:
        """Calcula un score de legibilidad"""
        sentences = re.split(r'[.!?]+', response)
        words = re.findall(r'\b\w+\b', response)
        
        if not sentences or not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Score basado en longitud de oraciones
        if avg_sentence_length <= 15:
            return 100.0
        elif avg_sentence_length <= 20:
            return 80.0
        elif avg_sentence_length <= 25:
            return 60.0
        else:
            return 40.0
    
    def _generate_improvement_suggestions(self, responses: Dict[str, str]) -> List[str]:
        """Genera sugerencias de mejora"""
        suggestions = []
        
        # Analizar patrones comunes
        short_responses = [ai for ai, resp in responses.items() if len(resp) < 100]
        long_responses = [ai for ai, resp in responses.items() if len(resp) > 500]
        
        if short_responses:
            suggestions.append(f"Las respuestas de {', '.join(short_responses)} podrían ser más detalladas")
        
        if long_responses:
            suggestions.append(f"Las respuestas de {', '.join(long_responses)} podrían ser más concisas")
        
        # Verificar estructura
        unstructured = [ai for ai, resp in responses.items() if not re.search(r'[•\-\*]', resp)]
        if unstructured:
            suggestions.append(f"Las respuestas de {', '.join(unstructured)} podrían beneficiarse de mejor estructura")
        
        return suggestions
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud entre dos textos"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _find_common_elements(self, text1: str, text2: str) -> List[str]:
        """Encuentra elementos comunes entre dos textos"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        common = words1.intersection(words2)
        return list(common)[:10]  # Limitar a 10 elementos
    
    def _find_unique_elements(self, text1: str, text2: str) -> List[str]:
        """Encuentra elementos únicos en text1 comparado con text2"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        unique = words1 - words2
        return list(unique)[:5]  # Limitar a 5 elementos
    
    def _compare_styles(self, text1: str, text2: str) -> Dict[str, Any]:
        """Compara estilos de escritura entre dos textos"""
        return {
            "text1_length": len(text1),
            "text2_length": len(text2),
            "text1_sentences": len(re.split(r'[.!?]+', text1)),
            "text2_sentences": len(re.split(r'[.!?]+', text2)),
            "text1_has_bullets": bool(re.search(r'[•\-\*]', text1)),
            "text2_has_bullets": bool(re.search(r'[•\-\*]', text2))
        }
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calcula la varianza de una lista de valores"""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return round(variance, 2)
    
    def _calculate_divergence_score(self, unique_points: Dict[str, List[str]], contradictions: List[Dict]) -> float:
        """Calcula un score de divergencia"""
        total_unique = sum(len(points) for points in unique_points.values())
        contradiction_count = len(contradictions)
        
        # Score basado en puntos únicos y contradicciones
        divergence = (total_unique * 0.1) + (contradiction_count * 0.3)
        return min(1.0, divergence) 