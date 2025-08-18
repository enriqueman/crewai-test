import os
import requests
from typing import Dict, List, Any
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    """Input para la herramienta de búsqueda web"""
    query: str = Field(..., description="Consulta de búsqueda")
    num_results: int = Field(default=10, description="Número de resultados")

class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = """
    Herramienta para buscar información actualizada en internet.
    Úsala para encontrar las últimas tendencias, estadísticas y 
    artículos sobre content marketing.
    """
    args_schema: type[BaseModel] = WebSearchInput
    
    def __init__(self):
        super().__init__()
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        
    def _run(self, query: str, num_results: int = 10) -> str:
        """Ejecuta la búsqueda web"""
        if not self.serper_api_key:
            return "Error: SERPER_API_KEY no configurada"
            
        url = "https://google.serper.dev/search"
        
        payload = {
            "q": query,
            "num": num_results,
            "gl": "us",
            "hl": "en"
        }
        
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Procesar resultados orgánicos
            if 'organic' in data:
                for result in data['organic']:
                    results.append(f"""
                    Título: {result.get('title', 'N/A')}
                    URL: {result.get('link', 'N/A')}
                    Snippet: {result.get('snippet', 'N/A')}
                    """)
            
            # Procesar noticias si están disponibles
            if 'news' in data:
                for news in data['news'][:3]:  # Solo las primeras 3 noticias
                    results.append(f"""
                    [NOTICIA] Título: {news.get('title', 'N/A')}
                    URL: {news.get('link', 'N/A')}
                    Snippet: {news.get('snippet', 'N/A')}
                    Fecha: {news.get('date', 'N/A')}
                    """)
            
            return "\n".join(results) if results else "No se encontraron resultados"
            
        except Exception as e:
            return f"Error en la búsqueda: {str(e)}"

class ContentAnalyzerTool(BaseTool):
    name: str = "Content Analyzer Tool"
    description: str = """
    Analiza y extrae insights clave de contenido sobre marketing.
    Identifica tendencias, métricas importantes y puntos clave.
    """
    
    def _run(self, content: str) -> str:
        """Analiza el contenido y extrae insights"""
        # Palabras clave relacionadas con content marketing
        marketing_keywords = [
            'AI', 'artificial intelligence', 'automation', 'personalization',
            'video marketing', 'social media', 'SEO', 'content strategy',
            'engagement', 'conversion', 'ROI', 'analytics', 'influencer',
            'user-generated content', 'interactive content', 'storytelling'
        ]
        
        insights = []
        content_lower = content.lower()
        
        # Buscar palabras clave
        found_keywords = [kw for kw in marketing_keywords if kw.lower() in content_lower]
        
        if found_keywords:
            insights.append(f"Tendencias identificadas: {', '.join(found_keywords[:5])}")
        
        # Buscar números/estadísticas
        import re
        numbers = re.findall(r'\d+(?:\.\d+)?%|\$\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*', content)
        
        if numbers:
            insights.append(f"Estadísticas relevantes encontradas: {', '.join(numbers[:3])}")
        
        # Buscar años (para identificar estudios recientes)
        years = re.findall(r'20\d{2}', content)
        recent_years = [y for y in years if int(y) >= 2023]
        
        if recent_years:
            insights.append(f"Estudios/datos recientes de: {', '.join(set(recent_years))}")
        
        return "\n".join(insights) if insights else "No se encontraron insights específicos"