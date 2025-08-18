from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings
from tools.content_analyzer import AdvancedContentAnalyzer, ContentQualityChecker
from tools.data_validator import DataValidatorTool

class AnalystAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.content_analyzer = AdvancedContentAnalyzer()
        self.quality_checker = ContentQualityChecker()
        self.data_validator = DataValidatorTool()
        
    def create_agent(self) -> Agent:
        """Crea el agente analista con herramientas avanzadas"""
        return Agent(
            role=AgentSettings.ANALYST_AGENT["role"],
            goal=AgentSettings.ANALYST_AGENT["goal"],
            backstory=AgentSettings.ANALYST_AGENT["backstory"],
            verbose=AgentSettings.ANALYST_AGENT["verbose"],
            allow_delegation=AgentSettings.ANALYST_AGENT["allow_delegation"],
            tools=[self.content_analyzer, self.quality_checker, self.data_validator],
            llm=self.model_config.get_default_model()
        )
    
    def create_analysis_task(self, agent: Agent) -> Task:
        """Crea la tarea de análisis estratégico"""
        return Task(
            description="""
            Analiza la investigación realizada sobre tendencias de content marketing y sintetiza 
            la información para crear insights estratégicos accionables. Utiliza las herramientas 
            de análisis para validar y profundizar en los hallazgos.
            
            Tu análisis debe incluir:
            
            1. **PROCESAMIENTO Y VALIDACIÓN DE DATOS** (usar DataValidatorTool):
               - Verificar la calidad y coherencia de la investigación
               - Validar estadísticas y fuentes encontradas
               - Identificar gaps o inconsistencias en los datos
               - Evaluar la credibilidad de las fuentes utilizadas
            
            2. **ANÁLISIS PROFUNDO DE CONTENIDO** (usar AdvancedContentAnalyzer):
               - Extraer keywords y tendencias principales del research
               - Analizar el sentimiento y dirección de las tendencias
               - Identificar patrones emergentes en el contenido analizado
               - Categorizar insights por nivel de impacto y relevancia
            
            3. **SÍNTESIS ESTRATÉGICA** (análisis propio):
               
               **Priorización de Tendencias** (Top 5 más importantes):
               - Criterios: impacto potencial, facilidad de adopción, timeline
               - Análisis de interdependencias entre tendencias
               - Evaluación de riesgo/oportunidad por tendencia
               
               **Análisis de Oportunidades de Negocio**:
               - Identificación de gaps en el mercado
               - Nichos emergentes con potencial
               - Tecnologías con adopción temprana
               - Modelos de monetización nuevos
               
               **Evaluación de Riesgos y Desafíos**:
               - Barreras de entrada identificadas
               - Riesgos tecnológicos y de mercado
               - Competencia emergente
               - Factores regulatorios potenciales
               
               **Framework de Implementación**:
               - Matriz de impacto vs. facilidad de implementación
               - Roadmap sugerido por tipo de empresa
               - Resources y capabilities requeridos
               - Timeline realista de adopción
            
            4. **SEGMENTACIÓN ESTRATÉGICA**:
               
               **Por Tipo de Empresa**:
               - Startups (0-50 empleados): Quick wins y herramientas accesibles
               - PYME (50-500 empleados): Escalabilidad y ROI balanceado
               - Enterprise (500+ empleados): Transformación integral y liderazgo
               
               **Por Industria**:
               - B2B vs B2C: Diferencias en aplicación
               - Vertical específicas: SaaS, e-commerce, servicios
               - Consideraciones regulatorias por sector
               
               **Por Madurez Digital**:
               - Digitally native: Innovación y experimentación
               - En transformación: Modernización gradual
               - Tradicionales: Fundamentos y cambio cultural
            
            5. **RECOMENDACIONES ESTRATÉGICAS**:
               - Top 3 acciones inmediatas (next 90 days)
               - Iniciativas de mediano plazo (3-12 meses)
               - Transformaciones de largo plazo (1-3 años)
               - KPIs y métricas recomendadas para cada fase
               - Budget allocation sugerido por área
            
            6. **FRAMEWORK DE DECISIÓN**:
               - Criterios para evaluar nuevas tecnologías
               - Proceso de adopción recomendado
               - Métricas de éxito por etapa
               - Señales de alerta temprana
            
            **IMPORTANTE**: Usa las herramientas de análisis para validar cada insight mayor 
            y asegurar que las recomendaciones estén basadas en data sólida.
            """,
            expected_output="""
            Un análisis estratégico completo y validado que contenga:
            
            **RESUMEN EJECUTIVO ESTRATÉGICO**
            - 5 insights clave más importantes
            - Recomendación principal para la industria
            - Timeline crítico de adopción
            - ROI esperado por categoría de implementación
            
            **MATRIZ DE TENDENCIAS PRIORIZADAS**
            - Top 5 tendencias con scoring detallado:
              * Impacto potencial (1-10)
              * Facilidad de adopción (1-10)
              * Timeline de materialización
              * Inversión requerida estimada
            
            **ANÁLISIS POR SEGMENTOS**
            - Recomendaciones específicas para:
              * Startups: 3-4 estrategias focalizadas
              * PYME: 4-5 iniciativas balanceadas
              * Enterprise: 5-6 transformaciones integrales
            - Budget allocation % recomendado por segmento
            
            **FRAMEWORK DE IMPLEMENTACIÓN**
            - Matriz impacto vs. facilidad (visual conceptual)
            - Roadmap de 3 fases con milestones específicos
            - Resources y capabilities por fase
            - Timeline realista con dependencies
            
            **ANÁLISIS DE RIESGOS Y OPORTUNIDADES**
            - Top 3 riesgos identificados con estrategias de mitigación
            - Top 3 oportunidades con estrategias de captura
            - Factores críticos de éxito por estrategia
            
            **KPIs Y MÉTRICAS ESTRATÉGICAS**
            - Leading indicators para cada tendencia
            - Lagging indicators para medir ROI
            - Frecuencia de medición recomendada
            - Benchmarks industry cuando disponibles
            
            **RECOMENDACIONES ACCIONABLES**
            - Immediate actions (0-90 días): Lista específica de 5-7 acciones
            - Short-term initiatives (3-12 meses): 4-6 proyectos estratégicos
            - Long-term transformation (1-3 años): 3-4 cambios fundamentales
            - Budget allocation recomendado por timeframe
            
            **VALIDACIÓN DE CALIDAD**
            - Reporte de validación de datos utilizados
            - Nivel de confianza por recomendación
            - Fuentes más críticas identificadas
            - Limitaciones del análisis
            
            Total: 2,500-3,500 palabras
            Formato: Estructura ejecutiva con datos de soporte
            Enfoque: Strategic actionability con ROI claro
            """,
            agent=agent
        )