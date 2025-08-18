from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings

class BibliografiaAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        
    def create_agent(self) -> Agent:
        """Crea el agente de Bibliografía"""
        return Agent(
            role=AgentSettings.BIBLIOGRAFIA_AGENT["role"],
            goal=AgentSettings.BIBLIOGRAFIA_AGENT["goal"],
            backstory=AgentSettings.BIBLIOGRAFIA_AGENT["backstory"],
            verbose=AgentSettings.BIBLIOGRAFIA_AGENT["verbose"],
            allow_delegation=AgentSettings.BIBLIOGRAFIA_AGENT["allow_delegation"],
            llm=self.model_config.get_default_model()
        )
    
    def create_bibliografia_task(self, agent: Agent) -> Task:
        """Crea la tarea de Bibliografía y Referencias"""
        return Task(
            description="""
            Crea una bibliografía profesional y completa que incluya todas las fuentes 
            utilizadas en el artículo, formateadas según estándares académicos y profesionales.
            
            Tu tarea incluye:
            
            1. **IDENTIFICACIÓN DE FUENTES**:
               - Extraer todas las referencias mencionadas en el artículo
               - Identificar fuentes citadas directa e indirectamente
               - Categorizar por tipo de fuente (estudios, reportes, artículos, etc.)
               - Verificar credibilidad y autoridad de cada fuente
               - Priorizar fuentes primarias sobre secundarias
            
            2. **FORMATEO PROFESIONAL DE REFERENCIAS**:
               
               **Estudios y Reportes de Investigación**
               - Formato: Autor(es). (Año). "Título del Estudio". Institución/Organización. URL. [Fecha de acceso]
               - Incluir metodología cuando esté disponible
               - Mencionar tamaño de muestra y geografía si es relevante
               
               **Artículos de Publicaciones Especializadas**
               - Formato: Autor. (Fecha). "Título del Artículo". Nombre de la Publicación. URL. [Fecha de acceso]
               - Indicar si es contenido premium o gated
               
               **Reportes de Empresas y Agencias**
               - Formato: Empresa/Agencia. (Año). "Título del Reporte". [Tipo de reporte]. URL. [Fecha de acceso]
               - Distinguir entre reportes públicos y privados
               
               **Datos Estadísticos y Métricas**
               - Formato: Fuente de Datos. (Año). "Descripción del Dataset/Métrica". Plataforma/Tool. URL. [Fecha de acceso]
               - Incluir periodo de tiempo cubierto por los datos
               
               **Casos de Estudio y Ejemplos**
               - Formato: Empresa. (Año). "Descripción del Caso". Fuente de Información. URL. [Fecha de acceso]
               - Indicar si el caso fue public disclosure o case study formal
            
            3. **ORGANIZACIÓN Y CATEGORIZACIÓN**:
               
               **Referencias Primarias** (Fuentes originales de datos/investigación):
               - Estudios académicos peer-reviewed
               - Reportes de investigación original
               - Datos primarios de plataformas
               - Surveys y encuestas originales
               
               **Referencias Secundarias** (Análisis y interpretaciones):
               - Artículos de análisis en publicaciones especializadas
               - Reportes de agencias basados en múltiples fuentes
               - Análisis de expertos y thought leaders
               
               **Referencias de Apoyo** (Contexto y ejemplos):
               - Casos de estudio públicos
               - Ejemplos de implementación
               - Best practices documentadas
               - Tools y plataformas mencionadas
            
            4. **CONTROL DE CALIDAD**:
               - Verificar que todas las URLs estén activas
               - Confirmar fechas de publicación y acceso
               - Validar credibilidad de las fuentes
               - Asegurar diversidad en tipos de fuentes
               - Mantener balance entre fuentes académicas y practitioner
            
            5. **RECURSOS ADICIONALES**:
               - Lecturas recomendadas para profundizar
               - Expertos y thought leaders a seguir
               - Publicaciones especializadas relevantes
               - Conferencias y eventos relacionados
               - Herramientas y plataformas mencionadas
            """,
            expected_output="""
            Sección completa de Bibliografía y Referencias que incluya:
            
            **REFERENCIAS PRIMARIAS** (15-20 fuentes)
            - Estudios académicos y de investigación
            - Reportes originales de organizaciones reconocidas
            - Datos primarios de plataformas líderes
            - Formato profesional consistente
            - Ordenadas alfabéticamente por autor/organización
            
            **REFERENCIAS SECUNDARIAS** (10-15 fuentes)
            - Artículos de análisis en publicaciones especializadas
            - Reportes de agencias y consultoras
            - Análisis de expertos reconocidos
            - Formato consistente con referencias primarias
            
            **REFERENCIAS DE APOYO** (8-12 fuentes)
            - Casos de estudio específicos
            - Ejemplos de implementación
            - Best practices documentadas
            - Herramientas y plataformas citadas
            
            **NOTAS DE CREDIBILIDAD**
            - Indicador de calidad/confiabilidad por fuente
            - Fecha de última verificación de URLs
            - Comentarios sobre limitaciones de datos cuando relevante
            
            **RECURSOS ADICIONALES RECOMENDADOS**
            - 5-8 lecturas complementarias
            - 3-5 expertos/thought leaders a seguir
            - 2-3 publicaciones especializadas
            - 3-5 conferencias/eventos anuales relevantes
            - 5-7 herramientas/plataformas útiles
            
            **TOTAL ESTIMADO**: 35-50 referencias bien categorizadas
            **FORMATO**: Estilo académico modificado para business
            **CALIDAD**: URLs verificadas, fuentes creíbles, diversidad adecuada
            **ORGANIZACIÓN**: Clara categorización y easy scanning
            """,
            agent=agent
        )