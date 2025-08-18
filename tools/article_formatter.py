import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class ArticleFormatterInput(BaseModel):
    """Input para el formateador de artículos"""
    sections: Dict[str, str] = Field(..., description="Diccionario con todas las secciones del artículo")
    title: str = Field(..., description="Título principal del artículo")
    author: str = Field(default="CrewAI Research Team", description="Autor del artículo")
    format_type: str = Field(default="academic", description="Tipo de formato: academic, blog, whitepaper, report")
    include_toc: bool = Field(default=True, description="Incluir tabla de contenidos")
    include_metadata: bool = Field(default=True, description="Incluir metadata del artículo")

class ArticleFormatterTool(BaseTool):
    name: str = "Article Formatter Tool"
    description: str = """
    Herramienta para formatear artículos académicos y profesionales.
    Combina todas las secciones en un documento cohesivo y bien estructurado.
    Soporta múltiples formatos: académico, blog, whitepaper, y reportes.
    """
    args_schema: type[BaseModel] = ArticleFormatterInput
    
    def __init__(self):
        super().__init__()
        
    def _run(self, sections: Dict[str, str], title: str, author: str = "CrewAI Research Team", 
             format_type: str = "academic", include_toc: bool = True, include_metadata: bool = True) -> str:
        """Formatea el artículo completo"""
        try:
            if format_type == "academic":
                return self._format_academic_article(sections, title, author, include_toc, include_metadata)
            elif format_type == "blog":
                return self._format_blog_post(sections, title, author, include_metadata)
            elif format_type == "whitepaper":
                return self._format_whitepaper(sections, title, author, include_toc, include_metadata)
            elif format_type == "report":
                return self._format_business_report(sections, title, author, include_toc, include_metadata)
            else:
                return self._format_academic_article(sections, title, author, include_toc, include_metadata)
                
        except Exception as e:
            return f"Error formateando artículo: {str(e)}"
    
    def _format_academic_article(self, sections: Dict[str, str], title: str, author: str, 
                                include_toc: bool, include_metadata: bool) -> str:
        """Formatea como artículo académico"""
        article_parts = []
        
        # Header académico
        if include_metadata:
            article_parts.append(self._create_academic_header(title, author))
        
        # Abstract y keywords (si están disponibles)
        if 'abstract_keywords' in sections and sections['abstract_keywords']:
            article_parts.append("## Abstract")
            article_parts.append(self._extract_abstract(sections['abstract_keywords']))
            article_parts.append("")
            
            keywords = self._extract_keywords(sections['abstract_keywords'])
            if keywords:
                article_parts.append("**Keywords:** " + keywords)
                article_parts.append("")
        
        # Tabla de contenidos
        if include_toc:
            toc = self._generate_table_of_contents(sections)
            if toc:
                article_parts.append("## Tabla de Contenidos")
                article_parts.append(toc)
                article_parts.append("")
        
        # Introducción y marco teórico
        if 'abstract_keywords' in sections and sections['abstract_keywords']:
            marco_teorico = self._extract_marco_teorico(sections['abstract_keywords'])
            if marco_teorico:
                article_parts.append("## 1. Introducción y Marco Teórico")
                article_parts.append(marco_teorico)
                article_parts.append("")
        
        # Revisión de literatura (research)
        if 'research' in sections and sections['research']:
            article_parts.append("## 2. Revisión de Literatura")
            article_parts.append(self._format_section_content(sections['research']))
            article_parts.append("")
        
        # Metodología (analysis)
        if 'analysis' in sections and sections['analysis']:
            article_parts.append("## 3. Metodología y Análisis")
            article_parts.append(self._format_section_content(sections['analysis']))
            article_parts.append("")
        
        # Desarrollo principal
        if 'desarrollo' in sections and sections['desarrollo']:
            article_parts.append("## 4. Desarrollo y Tendencias Identificadas")
            article_parts.append(self._format_section_content(sections['desarrollo']))
            article_parts.append("")
        
        # Resultados
        if 'resultados' in sections and sections['resultados']:
            article_parts.append("## 5. Resultados y Hallazgos")
            article_parts.append(self._format_section_content(sections['resultados']))
            article_parts.append("")
        
        # Discusión
        if 'discusion' in sections and sections['discusion']:
            article_parts.append("## 6. Discusión e Implicaciones")
            article_parts.append(self._format_section_content(sections['discusion']))
            article_parts.append("")
        
        # Conclusiones
        if 'conclusiones' in sections and sections['conclusiones']:
            article_parts.append("## 7. Conclusiones")
            article_parts.append(self._format_section_content(sections['conclusiones']))
            article_parts.append("")
        
        # Referencias
        if 'bibliografia' in sections and sections['bibliografia']:
            article_parts.append("## Referencias")
            article_parts.append(self._format_section_content(sections['bibliografia']))
            article_parts.append("")
        
        # Footer académico
        if include_metadata:
            article_parts.append(self._create_academic_footer())
        
        return "\n".join(article_parts)
    
    def _format_blog_post(self, sections: Dict[str, str], title: str, author: str, include_metadata: bool) -> str:
        """Formatea como blog post"""
        article_parts = []
        
        # Header de blog
        if include_metadata:
            article_parts.append(self._create_blog_header(title, author))
        
        # Introducción engaging
        if 'abstract_keywords' in sections:
            intro = self._extract_blog_intro(sections['abstract_keywords'])
            if intro:
                article_parts.append(intro)
                article_parts.append("")
        
        # Contenido principal
        if 'desarrollo' in sections and sections['desarrollo']:
            # Convertir headings académicos a estilo blog
            content = self._convert_to_blog_style(sections['desarrollo'])
            article_parts.append(content)
            article_parts.append("")
        
        # Sección de takeaways
        if 'conclusiones' in sections and sections['conclusiones']:
            article_parts.append("## 🎯 Key Takeaways")
            takeaways = self._extract_takeaways(sections['conclusiones'])
            article_parts.append(takeaways)
            article_parts.append("")
        
        # Call to action
        article_parts.append(self._create_blog_cta())
        
        return "\n".join(article_parts)
    
    def _format_whitepaper(self, sections: Dict[str, str], title: str, author: str, 
                          include_toc: bool, include_metadata: bool) -> str:
        """Formatea como whitepaper"""
        article_parts = []
        
        # Cover page
        if include_metadata:
            article_parts.append(self._create_whitepaper_cover(title, author))
        
        # Executive Summary
        if 'abstract_keywords' in sections:
            exec_summary = self._extract_executive_summary(sections['abstract_keywords'])
            if exec_summary:
                article_parts.append("## Executive Summary")
                article_parts.append(exec_summary)
                article_parts.append("")
        
        # TOC
        if include_toc:
            toc = self._generate_table_of_contents(sections)
            if toc:
                article_parts.append("## Table of Contents")
                article_parts.append(toc)
                article_parts.append("")
        
        # Secciones principales formateadas para whitepaper
        section_mapping = {
            'research': 'Market Research and Analysis',
            'desarrollo': 'Current Trends and Insights',
            'resultados': 'Key Findings',
            'discusion': 'Strategic Implications',
            'conclusiones': 'Recommendations and Next Steps'
        }
        
        section_counter = 1
        for key, section_title in section_mapping.items():
            if key in sections and sections[key]:
                article_parts.append(f"## {section_counter}. {section_title}")
                article_parts.append(self._format_section_content(sections[key]))
                article_parts.append("")
                section_counter += 1
        
        # Appendix con referencias
        if 'bibliografia' in sections and sections['bibliografia']:
            article_parts.append("## Appendix A: References and Sources")
            article_parts.append(self._format_section_content(sections['bibliografia']))
        
        return "\n".join(article_parts)
    
    def _format_business_report(self, sections: Dict[str, str], title: str, author: str,
                               include_toc: bool, include_metadata: bool) -> str:
        """Formatea como reporte de negocio"""
        article_parts = []
        
        # Header ejecutivo
        if include_metadata:
            article_parts.append(self._create_business_report_header(title, author))
        
        # Resumen ejecutivo
        if 'abstract_keywords' in sections:
            exec_summary = self._extract_executive_summary(sections['abstract_keywords'])
            if exec_summary:
                article_parts.append("## Resumen Ejecutivo")
                article_parts.append(exec_summary)
                article_parts.append("")
        
        # Principales hallazgos (destacados)
        if 'resultados' in sections:
            key_findings = self._extract_key_findings_summary(sections['resultados'])
            if key_findings:
                article_parts.append("## Principales Hallazgos")
                article_parts.append(key_findings)
                article_parts.append("")
        
        # TOC
        if include_toc:
            article_parts.append("## Índice")
            article_parts.append(self._generate_table_of_contents(sections))
            article_parts.append("")
        
        # Secciones del reporte
        report_sections = {
            'research': 'Investigación de Mercado',
            'desarrollo': 'Análisis de Tendencias',
            'resultados': 'Resultados Detallados',
            'discusion': 'Implicaciones Estratégicas',
            'conclusiones': 'Recomendaciones'
        }
        
        for key, section_title in report_sections.items():
            if key in sections and sections[key]:
                article_parts.append(f"## {section_title}")
                article_parts.append(self._format_section_content(sections[key]))
                article_parts.append("")
        
        # Anexos
        if 'bibliografia' in sections and sections['bibliografia']:
            article_parts.append("## Anexo: Referencias y Fuentes")
            article_parts.append(self._format_section_content(sections['bibliografia']))
        
        return "\n".join(article_parts)
    
    # Métodos de utilidad para extraer y formatear contenido específico
    
    def _create_academic_header(self, title: str, author: str) -> str:
        """Crea header académico"""
        date = datetime.now().strftime("%B %Y")
        return f"""# {title}

**Autor:** {author}  
**Fecha:** {date}  
**Tipo:** Artículo de Investigación  

---
"""
    
    def _create_blog_header(self, title: str, author: str) -> str:
        """Crea header de blog"""
        date = datetime.now().strftime("%B %d, %Y")
        return f"""# {title}

*Por {author} | {date}*

---
"""
    
    def _create_whitepaper_cover(self, title: str, author: str) -> str:
        """Crea portada de whitepaper"""
        date = datetime.now().strftime("%B %Y")
        return f"""# {title}

## A Comprehensive Analysis of Content Marketing Trends

**Prepared by:** {author}  
**Date:** {date}  
**Document Type:** Whitepaper  

---
"""
    
    def _create_business_report_header(self, title: str, author: str) -> str:
        """Crea header de reporte de negocio"""
        date = datetime.now().strftime("%B %Y")
        return f"""# {title}

**Reporte Estratégico**

**Preparado por:** {author}  
**Fecha:** {date}  
**Tipo de documento:** Análisis Estratégico  

---
"""
    
    def _extract_abstract(self, abstract_section: str) -> str:
        """Extrae el abstract de la sección correspondiente"""
        # Buscar la sección de abstract
        abstract_match = re.search(r'\*\*ABSTRACT.*?\*\*(.*?)(?=\*\*|$)', abstract_section, re.DOTALL | re.IGNORECASE)
        if abstract_match:
            return abstract_match.group(1).strip()
        return abstract_section[:300] + "..." if len(abstract_section) > 300 else abstract_section
    
    def _extract_keywords(self, abstract_section: str) -> str:
        """Extrae keywords de la sección correspondiente"""
        # Buscar keywords primarias
        keywords_match = re.search(r'Keywords primarias[:\s]*([^\n\r]+)', abstract_section, re.IGNORECASE)
        if keywords_match:
            return keywords_match.group(1).strip()
        return ""
    
    def _extract_marco_teorico(self, abstract_section: str) -> str:
        """Extrae el marco teórico"""
        marco_match = re.search(r'\*\*MARCO TEÓRICO.*?\*\*(.*?)(?=\*\*|$)', abstract_section, re.DOTALL | re.IGNORECASE)
        if marco_match:
            return marco_match.group(1).strip()
        return ""
    
    def _generate_table_of_contents(self, sections: Dict[str, str]) -> str:
        """Genera tabla de contenidos"""
        toc_items = []
        
        section_titles = {
            'abstract_keywords': '1. Introducción y Marco Teórico',
            'research': '2. Revisión de Literatura', 
            'analysis': '3. Metodología y Análisis',
            'desarrollo': '4. Desarrollo y Tendencias',
            'resultados': '5. Resultados y Hallazgos',
            'discusion': '6. Discusión e Implicaciones',
            'conclusiones': '7. Conclusiones',
            'bibliografia': 'Referencias'
        }
        
        for key, title in section_titles.items():
            if key in sections and sections[key]:
                toc_items.append(f"- {title}")
        
        return "\n".join(toc_items)
    
    def _format_section_content(self, content: str) -> str:
        """Formatea el contenido de una sección"""
        # Limpiar el contenido
        formatted = content.strip()
        
        # Asegurar espaciado correcto después de headings
        formatted = re.sub(r'^(#{1,6}\s+.+)$', r'\1\n', formatted, flags=re.MULTILINE)
        
        # Asegurar espaciado correcto en listas
        formatted = re.sub(r'^(\s*[-*+]\s+)', r'\1', formatted, flags=re.MULTILINE)
        
        return formatted
    
    def _convert_to_blog_style(self, content: str) -> str:
        """Convierte contenido académico a estilo blog"""
        # Cambiar headings académicos por más casuales
        content = re.sub(r'## (\d+\.?\s*)', '## ', content)
        
        # Agregar emojis a algunos headings
        emoji_map = {
            'tendencias': '📈',
            'tecnolog': '💻',
            'estrategi': '🎯',
            'implement': '⚙️',
            'casos': '📋',
            'ejemplos': '💡'
        }
        
        for keyword, emoji in emoji_map.items():
            content = re.sub(f'(## [^{emoji}]*{keyword}[^\\n]*)', f'{emoji} \\1', content, flags=re.IGNORECASE)
        
        return content
    
    def _extract_takeaways(self, conclusions_section: str) -> str:
        """Extrae takeaways principales de las conclusiones"""
        # Buscar takeaways accionables
        takeaways_match = re.search(r'\*\*TAKEAWAYS ACCIONABLES.*?\*\*(.*?)(?=\*\*|$)', conclusions_section, re.DOTALL | re.IGNORECASE)
        if takeaways_match:
            return takeaways_match.group(1).strip()
        
        # Si no encuentra la sección específica, tomar las primeras conclusiones
        return conclusions_section[:500] + "..." if len(conclusions_section) > 500 else conclusions_section
    
    def _extract_executive_summary(self, abstract_section: str) -> str:
        """Extrae resumen ejecutivo"""
        return self._extract_abstract(abstract_section)
    
    def _extract_key_findings_summary(self, results_section: str) -> str:
        """Extrae resumen de hallazgos clave"""
        # Buscar la sección de resumen ejecutivo de hallazgos
        summary_match = re.search(r'\*\*RESUMEN EJECUTIVO.*?\*\*(.*?)(?=\*\*|$)', results_section, re.DOTALL | re.IGNORECASE)
        if summary_match:
            return summary_match.group(1).strip()
        
        return results_section[:400] + "..." if len(results_section) > 400 else results_section
    
    def _create_blog_cta(self) -> str:
        """Crea call-to-action para blog"""
        return """---

## 💬 ¿Qué opinas?

¿Cuáles de estas tendencias están implementando en tu estrategia de content marketing? ¿Qué otros desafíos has identificado? 

Comparte tu experiencia en los comentarios y conectemos para seguir explorando el futuro del marketing de contenidos.

**¿Te ha sido útil este análisis?** Compártelo con tu equipo y síguenos para más insights sobre las últimas tendencias en marketing digital."""
    
    def _create_academic_footer(self) -> str:
        """Crea footer académico"""
        return """---

*Este artículo ha sido generado utilizando metodologías de investigación avanzadas y análisis de múltiples fuentes especializadas. Para citar este trabajo, utiliza el formato académico estándar incluyendo autor, título, fecha y fuente.*

**Descargo de responsabilidad:** Las opiniones y análisis presentados en este documento están basados en la investigación disponible al momento de la publicación y pueden estar sujetos a cambios conforme evolucione la industria."""


