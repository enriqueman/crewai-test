from crewai import Agent
from tools.content_analyzer import ContentAnalyzer

class AbstractKeywordsAgent:
    """
    Agente especializado en la creación de abstracts y palabras clave
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Abstract and Keywords Specialist',
            goal='Create compelling abstracts and identify relevant keywords for academic and professional content',
            backstory="""You are an expert in academic writing and content summarization. 
            You have extensive experience in creating concise, informative abstracts that capture 
            the essence of research and professional content. You excel at identifying the most 
            relevant keywords that will improve content discoverability and SEO performance.""",
            verbose=True,
            allow_delegation=False,
            tools=[ContentAnalyzer()]
        )
    
    def create_abstract(self, topic, research_data, analysis_insights):
        """
        Crea un abstract profesional basado en la investigación y análisis
        """
        task = f"""
        Create a professional abstract for the following topic: {topic}
        
        Research Data:
        {research_data}
        
        Analysis Insights:
        {analysis_insights}
        
        Please create:
        1. A concise abstract (150-250 words) that summarizes the key points
        2. Background context and significance
        3. Main findings or key takeaways
        4. Implications or conclusions
        
        The abstract should be:
        - Clear and concise
        - Professional in tone
        - Suitable for academic or professional audiences
        - Engaging and informative
        """
        
        result = self.agent.execute(task)
        return result
    
    def generate_keywords(self, content, topic):
        """
        Genera palabras clave relevantes para el contenido
        """
        task = f"""
        Generate relevant keywords for the following content and topic: {topic}
        
        Content:
        {content}
        
        Please provide:
        1. Primary keywords (3-5 main terms)
        2. Secondary keywords (5-8 supporting terms)
        3. Long-tail keywords (2-3 specific phrases)
        4. Related terms and synonyms
        5. Keyword difficulty assessment (low/medium/high)
        
        Focus on:
        - Relevance to the topic
        - Search volume potential
        - SEO optimization
        - User intent matching
        """
        
        result = self.agent.execute(task)
        return result
    
    def optimize_abstract_seo(self, abstract, keywords):
        """
        Optimiza el abstract para SEO usando las palabras clave
        """
        task = f"""
        Optimize the following abstract for SEO using the provided keywords:
        
        Abstract:
        {abstract}
        
        Keywords:
        {keywords}
        
        Please provide:
        1. SEO-optimized version of the abstract
        2. Keyword density analysis
        3. Suggestions for improvement
        4. Meta description optimization
        5. Title tag suggestions
        
        Ensure:
        - Natural keyword integration
        - Maintains readability
        - Follows SEO best practices
        - Appropriate keyword density
        """
        
        result = self.agent.execute(task)
        return result
