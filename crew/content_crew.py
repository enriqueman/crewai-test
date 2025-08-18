from crewai import Crew, Process
from config.settings import ModelConfig
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.abstract_keywords_agent import AbstractKeywordsAgent
from agents.desarrollo_agent import DesarrolloAgent
from agents.resultados_agent import ResultadosAgent
from agents.discusion_agent import DiscusionAgent
from agents.conclusiones_agent import ConclusionesAgent
from agents.bibliografia_agent import BibliografiaAgent

class ContentMarketingCrew:
    def __init__(self):
        self.model_config = ModelConfig()
        
        # Inicializar agentes
        self.research_agent = ResearchAgent(self.model_config)
        self.analyst_agent = AnalystAgent(self.model_config)
        self.abstract_keywords_agent = AbstractKeywordsAgent(self.model_config)
        self.desarrollo_agent = DesarrolloAgent(self.model_config)
        self.resultados_agent = ResultadosAgent(self.model_config)
        self.discusion_agent = DiscusionAgent(self.model_config)
        self.conclusiones_agent = ConclusionesAgent(self.model_config)
        self.bibliografia_agent = BibliografiaAgent(self.model_config)
        
        # Crear agentes
        self.researcher = self.research_agent.create_agent()
        self.analyst = self.analyst_agent.create_agent()
        self.abstract_writer = self.abstract_keywords_agent.create_agent()
        self.content_developer = self.desarrollo_agent.create_agent()
        self.results_analyst = self.resultados_agent.create_agent()
        self.discussion_strategist = self.discusion_agent.create_agent()
        self.conclusions_synthesizer = self.conclusiones_agent.create_agent()
        self.bibliography_specialist = self.bibliografia_agent.create_agent()
        
        # Crear tareas
        self.research_task = self.research_agent.create_research_task(self.researcher)
        self.analysis_task = self.analyst_agent.create_analysis_task(self.analyst)
        self.abstract_task = self.abstract_keywords_agent.create_abstract_task(self.abstract_writer)
        self.desarrollo_task = self.desarrollo_agent.create_desarrollo_task(self.content_developer)
        self.resultados_task = self.resultados_agent.create_resultados_task(self.results_analyst)
        self.discusion_task = self.discusion_agent.create_discusion_task(self.discussion_strategist)
        self.conclusiones_task = self.conclusiones_agent.create_conclusiones_task(self.conclusions_synthesizer)
        self.bibliografia_task = self.bibliografia_agent.create_bibliografia_task(self.bibliography_specialist)
        
        # Configurar dependencias entre tareas
        self.analysis_task.context = [self.research_task]
        self.abstract_task.context = [self.research_task, self.analysis_task]
        self.desarrollo_task.context = [self.research_task, self.analysis_task, self.abstract_task]
        self.resultados_task.context = [self.research_task, self.analysis_task]
        self.discusion_task.context = [self.research_task, self.analysis_task, self.resultados_task]
        self.conclusiones_task.context = [self.research_task, self.analysis_task, self.abstract_task, 
                                         self.desarrollo_task, self.resultados_task, self.discusion_task]
        self.bibliografia_task.context = [self.research_task, self.analysis_task, self.desarrollo_task, 
                                         self.resultados_task, self.discusion_task]
    
    def create_crew(self) -> Crew:
        """Crea y configura el crew completo con todos los agentes especializados"""
        return Crew(
            agents=[
                self.researcher,
                self.analyst,
                self.abstract_writer,
                self.content_developer,
                self.results_analyst,
                self.discussion_strategist,
                self.conclusions_synthesizer,
                self.bibliography_specialist
            ],
            tasks=[
                self.research_task,
                self.analysis_task,
                self.abstract_task,
                self.desarrollo_task,
                self.resultados_task,
                self.discusion_task,
                self.conclusiones_task,
                self.bibliografia_task
            ],
            process=Process.sequential,  # Ejecutar tareas secuencialmente
            verbose=2,  # Logging detallado
            # memory=True,  # Habilitar memoria para contexto compartido
        )
    
    def run_crew(self, topic: str = None) -> dict:
        """Ejecuta el crew completo con todos los agentes especializados"""
        try:
            # Personalizar el topic si se proporciona
            if topic:
                self.research_task.description = f"""
                Realiza una investigación exhaustiva sobre las últimas tendencias en content marketing 
                específicamente relacionadas con: {topic}
                
                {self.research_task.description}
                """
            
            crew = self.create_crew()
            result = crew.kickoff()
            
            return {
                "success": True,
                "result": result,
                "topic": topic or "Tendencias generales en content marketing",
                "outputs": {
                    "research": getattr(self.research_task, 'output', None),
                    "analysis": getattr(self.analysis_task, 'output', None),
                    "abstract_keywords": getattr(self.abstract_task, 'output', None),
                    "desarrollo": getattr(self.desarrollo_task, 'output', None),
                    "resultados": getattr(self.resultados_task, 'output', None),
                    "discusion": getattr(self.discusion_task, 'output', None),
                    "conclusiones": getattr(self.conclusiones_task, 'output', None),
                    "bibliografia": getattr(self.bibliografia_task, 'output', None)
                },
                "metadata": {
                    "agents_count": 8,
                    "tasks_executed": 8,
                    "specialized_sections": [
                        "research", "analysis", "abstract_keywords", 
                        "desarrollo", "resultados", "discusion", 
                        "conclusiones", "bibliografia"
                    ]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "details": "Error durante la ejecución del crew especializado"
            }
    
    def get_crew_status(self) -> dict:
        """Obtiene el estado actual del crew especializado"""
        return {
            "agents": {
                "researcher": "initialized",
                "analyst": "initialized",
                "abstract_writer": "initialized",
                "content_developer": "initialized",
                "results_analyst": "initialized",
                "discussion_strategist": "initialized",
                "conclusions_synthesizer": "initialized",
                "bibliography_specialist": "initialized"
            },
            "tasks": {
                "research": "pending",
                "analysis": "pending",
                "abstract_keywords": "pending",
                "desarrollo": "pending",
                "resultados": "pending",
                "discusion": "pending",
                "conclusiones": "pending",
                "bibliografia": "pending"
            },
            "workflow": {
                "type": "sequential_specialized",
                "total_agents": 8,
                "total_tasks": 8,
                "estimated_completion_time": "20-30 minutes",
                "specialization_level": "academic_quality"
            },
            "model_config": {
                "openai_available": bool(self.model_config.openai_api_key),
                "default_model": "OpenAI" if self.model_config.openai_api_key else "Local"
            }
        }