from crewai import Agent
from tools.content_analyzer import ContentAnalyzer

class DiscusionAgent:
    """
    Agente especializado en la creación de secciones de discusión
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Discussion and Analysis Specialist',
            goal='Create comprehensive discussion sections that interpret results and provide deep insights',
            backstory="""You are an expert in academic writing and critical analysis. 
            You excel at creating discussion sections that go beyond simple result reporting 
            to provide deep insights, critical analysis, and meaningful interpretation. 
            Your discussions always connect findings to broader implications and future research.""",
            verbose=True,
            allow_delegation=False,
            tools=[ContentAnalyzer()]
        )
    
    def create_discussion_section(self, results, research_context, literature_review):
        """
        Crea una sección de discusión completa
        """
        task = f"""
        Create a comprehensive discussion section for the research:
        
        Research Results:
        {results}
        
        Research Context:
        {research_context}
        
        Literature Review:
        {literature_review}
        
        Please develop:
        1. Interpretation of key findings
        2. Comparison with existing literature
        3. Theoretical implications
        4. Practical applications
        5. Limitations and caveats
        
        The discussion should:
        - Provide deep analysis, not just summary
        - Connect findings to broader context
        - Address research questions directly
        - Identify unexpected findings
        - Suggest future research directions
        """
        
        result = self.agent.execute(task)
        return result
    
    def analyze_implications(self, findings, target_audience):
        """
        Analiza las implicaciones de los hallazgos
        """
        task = f"""
        Analyze the implications of the research findings:
        
        Key Findings:
        {findings}
        
        Target Audience:
        {target_audience}
        
        Please examine:
        1. Theoretical implications
        2. Practical applications
        3. Policy implications (if applicable)
        4. Industry impact
        5. Societal relevance
        
        Consider:
        - Immediate vs. long-term implications
        - Different stakeholder perspectives
        - Implementation challenges
        - Success factors
        - Risk assessment
        """
        
        result = self.agent.execute(task)
        return result
    
    def address_limitations(self, research_design, methodology, results):
        """
        Aborda las limitaciones del estudio
        """
        task = f"""
        Address the limitations of the research study:
        
        Research Design:
        {research_design}
        
        Methodology:
        {methodology}
        
        Results:
        {results}
        
        Please identify:
        1. Methodological limitations
        2. Sample size and selection issues
        3. Data collection constraints
        4. Analysis limitations
        5. Generalizability concerns
        
        For each limitation:
        - Explain its impact on results
        - Suggest mitigation strategies
        - Acknowledge transparency
        - Provide context for interpretation
        """
        
        result = self.agent.execute(task)
        return result
    
    def suggest_future_research(self, current_findings, identified_gaps):
        """
        Sugiere direcciones para investigación futura
        """
        task = f"""
        Suggest future research directions based on current findings:
        
        Current Findings:
        {current_findings}
        
        Identified Gaps:
        {identified_gaps}
        
        Please recommend:
        1. Immediate follow-up studies
        2. Long-term research agenda
        3. Methodological improvements
        4. New research questions
        5. Collaborative opportunities
        
        Consider:
        - Feasibility and resources
        - Scientific priority
        - Practical relevance
        - Innovation potential
        - Impact on the field
        """
        
        result = self.agent.execute(task)
        return result
    
    def create_critical_analysis(self, results, alternative_explanations):
        """
        Crea un análisis crítico de los resultados
        """
        task = f"""
        Create a critical analysis of the research results:
        
        Research Results:
        {results}
        
        Alternative Explanations:
        {alternative_explanations}
        
        Please provide:
        1. Critical evaluation of findings
        2. Alternative interpretations
        3. Confounding factors
        4. Bias assessment
        5. Robustness of conclusions
        
        The analysis should:
        - Be objective and balanced
        - Consider multiple perspectives
        - Identify potential weaknesses
        - Suggest validation approaches
        - Maintain scientific rigor
        """
        
        result = self.agent.execute(task)
        return result
