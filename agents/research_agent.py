from crewai import Agent
from tools.web_search_tool import WebSearchTool

class ResearchAgent:
    """
    Agente especializado en investigación y recopilación de información
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Research Specialist',
            goal='Gather comprehensive and accurate information on given topics',
            backstory="""You are an expert research specialist with years of experience 
            in gathering, analyzing, and synthesizing information from various sources. 
            You have a keen eye for credible sources and can quickly identify the most 
            relevant information for any given topic.""",
            verbose=True,
            allow_delegation=False,
            tools=[WebSearchTool()]
        )
    
    def research_topic(self, topic):
        """
        Realiza investigación sobre un tema específico
        """
        task = f"""
        Research the following topic thoroughly: {topic}
        
        Please provide:
        1. Key facts and data points
        2. Current trends and developments
        3. Relevant statistics and figures
        4. Expert opinions and quotes
        5. Recent news and updates
        
        Ensure all information is from credible sources and properly cited.
        """
        
        result = self.agent.execute(task)
        return result
