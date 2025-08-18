import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

class ModelConfig:
    """Configuración de modelos de IA"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.serper_api_key = os.getenv('SERPER_API_KEY')  # Para búsquedas web
        
    def get_openai_model(self, model_name: str = "gpt-4-turbo-preview") -> ChatOpenAI:
        """Obtiene modelo de OpenAI"""
        return ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=self.openai_api_key
        )
    
    def get_local_model(self, model_name: str = "llama3.1:8b") -> Ollama:
        """Obtiene modelo local (si está disponible)"""
        return Ollama(
            model=model_name,
            temperature=0.7
        )
    
    def get_default_model(self):
        """Obtiene el modelo por defecto basado en disponibilidad"""
        if self.openai_api_key:
            return self.get_openai_model()
        else:
            return self.get_local_model()

class AgentSettings:
    """Configuración específica para cada agente"""
    
    # Agentes originales
    RESEARCH_AGENT = {
        "role": "Senior Content Marketing Researcher",
        "goal": "Investigar y recopilar las últimas tendencias en content marketing",
        "backstory": """Eres un investigador experto en marketing digital con 10+ años 
        de experiencia. Tu especialidad es identificar tendencias emergentes y 
        analizar datos de mercado para proporcionar insights valiosos.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    ANALYST_AGENT = {
        "role": "Content Marketing Strategy Analyst",
        "goal": "Analizar y sintetizar información de tendencias para crear insights accionables",
        "backstory": """Eres un analista estratégico especializado en content marketing.
        Tu expertise está en tomar datos complejos y convertirlos en estrategias 
        claras y accionables para empresas.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    WRITER_AGENT = {
        "role": "Expert Content Marketing Writer",
        "goal": "Crear artículos de alta calidad sobre content marketing",
        "backstory": """Eres un escritor profesional especializado en marketing digital.
        Tu habilidad está en crear contenido engaging, bien estructurado y 
        altamente informativo que resuene con audiencias profesionales.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    # Nuevos agentes especializados
    ABSTRACT_KEYWORDS_AGENT = {
        "role": "Academic Abstract and Keywords Specialist",
        "goal": "Crear resúmenes ejecutivos profesionales, extraer palabras clave y establecer marcos teóricos",
        "backstory": """Eres un especialista en escritura académica y profesional con expertise 
        en crear abstracts convincentes y identificar keywords estratégicas. Tu especialidad es 
        sintetizar información compleja en resúmenes claros y establecer marcos teóricos sólidos.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    DESARROLLO_AGENT = {
        "role": "Content Development Specialist",
        "goal": "Desarrollar el contenido principal del artículo con análisis profundo y estructura lógica",
        "backstory": """Eres un experto en desarrollo de contenido especializado en crear 
        secciones principales de artículos. Tu fortaleza está en organizar información compleja 
        en narrativas coherentes y desarrollar análisis profundos con ejemplos prácticos.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    RESULTADOS_AGENT = {
        "role": "Data Analysis and Findings Specialist",
        "goal": "Analizar datos, presentar hallazgos y crear visualizaciones conceptuales",
        "backstory": """Eres un analista de datos especializado en interpretar información 
        de marketing y presentar hallazgos de manera clara. Tu expertise está en extraer 
        insights significativos y presentar resultados de forma comprensible.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    DISCUSION_AGENT = {
        "role": "Strategic Discussion and Future Research Specialist",
        "goal": "Interpretar implicaciones estratégicas e identificar áreas de investigación futura",
        "backstory": """Eres un pensador estratégico especializado en interpretar resultados 
        y sus implicaciones para el futuro del marketing. Tu habilidad está en conectar 
        hallazgos actuales con tendencias futuras y oportunidades de investigación.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    CONCLUSIONES_AGENT = {
        "role": "Strategic Conclusions Synthesizer",
        "goal": "Sintetizar todos los elementos en conclusiones estratégicas y accionables",
        "backstory": """Eres un sintetizador experto especializado en crear conclusiones 
        poderosas que integren todos los elementos del artículo. Tu fortaleza está en 
        destiliar insights complejos en takeaways claros y accionables.""",
        "verbose": True,
        "allow_delegation": False
    }
    
    BIBLIOGRAFIA_AGENT = {
        "role": "Academic References and Citation Specialist",
        "goal": "Formatear referencias académicas y crear bibliografías profesionales",
        "backstory": """Eres un especialista en documentación académica y profesional. 
        Tu expertise está en crear bibliografías impecables, formatear citas correctamente 
        y asegurar la credibilidad académica del contenido.""",
        "verbose": True,
        "allow_delegation": False
    }

# Configuraciones adicionales para el sistema académico
class AcademicConfig:
    """Configuración específica para el sistema académico"""
    
    # Configuración de timeouts y límites
    TIMEOUTS = {
        "research_timeout": 300,  # 5 minutos
        "analysis_timeout": 240,  # 4 minutos
        "writing_timeout": 600,   # 10 minutos por agente de escritura
        "total_timeout": 1800     # 30 minutos total
    }
    
    # Configuración de calidad
    QUALITY_METRICS = {
        "min_word_count_per_section": 200,
        "max_word_count_per_section": 800,
        "min_references": 25,
        "min_keywords": 8,
        "min_sections": 5
    }
    
    # Configuración de formato
    FORMAT_SETTINGS = {
        "citation_style": "business_academic",
        "reference_format": "apa_modified",
        "markdown_headers": True,
        "include_toc": True,
        "include_abstract": True
    }