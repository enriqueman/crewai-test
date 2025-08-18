from langchain.tools import BaseTool
from typing import Optional
import json
import re

class ContentAnalyzer(BaseTool):
    name = "content_analyzer"
    description = "Analyze content quality, relevance, and extract key insights"
    
    def _run(self, content: str) -> str:
        """
        Analiza el contenido y extrae insights clave
        """
        try:
            analysis = {
                "content_length": len(content),
                "word_count": len(content.split()),
                "key_topics": self._extract_key_topics(content),
                "sentiment": self._analyze_sentiment(content),
                "readability_score": self._calculate_readability(content),
                "key_insights": self._extract_insights(content),
                "recommendations": self._generate_recommendations(content)
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            return f"Error analyzing content: {str(e)}"
    
    def _extract_key_topics(self, content: str) -> list:
        """
        Extrae los temas principales del contenido
        """
        # Implementación básica - en producción usarías NLP más avanzado
        words = content.lower().split()
        # Filtrar palabras comunes y contar frecuencia
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        topic_words = [word for word in words if word not in common_words and len(word) > 3]
        return list(set(topic_words[:10]))  # Top 10 temas
    
    def _analyze_sentiment(self, content: str) -> str:
        """
        Análisis básico de sentimiento
        """
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'positive']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'negative', 'poor']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_readability(self, content: str) -> float:
        """
        Calcula un score básico de legibilidad
        """
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        
        if sentences > 0:
            return round(words / sentences, 2)
        return 0.0
    
    def _extract_insights(self, content: str) -> list:
        """
        Extrae insights clave del contenido
        """
        insights = []
        if len(content) > 100:
            insights.append("Content has substantial length")
        if content.count('.') > 5:
            insights.append("Well-structured with multiple sentences")
        if any(word in content.lower() for word in ['data', 'statistics', 'research']):
            insights.append("Contains data-driven information")
        
        return insights
    
    def _generate_recommendations(self, content: str) -> list:
        """
        Genera recomendaciones para mejorar el contenido
        """
        recommendations = []
        
        if len(content) < 200:
            recommendations.append("Consider adding more detail and examples")
        if content.count('!') > 3:
            recommendations.append("Reduce excessive exclamation marks for professional tone")
        if not any(char.isdigit() for char in content):
            recommendations.append("Consider adding specific numbers or statistics")
        
        return recommendations
    
    async def _arun(self, content: str) -> str:
        """
        Versión asíncrona del análisis
        """
        return self._run(content)
