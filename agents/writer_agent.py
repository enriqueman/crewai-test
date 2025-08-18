from crewai import Agent
from tools.article_formatter import ArticleFormatter

class WriterAgent:
    """
    Agente especializado en escritura y creación de contenido
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Content Writer',
            goal='Create engaging, informative, and well-structured content',
            backstory="""You are a talented content writer with years of experience 
            in creating compelling articles, blog posts, and other written content. 
            You have a natural ability to take complex information and transform it 
            into engaging, easy-to-understand content that resonates with readers.""",
            verbose=True,
            allow_delegation=False,
            tools=[ArticleFormatter()]
        )
    
    def create_content(self, topic, research_data, analysis_insights):
        """
        Crea contenido basado en la investigación y análisis
        """
        task = f"""
        Create engaging content on the following topic: {topic}
        
        Research Data:
        {research_data}
        
        Analysis Insights:
        {analysis_insights}
        
        Please create:
        1. A compelling headline
        2. An engaging introduction
        3. Well-structured body content with clear sections
        4. Key takeaways and conclusions
        5. A call-to-action if appropriate
        
        Ensure the content is:
        - Engaging and easy to read
        - Well-researched and accurate
        - Optimized for the target audience
        - SEO-friendly where applicable
        """
        
        result = self.agent.execute(task)
        return result
