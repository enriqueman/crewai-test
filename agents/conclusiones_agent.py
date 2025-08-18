from crewai import Agent, Task
from config.settings import ModelConfig, AgentSettings

class ConclusionesAgent:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        
    def create_agent(self) -> Agent:
        """Crea el agente de Conclusiones"""
        return Agent(
            role=AgentSettings.CONCLUSIONES_AGENT["role"],
            goal=AgentSettings.CONCLUSIONES_AGENT["goal"],
            backstory=AgentSettings.CONCLUSIONES_AGENT["backstory"],
            verbose=AgentSettings.CONCLUSIONES_AGENT["verbose"],
            allow_delegation=AgentSettings.CONCLUSIONES_AGENT["allow_delegation"],
            llm=self.model_config.get_default_model()
        )
    
    def create_conclusiones_task(self, agent: Agent) -> Task:
        """Crea la tarea de Conclusiones finales"""
        return Task(
            description="""
            Sintetiza todo el contenido del artículo en conclusiones poderosas, accionables 
            y memorables. Debe ser el cierre perfecto que integre todos los elementos y 
            proporcione valor final al lector.
            
            Tu síntesis debe incluir:
            
            1. **SÍNTESIS EJECUTIVA** (200-250 palabras):
               - Recapitulación de los puntos más importantes
               - Integración de hallazgos con implicaciones
               - Validación de la hipótesis/objetivos iniciales
               - Statement del valor único proporcionado por el artículo
               - Bridge hacia las recomendaciones finales
            
            2. **CONCLUSIONES ESTRATÉGICAS PRINCIPALES** (400-500 palabras):
               
               **Conclusión 1: [El cambio fundamental más importante]**
               - Statement claro y contundente
               - Evidencia de soporte condensada
               - Impacto directo en la industria
               - Timeline de materialización
               
               **Conclusión 2: [La oportunidad más significativa]**
               - Definición clara de la oportunidad
               - Quién puede capitalizarla mejor
               - Recursos necesarios para aprovecharla
               - Ventana de tiempo disponible
               
               **Conclusión 3: [El riesgo más crítico a mitigar]**
               - Descripción del riesgo principal
               - Consecuencias de no actuar
               - Estrategias de mitigación recomendadas
               - Señales de alerta temprana
               
               **Conclusión 4: [La transformación necesaria]**
               - Cambio organizacional requerido
               - Nuevas competencias críticas
               - Roadmap de transformación
               - Métricas de progreso sugeridas
            
            3. **TAKEAWAYS ACCIONABLES** (300-350 palabras):
               
               **Para Implementación Inmediata (0-3 meses)**
               - 3-4 acciones específicas que se pueden iniciar ya
               - Resources mínimos requeridos
               - Quick wins esperados
               - KPIs para medir progreso inicial
               
               **Para Implementación a Mediano Plazo (3-12 meses)**
               - 4-5 iniciativas estratégicas principales
               - Inversiones significativas requeridas
               - Milestones clave a alcanzar
               - Métricas de éxito a largo plazo
               
               **Para Consideración Estratégica (12+ meses)**
               - Transformaciones fundamentales a planear
               - Partnerships y alianzas a considerar
               - Innovaciones disruptivas a explorar
               - Posicionamiento futuro deseado
            
            4. **MENSAJE FINAL INSPIRACIONAL** (150-200 palabras):
               - Visión del futuro del content marketing
               - Llamado a la acción para la industria
               - Mensaje de empoderamiento para los lectores
               - Invitation para continuar la conversación
               - Statement memorable que resuma el artículo
            
            5. **NEXT STEPS CONCRETOS** (100-150 palabras):
               - 3-5 acciones específicas que el lector puede tomar hoy
               - Resources adicionales recomendados
               - Comunidades o expertos a seguir
               - Herramientas específicas a evaluar
               - Próximos contenidos o investigaciones a esperar
            """,
            expected_output="""
            Sección de Conclusiones completa y poderosa que incluya:
            
            **SÍNTESIS EJECUTIVA**
            - Recapitulación integrada de hallazgos principales
            - Validación de objetivos del artículo
            - Value statement del contenido proporcionado
            
            **CONCLUSIONES ESTRATÉGICAS PRINCIPALES**
            - 4 conclusiones específicas y contundentes
            - Cada una con evidencia condensada
            - Impacto claro en diferentes stakeholders
            - Timeline de materialización para cada una
            
            **TAKEAWAYS ACCIONABLES ESTRUCTURADOS**
            - Acciones inmediatas (0-3 meses): 3-4 items específicos
            - Iniciativas mediano plazo (3-12 meses): 4-5 items estratégicos
            - Consideraciones largo plazo (12+ meses): 3-4 transformaciones
            - Cada item con resources y métricas sugeridas
            
            **MENSAJE FINAL INSPIRACIONAL**
            - Visión motivacional del futuro
            - Call-to-action para la industria
            - Statement memorable y quoteable
            - Invitation para engagement continuo
            
            **NEXT STEPS ESPECÍFICOS**
            - Lista concreta de 3-5 acciones inmediatas
            - Resources y herramientas recomendadas
            - Contactos y comunidades relevantes
            - Follow-up content sugerido
            
            Total: 1,150-1,450 palabras
            Tono: Inspiracional pero pragmático
            Enfoque: Action-oriented y memorable
            Formato: Estructurado para fácil scanning y referencia
            """,
            agent=agent
        )