from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings
from tools.content_analyzer import ContentQualityChecker
from tools.article_formatter import ArticleFormatterTool
from tools.data_validator import FactCheckerTool

class WriterAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.quality_checker = ContentQualityChecker()
        self.article_formatter = ArticleFormatterTool()
        self.fact_checker = FactCheckerTool()
        
    def create_agent(self) -> Agent:
        """Crea el agente escritor con herramientas de calidad"""
        return Agent(
            role=AgentSettings.WRITER_AGENT["role"],
            goal=AgentSettings.WRITER_AGENT["goal"],
            backstory=AgentSettings.WRITER_AGENT["backstory"],
            verbose=AgentSettings.WRITER_AGENT["verbose"],
            allow_delegation=AgentSettings.WRITER_AGENT["allow_delegation"],
            tools=[self.quality_checker, self.article_formatter, self.fact_checker],
            llm=self.model_config.get_default_model()
        )
    
    def create_writing_task(self, agent: Agent) -> Task:
        """Crea la tarea de escritura completa"""
        return Task(
            description="""
            Escribe un artículo completo y profesional sobre las últimas tendencias en content marketing
            basado en la investigación y análisis realizados por los agentes anteriores. Utiliza las 
            herramientas disponibles para asegurar máxima calidad y precisión.
            
            El artículo debe ser:
            - Extenso y detallado (3000-5000 palabras)
            - Profesional pero accesible
            - Bien estructurado con secciones claras
            - Incluir datos y estadísticas específicas
            - Proporcionar ejemplos prácticos
            - Tener un enfoque actionable
            - Pasar validaciones de calidad
            
            **PROCESO DE ESCRITURA RECOMENDADO**:
            
            1. **PLANIFICACIÓN DEL ARTÍCULO**:
               - Definir audiencia objetivo y tone of voice
               - Crear outline detallado con 8-10 secciones principales
               - Identificar key messages y takeaways por sección
               - Planificar integración de datos y ejemplos
            
            2. **ESTRUCTURA REQUERIDA**:
               
               **I. TÍTULO Y META INFORMACIÓN**:
               - Título atractivo y SEO-friendly (8-12 palabras)
               - Meta descripción de 150-160 caracteres
               - Keywords principales identificadas
               - Fecha y autor
               
               **II. INTRODUCCIÓN HOOK (300-400 palabras)**:
               - Estadística impactante o pregunta provocativa
               - Contexto actual de la industria
               - Problema/oportunidad central identificada
               - Preview claro de lo que encontrará el lector
               - Value proposition del artículo
               
               **III. CONTEXTO Y ANTECEDENTES (400-500 palabras)**:
               - Estado actual del content marketing
               - Principales challenges que enfrenta la industria
               - Por qué este análisis es necesario ahora
               - Metodología utilizada en la investigación
               
               **IV. TENDENCIAS PRINCIPALES (2000-2500 palabras total)**:
               
               **Sección A: Inteligencia Artificial y Automatización** (400-500 palabras)
               - Estado actual de adopción de IA
               - Herramientas y tecnologías específicas
               - Casos de éxito documentados
               - ROI y métricas de adopción
               - Predicciones de evolución
               
               **Sección B: Personalización a Escala** (400-500 palabras)
               - Evolución de la personalización
               - Tecnologías habilitadoras
               - Ejemplos de implementación exitosa
               - Challenges y limitaciones
               - Best practices identificadas
               
               **Sección C: Video-First Content Strategy** (400-500 palabras)
               - Dominancia del video en 2024-2025
               - Formatos emergentes (short-form, live, interactive)
               - Plataformas y distribución
               - Métricas de performance
               - Herramientas de producción
               
               **Sección D: Content Marketing Omnichannel** (400-500 palabras)
               - Integración cross-platform
               - Customer journey mapping
               - Attribution y measurement
               - Technology stack necesario
               - Organizacional implications
               
               **Sección E: Emerging Technologies** (400-500 palabras)
               - AR/VR en content marketing
               - Voice search optimization
               - Blockchain y NFTs
               - Metaverse marketing
               - Timeline de adopción esperado
               
               **V. IMPLEMENTACIÓN PRÁCTICA (600-800 palabras)**:
               - Framework de adopción por tipo de empresa
               - Budget allocation recomendado
               - Timeline de implementación realista
               - Team structure y skills necesarios
               - Technology partners y vendors
               - Change management considerations
               
               **VI. CASOS DE ESTUDIO (500-600 palabras)**:
               - 3-4 casos detallados de empresas exitosas
               - Análisis de qué funcionó y por qué
               - Lecciones aplicables por industry
               - ROI y resultados medibles
               - Factores críticos de éxito
               
               **VII. PREDICCIONES Y FUTURO (400-500 palabras)**:
               - Tendencias emergentes a observar
               - Disruptores potenciales
               - Oportunidades de innovación
               - Timeline de materialización
               - Preparación recomendada
               
               **VIII. CONCLUSIÓN ACCIONABLE (300-400 palabras)**:
               - Síntesis de insights clave
               - Top 5 recomendaciones inmediatas
               - Call-to-action específico
               - Next steps para diferentes audiencias
               - Invitation para continuar el diálogo
            
            3. **ESTÁNDARES DE CALIDAD** (usar ContentQualityChecker):
               - Verificar longitud y estructura antes de finalizar
               - Asegurar mínimo 15 estadísticas específicas con fuentes
               - Incluir al menos 8 ejemplos concretos o casos
               - Mantener flow narrativo coherente
               - Optimizar para different reading patterns (scanning, deep reading)
            
            4. **VERIFICACIÓN DE HECHOS** (usar FactCheckerTool):
               - Revisar todas las afirmaciones categóricas
               - Verificar estadísticas sin fuente
               - Suavizar predicciones absolutas
               - Asegurar balance en el tone
            
            5. **FORMATEO FINAL** (usar ArticleFormatterTool):
               - Aplicar formato académico/profesional
               - Incluir tabla de contenidos
               - Asegurar estructura clara con headings
               - Optimizar para SEO y legibilidad
            
            **CRITERIOS DE ÉXITO**:
            - Artículo debe pasar ContentQualityChecker con score >85
            - Fact checking sin issues críticos
            - Estructura coherente y professional
            - Value immediate para diferentes tipos de lectores
            - Actionable insights en cada sección mayor
            """,
            expected_output="""
            Un artículo completo y publication-ready que incluya:
            
            **ARTÍCULO FORMATEADO COMPLETO**
            - 3,000-5,000 palabras total
            - Título SEO-optimizado
            - Meta descripción
            - Estructura clara con 8 secciones principales
            - Transiciones fluidas entre secciones
            
            **CONTENIDO DE ALTA CALIDAD**
            - Mínimo 15 estadísticas específicas citadas
            - 8+ ejemplos prácticos o casos de estudio
            - 3-4 casos de estudio detallados
            - Datos de soporte en cada sección principal
            - Insights accionables por sección
            
            **ELEMENTOS TÉCNICOS**
            - Lista de 10-12 keywords principales integradas naturalmente
            - Tabla de contenidos generada
            - Referencias y fuentes documentadas
            - Call-to-action específico por tipo de audiencia
            
            **REPORTES DE CALIDAD**
            - Score de ContentQualityChecker (target: >85/100)
            - Reporte de FactChecker con issues resueltos
            - Análisis de legibilidad y estructura
            - Tiempo estimado de lectura
            
            **FORMATOS ADICIONALES**
            - Versión blog-friendly con emojis y headings casuales
            - Abstract ejecutivo de 200 palabras
            - Key takeaways en bullet points
            - Social media snippets sugeridos
            
            **METADATA DEL ARTÍCULO**
            - Audiencia objetivo definida
            - Nivel de expertise: intermedio-avanzado
            - Tiempo de lectura: 12-18 minutos
            - Fecha de relevancia: siguiente 12-18 meses
            - Update frequency recomendada: cada 6 meses
            
            El artículo debe estar completamente ready para publicación inmediata
            en cualquier plataforma (blog corporativo, Medium, LinkedIn, etc.)
            """,
            agent=agent
        )