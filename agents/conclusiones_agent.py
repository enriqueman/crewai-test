from crewai import Agent
from tools.content_analyzer import ContentAnalyzer

class ConclusionesAgent:
    """
    Agente especializado en la creación de conclusiones y resúmenes ejecutivos
    """
    
    def __init__(self):
        self.agent = Agent(
            role='Conclusions and Executive Summary Specialist',
            goal='Create compelling conclusions that synthesize findings and provide clear takeaways',
            backstory="""You are an expert in creating powerful conclusions and executive summaries. 
            You excel at synthesizing complex information into clear, actionable conclusions that 
            resonate with readers and provide lasting impact. Your conclusions always connect 
            back to the main objectives and leave readers with clear next steps.""",
            verbose=True,
            allow_delegation=False,
            tools=[ContentAnalyzer()]
        )
    
    def create_main_conclusions(self, research_findings, key_insights, objectives):
        """
        Crea las conclusiones principales del estudio
        """
        task = f"""
        Create main conclusions for the research study:
        
        Research Findings:
        {research_findings}
        
        Key Insights:
        {key_insights}
        
        Research Objectives:
        {objectives}
        
        Please develop:
        1. Summary of key findings
        2. Achievement of research objectives
        3. Most significant discoveries
        4. Practical implications
        5. Overall impact assessment
        
        The conclusions should:
        - Be clear and concise
        - Address all research objectives
        - Highlight the most important points
        - Provide actionable insights
        - Leave a lasting impression
        """
        
        result = self.agent.execute(task)
        return result
    
    def create_executive_summary(self, full_content, target_audience):
        """
        Crea un resumen ejecutivo del contenido completo
        """
        task = f"""
        Create an executive summary for the following content:
        
        Full Content:
        {full_content}
        
        Target Audience:
        {target_audience}
        
        Please provide:
        1. One-page executive summary
        2. Key highlights and findings
        3. Strategic implications
        4. Recommendations
        5. Next steps
        
        The executive summary should:
        - Be suitable for busy executives
        - Include only the most critical information
        - Use clear, professional language
        - Provide actionable insights
        - Be visually scannable
        """
        
        result = self.agent.execute(task)
        return result
    
    def synthesize_key_takeaways(self, all_sections, main_arguments):
        """
        Sintetiza los puntos clave de todas las secciones
        """
        task = f"""
        Synthesize key takeaways from all content sections:
        
        All Sections:
        {all_sections}
        
        Main Arguments:
        {main_arguments}
        
        Please identify:
        1. Core messages and themes
        2. Supporting evidence summary
        3. Key recommendations
        4. Critical success factors
        5. Implementation priorities
        
        Focus on:
        - What readers should remember
        - Most actionable insights
        - Evidence-based conclusions
        - Practical applications
        - Strategic importance
        """
        
        result = self.agent.execute(task)
        return result
    
    def create_call_to_action(self, conclusions, target_audience):
        """
        Crea un llamado a la acción basado en las conclusiones
        """
        task = f"""
        Create a compelling call to action based on the conclusions:
        
        Conclusions:
        {conclusions}
        
        Target Audience:
        {target_audience}
        
        Please develop:
        1. Clear action steps
        2. Immediate next steps
        3. Long-term recommendations
        4. Success metrics
        5. Timeline for implementation
        
        The call to action should:
        - Be specific and actionable
        - Address audience needs
        - Provide clear guidance
        - Include success measures
        - Create urgency and motivation
        """
        
        result = self.agent.execute(task)
        return result
    
    def create_future_outlook(self, current_findings, trends, predictions):
        """
        Crea una perspectiva de futuro basada en los hallazgos
        """
        task = f"""
        Create a future outlook section based on current findings:
        
        Current Findings:
        {current_findings}
        
        Industry Trends:
        {trends}
        
        Predictions:
        {predictions}
        
        Please provide:
        1. Future implications of current findings
        2. Emerging opportunities
        3. Potential challenges
        4. Strategic recommendations
        5. Long-term vision
        
        Consider:
        - Market dynamics
        - Technology trends
        - Regulatory changes
        - Competitive landscape
        - Innovation potential
        """
        
        result = self.agent.execute(task)
        return result
    
    def create_final_recommendations(self, all_analysis, stakeholder_needs):
        """
        Crea recomendaciones finales basadas en todo el análisis
        """
        task = f"""
        Create final recommendations based on complete analysis:
        
        Complete Analysis:
        {all_analysis}
        
        Stakeholder Needs:
        {stakeholder_needs}
        
        Please provide:
        1. Priority recommendations
        2. Implementation roadmap
        3. Resource requirements
        4. Risk mitigation strategies
        5. Success measurement criteria
        
        The recommendations should:
        - Be practical and implementable
        - Address stakeholder priorities
        - Include clear timelines
        - Provide measurable outcomes
        - Consider resource constraints
        """
        
        result = self.agent.execute(task)
        return result
