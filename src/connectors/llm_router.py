from litellm import completion
from src.core.config import config
import logging

import os

logger = logging.getLogger(__name__)

SCRIPTWRITER_WINNING_MODEL_DIRECT = "claude-3-7-sonnet-20250219"
SCRIPTWRITER_WINNING_MODEL_OPENROUTER = "openrouter/anthropic/claude-3.7-sonnet"

def generate_response(prompt: str, system_prompt: str = "Você é um assistente da Automação Faceless.", model: str = None, **kwargs) -> str:
    """
    Roteador inteligente de LLMs com suporte nativo ao OpenRouter.
    Se USE_OPENROUTER estiver ativo ou OPENROUTER_API_KEY configurada,
    mapeia automaticamente chamadas da nuvem via OpenRouter.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    target_model = model
    use_openrouter = config.USE_OPENROUTER or bool(os.getenv("OPENROUTER_API_KEY"))
    
    # Regra de Roteamento Específica (Esteira Autônoma - TTS Scriptwriter)
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        if use_openrouter:
            target_model = SCRIPTWRITER_WINNING_MODEL_OPENROUTER
            logger.info("Roteamento Especial: Claude 3.7 Sonnet via OpenRouter (openrouter/anthropic/claude-3.7-sonnet).")
        else:
            target_model = SCRIPTWRITER_WINNING_MODEL_DIRECT
            logger.info("Roteamento Especial: Claude 3.7 Sonnet direto via Anthropic API.")
    elif config.USE_LOCAL_LLM and target_model is None:
        # Default local fallback (llama3 ou mistral)
        target_model = "ollama/llama3"
    elif target_model is None:
        target_model = config.LITELLM_DEFAULT_MODEL
        if use_openrouter and not target_model.startswith("openrouter/") and not target_model.startswith("ollama/"):
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
            logger.info(f"Roteando requisição para provedor em nuvem (LiteLLM): {target_model}")
            response = completion(
                model=target_model,
                messages=messages
            )
            
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Erro na inferência do modelo {target_model}: {e}")
        return f"ERROR_LLM: {str(e)}"
