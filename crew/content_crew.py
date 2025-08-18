from crewai import Crew, Process
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent
from config.settings import get_llm_config

class ContentCrew:
    """
    Crew principal que coordina los agentes para la creación de contenido
    """
    
    def __init__(self):
        self.llm = get_llm_config()
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.writer_agent = WriterAgent()
        
        # Configurar el crew
        self.crew = Crew(
            agents=[
                self.research_agent.agent,
                self.analyst_agent.agent,
                self.writer_agent.agent
            ],
            tasks=[],
            verbose=True,
            process=Process.sequential
        )
    
    def run(self, topic: str):
        """
        Ejecuta el flujo completo de creación de contenido
        """
        try:
            # Paso 1: Investigación
            print(f"🔍 Iniciando investigación sobre: {topic}")
            research_data = self.research_agent.research_topic(topic)
            
            # Paso 2: Análisis
            print("📊 Analizando contenido de investigación...")
            analysis_insights = self.analyst_agent.analyze_content(research_data)
            
            # Paso 3: Creación de contenido
            print("✍️ Creando contenido final...")
            final_content = self.writer_agent.create_content(
                topic=topic,
                research_data=research_data,
                analysis_insights=analysis_insights
            )
            
            # Resultado final
            result = {
                "topic": topic,
                "research_data": research_data,
                "analysis_insights": analysis_insights,
                "final_content": final_content,
                "status": "completed"
            }
            
            print("✅ Proceso completado exitosamente")
            return result
            
        except Exception as e:
            print(f"❌ Error en el proceso: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "status": "failed"
            }
    
    def run_with_tasks(self, topic: str):
        """
        Ejecuta el crew usando el sistema de tareas de CrewAI
        """
        try:
            # Definir tareas específicas
            research_task = {
                "description": f"Research the topic: {topic}",
                "expected_output": "Comprehensive research data with key facts, trends, and insights",
                "agent": self.research_agent.agent
            }
            
            analysis_task = {
                "description": "Analyze the research data and extract key insights",
                "expected_output": "Analysis report with key insights and recommendations",
                "agent": self.analyst_agent.agent
            }
            
            writing_task = {
                "description": f"Create engaging content about {topic} based on research and analysis",
                "expected_output": "Well-structured, engaging article ready for publication",
                "agent": self.writer_agent.agent
            }
            
            # Ejecutar el crew
            result = self.crew.kickoff()
            
            return {
                "topic": topic,
                "result": result,
                "status": "completed"
            }
            
        except Exception as e:
            print(f"❌ Error en el crew: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "status": "failed"
            }
