from litellm import completion
from src.core.config import config
import logging

logger = logging.getLogger(__name__)

SCRIPTWRITER_WINNING_MODEL = "claude-3-7-sonnet-20250219"

def generate_response(prompt: str, system_prompt: str = "Você é um assistente da Automação Faceless.", model: str = None, **kwargs) -> str:
    """
    Roteador inteligente de LLMs.
    Se a config USE_LOCAL_LLM for verdadeira, força o envio para o Ollama (economia de RAM e custos).
    Caso contrário, ou se houver falha, envia via LiteLLM para nuvem.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    target_model = model
    
    # Regra de Roteamento Específica (Esteira Autônoma - TTS Scriptwriter)
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        target_model = SCRIPTWRITER_WINNING_MODEL
        logger.info("Regra especial: Roteamento forçado para Claude 3.7 Sonnet (Anti-AI Slop).")
    elif config.USE_LOCAL_LLM and target_model is None:
        # Default local fallback (llama3 ou mistral, configurável)
        target_model = "ollama/llama3"
        
    if target_model is None:
        target_model = config.LITELLM_DEFAULT_MODEL

    # Mapeamento Inteligente para OpenRouter quando habilitado
    if config.USE_OPENROUTER or config.OPENROUTER_API_KEY:
        if target_model == "claude-3-7-sonnet-20250219" or "claude-3-7" in target_model.lower():
            target_model = "openrouter/anthropic/claude-3.7-sonnet"
            logger.info("Mapeado automaticamente para OpenRouter: openrouter/anthropic/claude-3.7-sonnet")
        elif not target_model.startswith("ollama/") and not target_model.startswith("openrouter/"):
            target_model = f"openrouter/{target_model}"

    try:
        if target_model.startswith("ollama/"):
            logger.info(f"Roteando requisição para modelo local: {target_model}")
            response = completion(
                model=target_model, 
                messages=messages, 
                api_base=config.OLLAMA_BASE_URL
            )
        else:
            logger.info(f"Roteando requisição para provedor em nuvem (LiteLLM/OpenRouter): {target_model}")
            response = completion(
                model=target_model,
                messages=messages
            )
            
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Erro na inferência do modelo {target_model}: {e}")
        return f"ERROR_LLM: {str(e)}"
