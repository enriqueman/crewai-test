from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings
from tools.web_search_tool import WebSearchTool
from tools.content_analyzer import AdvancedContentAnalyzer, ContentQualityChecker

class ResearchAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.web_search_tool = WebSearchTool()
        self.content_analyzer = AdvancedContentAnalyzer()
        self.quality_checker = ContentQualityChecker()
        
    def create_agent(self) -> Agent:
        """Crea el agente de investigación con herramientas mejoradas"""
        return Agent(
            role=AgentSettings.RESEARCH_AGENT["role"],
            goal=AgentSettings.RESEARCH_AGENT["goal"],
            backstory=AgentSettings.RESEARCH_AGENT["backstory"],
            verbose=AgentSettings.RESEARCH_AGENT["verbose"],
            allow_delegation=AgentSettings.RESEARCH_AGENT["allow_delegation"],
            tools=[self.web_search_tool, self.content_analyzer, self.quality_checker],
            llm=self.model_config.get_default_model()
        )
    
    def create_research_task(self, agent: Agent) -> Task:
        """Crea la tarea de investigación mejorada"""
        return Task(
            description="""
            Realiza una investigación exhaustiva sobre las últimas tendencias en content marketing para 2024-2025.
            Utiliza todas las herramientas disponibles para obtener insights profundos y de alta calidad.
            
            Tu investigación debe incluir:
            
            1. **BÚSQUEDA Y RECOPILACIÓN** (usar WebSearchTool):
               - Tendencias emergentes en content marketing
               - Nuevas tecnologías y herramientas
               - Cambios en el comportamiento del consumidor
               - Estadísticas y datos recientes del sector
               - Casos de éxito y mejores prácticas
               - Predicciones y proyecciones futuras
            
            2. **ANÁLISIS DE CONTENIDO** (usar AdvancedContentAnalyzer):
               - Analizar el contenido encontrado para extraer insights clave
               - Identificar keywords y tendencias principales
               - Evaluar el sentimiento y calidad de las fuentes
               - Categorizar información por relevancia
            
            3. **CONTROL DE CALIDAD** (usar ContentQualityChecker):
               - Verificar la calidad de la información recopilada
               - Asegurar diversidad en tipos de fuentes
               - Validar credibilidad y autoridad de las fuentes
            
            Busca información de fuentes confiables como:
            - HubSpot, Content Marketing Institute
            - Informes de agencias reconocidas (McKinsey, Deloitte, Accenture)
            - Estudios académicos recientes
            - Plataformas líderes en marketing digital (Google, Meta, LinkedIn)
            - Publicaciones especializadas (Marketing Land, Search Engine Journal)
            
            **IMPORTANTE:** Usa las herramientas de análisis para procesar cada fuente importante
            y extraer los insights más relevantes. Asegúrate de que la información sea actual (2024-2025).
            """,
            expected_output="""
            Un informe de investigación completo y analizado que incluya:
            
            **RESUMEN EJECUTIVO DE LA INVESTIGACIÓN**
            - Overview de las 10-15 tendencias principales identificadas
            - Nivel de confianza y calidad de las fuentes por tendencia
            - Metodología de investigación utilizada
            
            **HALLAZGOS CATEGORIZADOS**
            - Tendencias tecnológicas (AI, automation, nuevas plataformas)
            - Cambios en comportamiento del consumidor
            - Evolución de formatos de contenido
            - Métricas y KPIs emergentes
            - Herramientas y tecnologías disruptivas
            
            **DATOS Y ESTADÍSTICAS CLAVE**
            - Mínimo 20 estadísticas específicas con fuentes
            - Tendencias cuantificables con datos de soporte
            - Proyecciones y forecasts de expertos
            
            **CASOS DE ESTUDIO IDENTIFICADOS**
            - 5-7 casos de éxito específicos con detalles
            - Análisis de qué funcionó y por qué
            - Empresas líderes por categoría de tendencia
            
            **ANÁLISIS DE CALIDAD DE FUENTES**
            - Evaluación de credibilidad por fuente utilizada
            - Categorización: primarias vs. secundarias
            - Notas sobre limitaciones o sesgos identificados
            
            **FUENTES Y REFERENCIAS DOCUMENTADAS**
            - Lista completa de todas las fuentes consultadas
            - URLs verificadas y fechas de acceso
            - Clasificación por tipo y relevancia
            
            Todo debe estar ready para análisis posterior y citación académica.
            """,
            agent=agent
        )