import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Cargar variables de entorno
load_dotenv()

def get_llm_config():
    """
    Configura y retorna el modelo de lenguaje a usar
    """
    try:
        # Configuración del modelo OpenAI
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=4000
        )
        return llm
        
    except Exception as e:
        print(f"Error configurando LLM: {str(e)}")
        # Fallback a configuración básica
        return None

def get_api_keys():
    """
    Retorna las claves de API configuradas
    """
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "google_search_api_key": os.getenv("GOOGLE_SEARCH_API_KEY"),
        "google_search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    }

def get_model_config():
    """
    Retorna la configuración del modelo
    """
    return {
        "model_name": os.getenv("MODEL_NAME", "gpt-4"),
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("MAX_TOKENS", "4000")),
        "top_p": float(os.getenv("TOP_P", "1.0")),
        "frequency_penalty": float(os.getenv("FREQUENCY_PENALTY", "0.0")),
        "presence_penalty": float(os.getenv("PRESENCE_PENALTY", "0.0"))
    }

def get_crew_config():
    """
    Retorna la configuración del crew
    """
    return {
        "verbose": os.getenv("CREW_VERBOSE", "True").lower() == "true",
        "process": os.getenv("CREW_PROCESS", "sequential"),
        "max_iterations": int(os.getenv("MAX_ITERATIONS", "3")),
        "memory": os.getenv("ENABLE_MEMORY", "False").lower() == "true"
    }

def get_tools_config():
    """
    Retorna la configuración de las herramientas
    """
    return {
        "web_search_enabled": os.getenv("WEB_SEARCH_ENABLED", "True").lower() == "true",
        "content_analysis_enabled": os.getenv("CONTENT_ANALYSIS_ENABLED", "True").lower() == "true",
        "article_formatting_enabled": os.getenv("ARTICLE_FORMATTING_ENABLED", "True").lower() == "true",
        "max_search_results": int(os.getenv("MAX_SEARCH_RESULTS", "10")),
        "search_timeout": int(os.getenv("SEARCH_TIMEOUT", "30"))
    }

def validate_config():
    """
    Valida que la configuración esté completa
    """
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Por favor, configura estas variables en tu archivo .env")
        return False
    
    print("✅ Configuración validada correctamente")
    return True

def get_logging_config():
    """
    Retorna la configuración de logging
    """
    return {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        "file_enabled": os.getenv("LOG_TO_FILE", "False").lower() == "true",
        "file_path": os.getenv("LOG_FILE_PATH", "crewai.log")
    }
