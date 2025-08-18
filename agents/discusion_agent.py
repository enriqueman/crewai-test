from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings

class DiscusionAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        
    def create_agent(self) -> Agent:
        """Crea el agente de Discusión"""
        return Agent(
            role=AgentSettings.DISCUSION_AGENT["role"],
            goal=AgentSettings.DISCUSION_AGENT["goal"],
            backstory=AgentSettings.DISCUSION_AGENT["backstory"],
            verbose=AgentSettings.DISCUSION_AGENT["verbose"],
            allow_delegation=AgentSettings.DISCUSION_AGENT["allow_delegation"],
            llm=self.model_config.get_default_model()
        )
    
    def create_discusion_task(self, agent: Agent) -> Task:
        """Crea la tarea de Discusión y Trabajos Futuros"""
        return Task(
            description="""
            Interpreta los hallazgos encontrados, analiza sus implicaciones estratégicas 
            e identifica áreas críticas para investigación futura. Proporciona una perspectiva 
            estratégica y visionaria.
            
            Tu análisis debe incluir:
            
            1. **INTERPRETACIÓN DE HALLAZGOS** (500-600 palabras):
               
               **Significado Estratégico**
               - Qué significan realmente los hallazgos para la industria
               - Cómo cambian las reglas del juego actuales
               - Impacto en diferentes tipos de empresas (startup, PYME, enterprise)
               - Redefinición de best practices tradicionales
               
               **Contexto Competitivo**
               - Ventajas competitivas que emergen
               - Amenazas para modelos de negocio existentes
               - Oportunidades de diferenciación
               - Nuevos players vs. incumbentes
               
               **Implicaciones Económicas**
               - Impacto en costos operativos
               - Nuevas fuentes de revenue
               - ROI esperado de adopción temprana
               - Riesgos de no adaptarse
            
            2. **IMPLICACIONES PRÁCTICAS** (600-700 palabras):
               
               **Para CMOs y Marketing Leaders**
               - Cambios necesarios en estrategia organizacional
               - Nuevas competencias requeridas en el equipo
               - Inversiones prioritarias en tecnología
               - KPIs que necesitan redefinirse
               
               **Para Equipos de Contenido**
               - Evolución necesaria en processes creativos
               - Nuevas herramientas a adoptar
               - Skills gaps a cerrar
               - Workflows a rediseñar
               
               **Para Organizaciones**
               - Impacto en estructura organizacional
               - Necesidades de training y upskilling
               - Cambios en budget allocation
               - Timeline de transformación sugerido
               
               **Para la Industria en General**
               - Consolidación vs. fragmentación esperada
               - Estándares emergentes a adoptar
               - Regulaciones potenciales a considerar
               - Ecosystem partnerships necesarios
            
            3. **IDENTIFICACIÓN DE RIESGOS Y OPORTUNIDADES** (400-500 palabras):
               
               **Riesgos Principales**
               - Riesgos de adopción temprana vs. tardía
               - Amenazas tecnológicas disruptivas
               - Cambios regulatorios potenciales
               - Volatilidad del consumer behavior
               
               **Oportunidades Emergentes**
               - Nichos de mercado sin explotar
               - Aplicaciones innovadoras de tecnologías
               - Partnerships estratégicos potenciales
               - Monetización de nuevos formatos
            
            4. **INVESTIGACIÓN FUTURA NECESARIA** (500-600 palabras):
               
               **Áreas de Investigación Prioritarias**
               - Gaps de conocimiento identificados
               - Preguntas sin respuesta que surgen
               - Metodologías de investigación recomendadas
               - Timeline sugerido para cada área
               
               **Estudios Longitudinales Recomendados**
               - Métricas a trackear en el tiempo
               - Cohortes a seguir
               - Frecuencia de medición sugerida
               
               **Investigación Experimental Sugerida**
               - Hipótesis a testear
               - Experimentos recomendados
               - Variables a controlar
               - Métricas de éxito a definir
               
               **Colaboraciones Académicas**
               - Partnerships universidad-industria sugeridos
               - Temas para tesis y papers académicos
               - Conferencias y journals relevantes
            """,
            expected_output="""
            Sección completa de Discusión y Trabajos Futuros que incluya:
            
            **INTERPRETACIÓN ESTRATÉGICA DE HALLAZGOS**
            - Significado profundo de los resultados
            - Contexto competitivo y económico
            - Implicaciones para diferentes stakeholders
            - Redefinición de paradigmas actuales
            
            **IMPLICACIONES PRÁCTICAS DETALLADAS**
            - Recomendaciones específicas por rol (CMO, Content Teams, etc.)
            - Cambios organizacionales necesarios
            - Inversiones y recursos requeridos
            - Timeline de implementación sugerido
            
            **ANÁLISIS DE RIESGOS Y OPORTUNIDADES**
            - Matriz de riesgos identificados
            - Oportunidades emergentes categorizadas
            - Estrategias de mitigación y aprovechamiento
            - Factores críticos de éxito
            
            **AGENDA DE INVESTIGACIÓN FUTURA**
            - 5-7 áreas prioritarias de investigación
            - Metodologías recomendadas para cada área
            - Preguntas específicas a investigar
            - Timeline y resources necesarios
            - Potenciales colaboradores y partners
            
            **CALL TO ACTION PARA LA INDUSTRIA**
            - Acciones inmediatas recomendadas
            - Iniciativas colaborativas sugeridas
            - Métricas a establecer industrywide
            - Próximos pasos concretos
            
            Total: 2,000-2,400 palabras
            Tono: Estratégico, visionario, pero pragmático
            Enfoque: Future-oriented con actionable insights
            """,
            agent=agent
        )