from crewai import Agent
from tools.content_analyzer import ContentAnalyzer

class AnalystAgent:
    """
    Agente especializado en análisis y evaluación de contenido
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Content Analyst',
            goal='Analyze and evaluate content quality, relevance, and insights',
            backstory="""You are a seasoned content analyst with expertise in 
            evaluating information quality, identifying key insights, and determining 
            the most valuable content for specific audiences. You excel at pattern 
            recognition and can spot trends that others might miss.""",
            verbose=True,
            allow_delegation=False,
            tools=[ContentAnalyzer()]
        )
    
    def analyze_content(self, research_data):
        """
        Analiza el contenido de investigación y extrae insights clave
        """
        task = f"""
        Analyze the following research data and provide insights:
        
        {research_data}
        
        Please provide:
        1. Key insights and patterns identified
        2. Data quality assessment
        3. Relevance scoring for different aspects
        4. Recommendations for content focus
        5. Potential angles for content creation
        
        Focus on actionable insights that can guide content creation.
        """
        
        result = self.agent.execute(task)
        return result
