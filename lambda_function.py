import json
import os
import logging
from typing import Dict, Any
from crew.content_crew import ContentMarketingCrew

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Función principal de Lambda para el sistema de agentes de content marketing
    
    Parámetros esperados en el event:
    - action: 'generate_article', 'get_status', 'health_check'
    - topic: (opcional) tema específico para el artículo
    - config: (opcional) configuraciones adicionales
    """
    
    # Headers para CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    
    try:
        # Manejar preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Parsear el body si viene como string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        action = body.get('action', event.get('action', 'generate_article'))
        topic = body.get('topic', event.get('topic'))
        crew_type = body.get('crew_type', event.get('crew_type', 'basic'))  # Nuevo parámetro
        format_type = body.get('format_type', event.get('format_type', 'blog'))  # Nuevo parámetro
        
        logger.info(f"Ejecutando acción: {action}, crew_type: {crew_type}, format: {format_type}")
        
        # Validar variables de entorno críticas
        required_env_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(f"Variables de entorno faltantes: {missing_vars}")
        
        # Inicializar el crew según el tipo solicitado
        if crew_type == "basic":
            from crew.basic_content_crew import BasicContentMarketingCrew
            crew = BasicContentMarketingCrew()
        else:
            from crew.content_crew import ContentMarketingCrew
            crew = ContentMarketingCrew()
        
        # Manejar diferentes acciones
        if action == 'health_check':
            response = handle_health_check(crew)
            
        elif action == 'get_status':
            response = handle_get_status(crew)
            
        elif action == 'generate_article':
            response = handle_generate_article(crew, topic, crew_type, format_type)
            
        else:
            response = {
                'success': False,
                'error': f'Acción no reconocida: {action}',
                'available_actions': ['health_check', 'get_status', 'generate_article']
            }
        
        status_code = 200 if response.get('success', False) else 400
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': json.dumps(response, ensure_ascii=False, indent=2)
        }
        
    except Exception as e:
        logger.error(f"Error en lambda_handler: {str(e)}", exc_info=True)
        
        error_response = {
            'success': False,
            'error': 'Error interno del servidor',
            'details': str(e),
            'type': type(e).__name__
        }
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response, ensure_ascii=False)
        }

def handle_health_check(crew: ContentMarketingCrew) -> Dict[str, Any]:
    """Maneja el health check del sistema"""
    try:
        status = crew.get_crew_status()
        
        return {
            'success': True,
            'message': 'Sistema operativo',
            'timestamp': context_timestamp(),
            'status': status,
            'environment': {
                'openai_configured': bool(os.getenv('OPENAI_API_KEY')),
                'serper_configured': bool(os.getenv('SERPER_API_KEY')),
                'lambda_region': os.getenv('AWS_REGION', 'unknown')
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error en health check: {str(e)}'
        }

def handle_get_status(crew: ContentMarketingCrew) -> Dict[str, Any]:
    """Obtiene el estado detallado del crew"""
    try:
        status = crew.get_crew_status()
        
        return {
            'success': True,
            'crew_status': status,
            'configuration': {
                'agents_count': 8,
                'tasks_count': 8,
                'process_type': 'sequential_specialized',
                'specialization': 'academic_quality_article',
                'tools_available': ['web_search', 'content_analyzer'],
                'sections': [
                    'abstract_keywords', 'desarrollo', 'resultados',
                    'discusion', 'conclusiones', 'bibliografia'
                ]
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error obteniendo status: {str(e)}'
        }

def handle_generate_article(crew, topic: str = None, crew_type: str = "basic", format_type: str = "blog") -> Dict[str, Any]:
    """Genera un artículo usando el crew de agentes"""
    try:
        logger.info(f"Iniciando generación de artículo. Tópico: {topic or 'general'}, Crew: {crew_type}, Formato: {format_type}")
        
        # Ejecutar el crew
        if crew_type == "basic":
            result = crew.run_crew(topic=topic, format_type=format_type)
        else:
            result = crew.run_crew(topic=topic)
        
        if result['success']:
            logger.info(f"Artículo generado exitosamente con crew {crew_type}")
            
            article_type = "artículo de blog" if crew_type == "basic" else "artículo académico"
            
            return {
                'success': True,
                'message': f'{article_type.title()} generado exitosamente',
                'timestamp': context_timestamp(),
                'topic': topic or 'Tendencias generales en content marketing',
                'crew_type': crew_type,
                'format_type': format_type,
                'result': result,
                'metadata': {
                    'agents_used': result.get('metadata', {}).get('agents_count', 3),
                    'workflow_type': crew_type,
                    'article_type': article_type,
                    'estimated_length': result.get('metadata', {}).get('output_length', 'Variable'),
                    'execution_time': result.get('metadata', {}).get('estimated_time', 'Variable')
                }
            }
        else:
            logger.error(f"Error generando artículo: {result.get('error')}")
            
            return {
                'success': False,
                'error': 'Error generando artículo',
                'details': result.get('error'),
                'crew_type': crew_type,
                'debug_info': result
            }
            
    except Exception as e:
        logger.error(f"Excepción en handle_generate_article: {str(e)}", exc_info=True)
        
        return {
            'success': False,
            'error': f'Error ejecutando crew: {str(e)}',
            'crew_type': crew_type,
            'type': type(e).__name__
        }

def context_timestamp() -> str:
    """Genera timestamp para respuestas"""
    from datetime import datetime
    return datetime.utcnow().isoformat() + 'Z'

# Para testing local
if __name__ == "__main__":
    # Test event
    test_event = {
        'action': 'generate_article',
        'topic': 'AI en content marketing'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2, ensure_ascii=False))