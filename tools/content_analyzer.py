import re
import json
from typing import Dict, List, Any, Optional
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from collections import Counter
import nltk

# Descargar recursos de NLTK si no están disponibles
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    pass  # En Lambda no podemos descargar, usaremos regex

class ContentAnalysisInput(BaseModel):
    """Input para la herramienta de análisis de contenido"""
    content: str = Field(..., description="Contenido a analizar")
    analysis_type: str = Field(default="comprehensive", description="Tipo de análisis: comprehensive, keywords, readability, structure")

class ContentAnalyzerTool(BaseTool):
    name: str = "Content Analyzer Tool"
    description: str = """
    Herramienta avanzada para analizar contenido de marketing. Puede identificar:
    - Keywords y temas principales
    - Métricas de legibilidad
    - Estructura del contenido
    - Sentiment y tone
    - Gaps de contenido
    - Optimización SEO
    """
    args_schema: type[BaseModel] = ContentAnalysisInput
    
    def _run(self, content: str, analysis_type: str = "comprehensive") -> str:
        """Ejecuta el análisis de contenido"""
        try:
            if analysis_type == "keywords":
                return self._analyze_keywords(content)
            elif analysis_type == "readability":
                return self._analyze_readability(content)
            elif analysis_type == "structure":
                return self._analyze_structure(content)
            elif analysis_type == "seo":
                return self._analyze_seo(content)
            else:
                return self._comprehensive_analysis(content)
                
        except Exception as e:
            return f"Error en análisis de contenido: {str(e)}"
    
    def _comprehensive_analysis(self, content: str) -> str:
        """Análisis completo del contenido"""
        results = {
            "content_metrics": self._get_content_metrics(content),
            "keyword_analysis": self._extract_keywords(content),
            "structure_analysis": self._analyze_content_structure(content),
            "readability": self._calculate_readability(content),
            "seo_metrics": self._analyze_seo_factors(content),
            "content_gaps": self._identify_content_gaps(content),
            "recommendations": self._generate_recommendations(content)
        }
        
        return self._format_analysis_results(results)
    
    def _get_content_metrics(self, content: str) -> Dict[str, Any]:
        """Obtiene métricas básicas del contenido"""
        words = len(content.split())
        sentences = len(re.split(r'[.!?]+', content))
        paragraphs = len([p for p in content.split('\n\n') if p.strip()])
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "paragraph_count": paragraphs,
            "average_words_per_sentence": round(words / max(sentences, 1), 2),
            "average_sentences_per_paragraph": round(sentences / max(paragraphs, 1), 2),
            "character_count": len(content),
            "character_count_no_spaces": len(content.replace(" ", ""))
        }
    
    def _extract_keywords(self, content: str) -> Dict[str, Any]:
        """Extrae y analiza keywords del contenido"""
        # Limpiar contenido
        clean_content = re.sub(r'[^\w\s]', '', content.lower())
        words = clean_content.split()
        
        # Filtrar stop words básicas
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'pero', 'sus', 'han', 'muy', 'está', 'son', 'todo', 'esta', 'más', 'tiene', 'si', 'ya', 'puede', 'bien', 'hacer', 'sobre', 'ser', 'era', 'vez', 'solo', 'desde', 'cada', 'hasta', 'también', 'otros', 'donde', 'cuando', 'mismo', 'tanto', 'algo', 'qué', 'porque', 'así', 'cómo', 'tanto',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'we', 'us', 'our', 'you', 'your', 'i', 'me', 'my', 'he', 'him', 'his', 'she', 'her', 'hers'
        }
        
        # Filtrar palabras relevantes
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Contar frecuencias
        word_freq = Counter(filtered_words)
        
        # Keywords relacionados con marketing
        marketing_keywords = [
            'content', 'marketing', 'digital', 'social', 'media', 'seo', 'strategy', 'brand', 'engagement', 'analytics', 'roi', 'conversion', 'automation', 'personalization', 'ai', 'artificial', 'intelligence', 'video', 'blog', 'email', 'influencer', 'campaign', 'audience', 'target', 'customer', 'user', 'experience', 'data', 'insights', 'trends', 'innovation', 'growth', 'optimization', 'performance', 'metrics', 'kpi'
        ]
        
        # Identificar keywords de marketing en el contenido
        found_marketing_keywords = {kw: word_freq.get(kw, 0) for kw in marketing_keywords if kw in word_freq}
        
        return {
            "total_unique_words": len(set(words)),
            "top_keywords": dict(word_freq.most_common(20)),
            "marketing_keywords_found": found_marketing_keywords,
            "keyword_density": round(len(filtered_words) / len(words) * 100, 2) if words else 0
        }
    
    def _analyze_content_structure(self, content: str) -> Dict[str, Any]:
        """Analiza la estructura del contenido"""
        # Detectar headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # Detectar listas
        bullet_points = len(re.findall(r'^\s*[-*•]\s+', content, re.MULTILINE))
        numbered_lists = len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
        
        # Detectar enlaces y referencias
        links = len(re.findall(r'https?://\S+', content))
        email_addresses = len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content))
        
        # Detectar formatting
        bold_text = len(re.findall(r'\*\*(.+?)\*\*', content))
        italic_text = len(re.findall(r'\*(.+?)\*', content))
        
        return {
            "headers_count": len(headers),
            "headers": headers[:10],  # Solo los primeros 10
            "bullet_points": bullet_points,
            "numbered_lists": numbered_lists,
            "links_count": links,
            "email_addresses": email_addresses,
            "bold_formatting": bold_text,
            "italic_formatting": italic_text,
            "has_good_structure": len(headers) >= 3 and (bullet_points > 0 or numbered_lists > 0)
        }
    
    def _calculate_readability(self, content: str) -> Dict[str, Any]:
        """Calcula métricas de legibilidad"""
        sentences = re.split(r'[.!?]+', content)
        words = content.split()
        
        if not sentences or not words:
            return {"error": "Contenido insuficiente para análisis"}
        
        # Flesch Reading Ease (aproximado)
        avg_sentence_length = len(words) / len(sentences)
        
        # Contar sílabas aproximadamente
        syllables = sum([self._count_syllables(word) for word in words])
        avg_syllables_per_word = syllables / len(words) if words else 0
        
        # Flesch Reading Ease Score (aproximado)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Interpretar score
        if flesch_score >= 90:
            reading_level = "Muy fácil"
        elif flesch_score >= 80:
            reading_level = "Fácil"
        elif flesch_score >= 70:
            reading_level = "Bastante fácil"
        elif flesch_score >= 60:
            reading_level = "Estándar"
        elif flesch_score >= 50:
            reading_level = "Bastante difícil"
        elif flesch_score >= 30:
            reading_level = "Difícil"
        else:
            reading_level = "Muy difícil"
        
        return {
            "flesch_score": round(flesch_score, 2),
            "reading_level": reading_level,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
            "estimated_reading_time_minutes": round(len(words) / 200, 1)  # 200 WPM promedio
        }
    
    def _count_syllables(self, word: str) -> int:
        """Cuenta sílabas aproximadamente"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not previous_was_vowel:
                    syllable_count += 1
                previous_was_vowel = True
            else:
                previous_was_vowel = False
        
        # Ajustes
        if word.endswith("e"):
            syllable_count -= 1
        if syllable_count == 0:
            syllable_count = 1
            
        return syllable_count
    
    def _analyze_seo_factors(self, content: str) -> Dict[str, Any]:
        """Analiza factores SEO del contenido"""
        word_count = len(content.split())
        
        # Detectar keywords en títulos
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # Meta información
        has_intro = len(content.split('\n\n')[0].split()) > 50 if content else False
        has_conclusion = "conclusión" in content.lower() or "resumen" in content.lower()
        
        # Densidad de keywords (aproximada)
        marketing_terms = ['marketing', 'content', 'digital', 'strategy', 'seo']
        keyword_mentions = sum([content.lower().count(term) for term in marketing_terms])
        keyword_density = (keyword_mentions / word_count * 100) if word_count > 0 else 0
        
        return {
            "word_count": word_count,
            "optimal_length": 1500 <= word_count <= 3000,
            "headers_count": len(headers),
            "has_intro": has_intro,
            "has_conclusion": has_conclusion,
            "keyword_density": round(keyword_density, 2),
            "seo_score": self._calculate_seo_score(word_count, len(headers), has_intro, has_conclusion, keyword_density)
        }
    
    def _calculate_seo_score(self, word_count: int, headers: int, has_intro: bool, has_conclusion: bool, keyword_density: float) -> int:
        """Calcula un score SEO básico"""
        score = 0
        
        # Longitud del contenido
        if 1500 <= word_count <= 3000:
            score += 25
        elif word_count >= 1000:
            score += 15
        
        # Estructura
        if headers >= 3:
            score += 20
        elif headers >= 1:
            score += 10
        
        # Introducción y conclusión
        if has_intro:
            score += 15
        if has_conclusion:
            score += 15
        
        # Densidad de keywords
        if 1 <= keyword_density <= 3:
            score += 25
        elif keyword_density > 0:
            score += 10
        
        return min(score, 100)
    
    def _identify_content_gaps(self, content: str) -> List[str]:
        """Identifica gaps en el contenido"""
        gaps = []
        
        # Verificar elementos comunes
        if "ejemplo" not in content.lower() and "case study" not in content.lower():
            gaps.append("Falta ejemplos o casos de estudio")
        
        if "estadística" not in content.lower() and "%" not in content and "datos" not in content.lower():
            gaps.append("Falta datos estadísticos o métricas")
        
        if len(re.findall(r'https?://\S+', content)) == 0:
            gaps.append("Falta enlaces externos o referencias")
        
        if "futuro" not in content.lower() and "tendencia" not in content.lower():
            gaps.append("Falta perspectiva futura o tendencias")
        
        if "recomendación" not in content.lower() and "acción" not in content.lower():
            gaps.append("Falta recomendaciones accionables")
        
        return gaps
    
    def _generate_recommendations(self, content: str) -> List[str]:
        """Genera recomendaciones para mejorar el contenido"""
        recommendations = []
        
        word_count = len(content.split())
        headers = len(re.findall(r'^#+\s+(.+)$', content, re.MULTILINE))
        
        if word_count < 1000:
            recommendations.append("Expandir el contenido: mínimo 1000 palabras para SEO")
        
        if headers < 3:
            recommendations.append("Agregar más subtítulos para mejorar estructura")
        
        if len(re.findall(r'\*\*(.+?)\*\*', content)) == 0:
            recommendations.append("Usar texto en negrita para destacar puntos clave")
        
        if len(re.findall(r'^\s*[-*•]\s+', content, re.MULTILINE)) == 0:
            recommendations.append("Agregar listas con viñetas para mejor lectura")
        
        gaps = self._identify_content_gaps(content)
        if gaps:
            recommendations.extend([f"Mejorar: {gap}" for gap in gaps[:3]])
        
        return recommendations
    
    def _format_analysis_results(self, results: Dict[str, Any]) -> str:
        """Formatea los resultados del análisis"""
        output = ["=== ANÁLISIS COMPLETO DE CONTENIDO ===\n"]
        
        # Métricas básicas
        metrics = results["content_metrics"]
        output.append(f"📊 MÉTRICAS BÁSICAS:")
        output.append(f"   • Palabras: {metrics['word_count']}")
        output.append(f"   • Oraciones: {metrics['sentence_count']}")
        output.append(f"   • Párrafos: {metrics['paragraph_count']}")
        output.append(f"   • Promedio palabras/oración: {metrics['average_words_per_sentence']}")
        
        # Keywords
        keywords = results["keyword_analysis"]
        output.append(f"\n🔍 ANÁLISIS DE KEYWORDS:")
        output.append(f"   • Palabras únicas: {keywords['total_unique_words']}")
        output.append(f"   • Densidad de keywords: {keywords['keyword_density']}%")
        if keywords['marketing_keywords_found']:
            output.append("   • Keywords de marketing encontradas:")
            for kw, count in list(keywords['marketing_keywords_found'].items())[:5]:
                output.append(f"     - {kw}: {count} veces")
        
        # Estructura
        structure = results["structure_analysis"]
        output.append(f"\n🏗️ ESTRUCTURA:")
        output.append(f"   • Headers: {structure['headers_count']}")
        output.append(f"   • Listas con viñetas: {structure['bullet_points']}")
        output.append(f"   • Enlaces: {structure['links_count']}")
        output.append(f"   • Buena estructura: {'✅' if structure['has_good_structure'] else '❌'}")
        
        # Legibilidad
        readability = results["readability"]
        if "error" not in readability:
            output.append(f"\n📖 LEGIBILIDAD:")
            output.append(f"   • Score Flesch: {readability['flesch_score']}")
            output.append(f"   • Nivel: {readability['reading_level']}")
            output.append(f"   • Tiempo estimado lectura: {readability['estimated_reading_time_minutes']} min")
        
        # SEO
        seo = results["seo_metrics"]
        output.append(f"\n🎯 MÉTRICAS SEO:")
        output.append(f"   • Longitud óptima: {'✅' if seo['optimal_length'] else '❌'}")
        output.append(f"   • Score SEO: {seo['seo_score']}/100")
        output.append(f"   • Densidad keywords: {seo['keyword_density']}%")
        
        # Gaps y recomendaciones
        gaps = results["content_gaps"]
        if gaps:
            output.append(f"\n⚠️ GAPS IDENTIFICADOS:")
            for gap in gaps:
                output.append(f"   • {gap}")
        
        recommendations = results["recommendations"]
        if recommendations:
            output.append(f"\n💡 RECOMENDACIONES:")
            for rec in recommendations:
                output.append(f"   • {rec}")
        
        return "\n".join(output)
    
    def _analyze_keywords(self, content: str) -> str:
        """Análisis específico de keywords"""
        keywords = self._extract_keywords(content)
        return json.dumps(keywords, indent=2)
    
    def _analyze_readability(self, content: str) -> str:
        """Análisis específico de legibilidad"""
        readability = self._calculate_readability(content)
        return json.dumps(readability, indent=2)
    
    def _analyze_structure(self, content: str) -> str:
        """Análisis específico de estructura"""
        structure = self._analyze_content_structure(content)
        return json.dumps(structure, indent=2)
    
    def _analyze_seo(self, content: str) -> str:
        """Análisis específico de SEO"""
        seo = self._analyze_seo_factors(content)
        return json.dumps(seo, indent=2)