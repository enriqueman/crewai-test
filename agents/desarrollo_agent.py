from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings

class DesarrolloAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        
    def create_agent(self) -> Agent:
        """Crea el agente de Desarrollo"""
        return Agent(
            role=AgentSettings.DESARROLLO_AGENT["role"],
            goal=AgentSettings.DESARROLLO_AGENT["goal"],
            backstory=AgentSettings.DESARROLLO_AGENT["backstory"],
            verbose=AgentSettings.DESARROLLO_AGENT["verbose"],
            allow_delegation=AgentSettings.DESARROLLO_AGENT["allow_delegation"],
            llm=self.model_config.get_default_model()
        )
    
    def create_desarrollo_task(self, agent: Agent) -> Task:
        """Crea la tarea de Desarrollo del contenido principal"""
        return Task(
            description="""
            Desarrolla el contenido principal del artículo basándote en la investigación, 
            análisis y marco teórico establecidos. Crea secciones profundas y bien estructuradas.
            
            Tu desarrollo debe incluir:
            
            1. **INTRODUCCIÓN EXPANDIDA** (300-400 palabras):
               - Hook inicial que capture atención
               - Contexto de la industria actual
               - Problema/oportunidad identificada
               - Preview de lo que encontrará el lector
               - Transición fluida al contenido principal
            
            2. **SECCIONES PRINCIPALES** (5-7 secciones de 400-600 palabras c/u):
               
               **Sección A: Estado Actual del Content Marketing**
               - Landscape actual de la industria
               - Métricas y benchmarks importantes
               - Desafíos principales identificados
               
               **Sección B: Tendencias Disruptivas Emergentes**
               - Top 3-5 tendencias más impactantes
               - Análisis detallado de cada tendencia
               - Ejemplos reales y casos de uso
               
               **Sección C: Tecnologías y Herramientas Clave**
               - Tecnologías que están cambiando el juego
               - Herramientas recomendadas por categoría
               - ROI y adopción esperada
               
               **Sección D: Cambios en Comportamiento del Consumidor**
               - Nuevos patrones de consumo de contenido
               - Preferencias generacionales
               - Impacto en estrategias de marketing
               
               **Sección E: Estrategias de Implementación**
               - Frameworks prácticos para adopción
               - Best practices por tipo de empresa
               - Cronogramas de implementación
               
               **Sección F: Casos de Estudio y Ejemplos**
               - 3-4 casos de éxito detallados
               - Análisis de qué funcionó y por qué
               - Lecciones aplicables
            
            3. **CRITERIOS DE DESARROLLO**:
               - Cada sección debe tener estructura clara (intro, desarrollo, conclusión)
               - Incluir datos específicos y estadísticas
               - Usar ejemplos concretos y actionables
               - Mantener flow narrativo entre secciones
               - Optimizar para diferentes tipos de lectura (scanning y deep reading)
            """,
            expected_output="""
            Contenido principal completo y estructurado que incluya:
            
            **INTRODUCCIÓN EXPANDIDA**
            - 300-400 palabras engaging y contextualizadas
            - Hook, contexto, problema/oportunidad, preview
            
            **SECCIONES PRINCIPALES DESARROLLADAS**
            - 5-7 secciones de 400-600 palabras cada una
            - Cada sección con subtítulos descriptivos
            - Contenido profundo con análisis detallado
            - Estadísticas específicas y datos concretos
            - Ejemplos prácticos y casos reales
            - Transiciones fluidas entre secciones
            
            **ELEMENTOS INCLUIDOS POR SECCIÓN**:
            - Introducción al tema de la sección
            - Desarrollo con evidencia y ejemplos
            - Implicaciones prácticas
            - Conexión con la siguiente sección
            
            Total: 2,500-4,000 palabras de contenido principal
            Formato: Markdown con estructura clara
            SEO: Uso natural de keywords identificadas
            """,
            agent=agent
        )