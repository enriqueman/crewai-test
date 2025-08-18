from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings

class ResultadosAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        
    def create_agent(self) -> Agent:
        """Crea el agente de Resultados"""
        return Agent(
            role=AgentSettings.RESULTADOS_AGENT["role"],
            goal=AgentSettings.RESULTADOS_AGENT["goal"],
            backstory=AgentSettings.RESULTADOS_AGENT["backstory"],
            verbose=AgentSettings.RESULTADOS_AGENT["verbose"],
            allow_delegation=AgentSettings.RESULTADOS_AGENT["allow_delegation"],
            llm=self.model_config.get_default_model()
        )
    
    def create_resultados_task(self, agent: Agent) -> Task:
        """Crea la tarea de Análisis de Resultados"""
        return Task(
            description="""
            Analiza todos los datos recopilados y presenta los hallazgos clave de manera 
            estructurada y comprensible. Enfócate en extraer insights accionables.
            
            Tu análisis debe incluir:
            
            1. **ANÁLISIS CUANTITATIVO** (400-500 palabras):
               - Métricas clave identificadas en la investigación
               - Tendencias numéricas y estadísticas relevantes
               - Comparaciones year-over-year o period-over-period
               - Benchmarks de la industria vs. performance actual
               - Proyecciones basadas en datos históricos
               
            2. **HALLAZGOS PRINCIPALES** (500-600 palabras):
               
               **Hallazgo 1: [Tendencia más significativa]**
               - Descripción del hallazgo
               - Datos que lo sustentan
               - Nivel de adopción actual
               - Impacto medible en ROI/KPIs
               
               **Hallazgo 2: [Cambio de comportamiento clave]**
               - Análisis del cambio observado
               - Demografía más afectada
               - Implicaciones para estrategias
               
               **Hallazgo 3: [Oportunidad tecnológica]**
               - Descripción de la oportunidad
               - Barreras de entrada identificadas
               - Potencial de crecimiento
               
               **Hallazgo 4: [Gap en el mercado]**
               - Área de oportunidad identificada
               - Competencia actual
               - Estrategias de captura sugeridas
               
               **Hallazgo 5: [Predicción emergente]**
               - Tendencia en formación
               - Indicadores tempranos
               - Timeline de materialización
            
            3. **ANÁLISIS CUALITATIVO** (300-400 palabras):
               - Patrones emergentes no cuantificables
               - Insights sobre preferencias del consumidor
               - Cambios en percepción de marca
               - Factores culturales y sociales influyentes
               - Sentimiento general de la industria
            
            4. **CORRELACIONES Y CAUSAS** (300-350 palabras):
               - Relaciones causa-efecto identificadas
               - Factores que impulsan las tendencias
               - Variables externas que influyen
               - Interdependencias entre diferentes tendencias
            
            5. **VALIDACIÓN DE HIPÓTESIS** (200-250 palabras):
               - Hipótesis iniciales vs. hallazgos reales
               - Confirmaciones y refutaciones
               - Sorpresas y descubrimientos inesperados
               - Grado de confianza en los resultados
            """,
            expected_output="""
            Sección completa de Resultados y Hallazgos que incluya:
            
            **RESUMEN EJECUTIVO DE HALLAZGOS**
            - 3-5 hallazgos principales en bullet points
            - Nivel de confianza y significancia de cada uno
            
            **ANÁLISIS CUANTITATIVO DETALLADO**
            - Métricas clave con datos específicos
            - Gráficos conceptuales descritos en texto
            - Tendencias numéricas y proyecciones
            - Comparativas con benchmarks industry
            
            **HALLAZGOS PRINCIPALES EXPANDIDOS**
            - 5 hallazgos desarrollados individualmente
            - Cada uno con 100-120 palabras de análisis
            - Datos de soporte y evidencia
            - Implicaciones inmediatas identificadas
            
            **ANÁLISIS CUALITATIVO**
            - Patrones emergentes y insights soft
            - Factores culturales y sociales
            - Percepciones y sentimientos del mercado
            
            **CORRELACIONES IDENTIFICADAS**
            - Relaciones causa-efecto documentadas
            - Factores impulsores de las tendencias
            - Interdependencias entre hallazgos
            
            **VALIDACIÓN Y CONFIABILIDAD**
            - Assessment de la validez de los hallazgos
            - Limitaciones del análisis
            - Grado de confianza por hallazgo
            
            Total: 1,700-2,100 palabras
            Formato: Estructura clara con subsecciones
            Incluir: Referencias a datos específicos y fuentes
            """,
            agent=agent
        )