class DocumentExporter(BaseTool):
    name: str = "Document Exporter"
    description: str = """
    Exporta artículos formateados a diferentes formatos de archivo.
    Soporta Markdown, HTML, y otros formatos de documentos.
    """
    
    def _run(self, content: str, format_type: str = "markdown", filename: str = "article") -> str:
        """Exporta el documento al formato especificado"""
        try:
            if format_type == "html":
                return self._export_to_html(content, filename)
            elif format_type == "markdown":
                return self._export_to_markdown(content, filename)
            else:
                return f"Formato no soportado: {format_type}"
        except Exception as e:
            return f"Error exportando documento: {str(e)}"
    
    def _export_to_html(self, content: str, filename: str) -> str:
        """Convierte a HTML"""
        # Conversión básica de Markdown a HTML
        html_content = content
        
        # Convertir headings
        html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        
        # Convertir listas
        html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
        
        # Convertir párrafos
        html_content = re.sub(r'\n\n', '</p>\n<p>', html_content)
        html_content = '<p>' + html_content + '</p>'
        
        # Plantilla HTML básica
        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        p {{ line-height: 1.6; }}
        li {{ margin-bottom: 5px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        return f"Documento HTML generado:\n```html\n{html_template}\n```"
    
    def _export_to_markdown(self, content: str, filename: str) -> str:
        """Exporta como Markdown limpio"""
        return f"Documento Markdown generado ({filename}.md):\n\n```markdown\n{content}\n```"