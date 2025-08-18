from langchain.tools import BaseTool
from typing import Optional
import json
import re

class ArticleFormatter(BaseTool):
    name = "article_formatter"
    description = "Format and structure articles for better readability and engagement"
    
    def _run(self, content: str) -> str:
        """
        Formatea el contenido del artículo para mejor legibilidad
        """
        try:
            formatted_content = {
                "original_length": len(content),
                "formatted_content": self._format_content(content),
                "seo_optimization": self._seo_optimize(content),
                "readability_improvements": self._improve_readability(content),
                "structure_analysis": self._analyze_structure(content)
            }
            
            return json.dumps(formatted_content, indent=2)
            
        except Exception as e:
            return f"Error formatting article: {str(e)}"
    
    def _format_content(self, content: str) -> str:
        """
        Aplica formato básico al contenido
        """
        # Dividir en párrafos
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                # Capitalizar primera letra
                paragraph = paragraph.strip()
                if paragraph and not paragraph[0].isupper():
                    paragraph = paragraph[0].upper() + paragraph[1:]
                
                # Asegurar que termine con punto
                if paragraph and not paragraph.endswith(('.', '!', '?')):
                    paragraph += '.'
                
                formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _seo_optimize(self, content: str) -> dict:
        """
        Optimización básica para SEO
        """
        seo_analysis = {
            "word_count": len(content.split()),
            "has_headlines": bool(re.search(r'^[A-Z][^.!?]*[.!?]?$', content, re.MULTILINE)),
            "keyword_density": self._calculate_keyword_density(content),
            "meta_description_length": len(content[:160]),
            "recommendations": []
        }
        
        # Recomendaciones SEO
        if seo_analysis["word_count"] < 300:
            seo_analysis["recommendations"].append("Consider increasing content length for better SEO")
        
        if not seo_analysis["has_headlines"]:
            seo_analysis["recommendations"].append("Add clear headlines and subheadings")
        
        if seo_analysis["meta_description_length"] < 120:
            seo_analysis["recommendations"].append("Meta description is too short")
        
        return seo_analysis
    
    def _calculate_keyword_density(self, content: str) -> dict:
        """
        Calcula la densidad de palabras clave
        """
        words = content.lower().split()
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Ignorar palabras muy cortas
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Top 5 palabras más frecuentes
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {word: {"count": count, "percentage": round((count/len(words))*100, 2)} 
                for word, count in top_words}
    
    def _improve_readability(self, content: str) -> dict:
        """
        Sugiere mejoras de legibilidad
        """
        improvements = {
            "sentence_length": self._analyze_sentence_length(content),
            "paragraph_breaks": self._suggest_paragraph_breaks(content),
            "transition_words": self._suggest_transitions(content)
        }
        
        return improvements
    
    def _analyze_sentence_length(self, content: str) -> dict:
        """
        Analiza la longitud de las oraciones
        """
        sentences = re.split(r'[.!?]+', content)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if sentence_lengths:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            long_sentences = [s for s in sentence_lengths if s > 25]
            
            return {
                "average_length": round(avg_length, 2),
                "long_sentences_count": len(long_sentences),
                "recommendation": "Break down long sentences for better readability" if long_sentences else "Sentence length is good"
            }
        
        return {"average_length": 0, "long_sentences_count": 0, "recommendation": "No sentences found"}
    
    def _suggest_paragraph_breaks(self, content: str) -> list:
        """
        Sugiere dónde hacer saltos de párrafo
        """
        suggestions = []
        paragraphs = content.split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.split()) > 100:
                suggestions.append(f"Paragraph {i+1} is long - consider breaking it up")
        
        return suggestions
    
    def _suggest_transitions(self, content: str) -> list:
        """
        Sugiere palabras de transición
        """
        transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently', 'in addition']
        suggestions = []
        
        content_lower = content.lower()
        for word in transition_words:
            if word not in content_lower:
                suggestions.append(f"Consider using '{word}' for better flow")
        
        return suggestions[:3]  # Máximo 3 sugerencias
    
    def _analyze_structure(self, content: str) -> dict:
        """
        Analiza la estructura del artículo
        """
        structure = {
            "has_introduction": bool(re.search(r'introduction|overview|summary', content.lower())),
            "has_conclusion": bool(re.search(r'conclusion|summary|final', content.lower())),
            "section_count": len(re.findall(r'[A-Z][^.!?]*:', content)),
            "recommendations": []
        }
        
        if not structure["has_introduction"]:
            structure["recommendations"].append("Add a clear introduction")
        
        if not structure["has_conclusion"]:
            structure["recommendations"].append("Include a conclusion or summary")
        
        if structure["section_count"] < 2:
            structure["recommendations"].append("Consider adding more sections for better organization")
        
        return structure
    
    async def _arun(self, content: str) -> str:
        """
        Versión asíncrona del formateo
        """
        return self._run(content)
