from litellm import completion
from src.core.config import config
import logging

logger = logging.getLogger(__name__)

SCRIPTWRITER_WINNING_MODEL = config.SCRIPTWRITER_MODEL

def generate_response(prompt: str, system_prompt: str = "Você é um assistente da Automação Faceless.", model: str = None, **kwargs) -> str:
    """
    Roteador inteligente de LLMs via OmniRoute + LiteLLM.
    Todas as requisições são direcionadas estritamente através da API OpenAI-compatible do OmniRoute.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    target_model = model
    
    # Regra de Roteamento Específica (Esteira Autônoma - TTS Scriptwriter / Claude 3.7 Sonnet)
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        target_model = config.SCRIPTWRITER_MODEL
        logger.info(f"Regra especial: Roteamento forçado para {target_model} via OmniRoute (Anti-AI Slop).")
    elif target_model is None:
        target_model = config.LITELLM_DEFAULT_MODEL

    # Formata a chamada OpenAI-compatible para ser processada via OmniRoute proxy
    llm_model_name = target_model if target_model.startswith("openai/") else f"openai/{target_model}"

    try:
        logger.info(f"Roteando requisição via OmniRoute ({config.OMNIROUTE_BASE_URL}): {target_model}")
        response = completion(
            model=llm_model_name,
            messages=messages,
            api_base=config.OMNIROUTE_BASE_URL,
            api_key=config.OMNIROUTE_API_KEY,
            custom_llm_provider="openai"
        )
            
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Erro na inferência do modelo {target_model} via OmniRoute: {e}")
        return f"ERROR_LLM: {str(e)}"
