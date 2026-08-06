from litellm import completion
from src.core.config import config
import logging

logger = logging.getLogger(__name__)

# Mapa de especialização: cada agente da esteira tem seu modelo ideal
AGENT_MODEL_MAP = {
    "researcher":    config.RESEARCHER_MODEL,     # gemini-2.0-flash (1M context, gratuito)
    "packaging":     config.PACKAGING_MODEL,       # gpt-4o-mini (rápido, formatação JSON)
    "architect":     config.ARCHITECT_MODEL,        # claude-3-7-sonnet (qualidade narrativa)
    "scriptwriter":  config.SCRIPTWRITER_MODEL,     # claude-3-7-sonnet (anti-AI slop)
    "storyboarder":  config.STORYBOARDER_MODEL,     # gemini-2.0-flash (detalhamento visual)
    "auditor":       config.AUDITOR_MODEL,          # gpt-4o-mini (raciocínio lógico)
}


def generate_response(
    prompt: str,
    system_prompt: str = "Você é um assistente da Automação Faceless.",
    model: str = None,
    agent_role: str = None,
    **kwargs
) -> str:
    """
    Roteador inteligente de LLMs via OmniRoute + LiteLLM.
    
    Hierarquia de seleção de modelo:
      1. force_claude_sonnet / force_scriptwriter → Scriptwriter Model (Anti-AI Slop)
      2. agent_role → Modelo especializado do AGENT_MODEL_MAP
      3. model (argumento explícito) → Modelo escolhido pelo chamador
      4. Fallback → LITELLM_DEFAULT_MODEL (gpt-4o-mini)
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    target_model = None
    
    # 1. Regra de força: Scriptwriter obrigatoriamente usa Claude Sonnet
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        target_model = config.SCRIPTWRITER_MODEL
        logger.info(f"[FORCE] Roteamento forçado para {target_model} (Anti-AI Slop).")
    
    # 2. Roteamento por especialidade de agente
    elif agent_role and agent_role in AGENT_MODEL_MAP:
        target_model = AGENT_MODEL_MAP[agent_role]
        logger.info(f"[AGENT_MAP] Agente '{agent_role}' → Modelo: {target_model}")
    
    # 3. Modelo explícito passado como argumento
    elif model:
        target_model = model
    
    # 4. Fallback padrão
    if not target_model:
        target_model = config.LITELLM_DEFAULT_MODEL
    
    # Formata a chamada OpenAI-compatible para ser processada via OmniRoute proxy
    llm_model_name = target_model if target_model.startswith("openai/") else f"openai/{target_model}"

    try:
        logger.info(f"[OMNIROUTE] Roteando → {target_model} via {config.OMNIROUTE_BASE_URL}")
        response = completion(
            model=llm_model_name,
            messages=messages,
            api_base=config.OMNIROUTE_BASE_URL,
            api_key=config.OMNIROUTE_API_KEY,
            custom_llm_provider="openai"
        )
            
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"[OMNIROUTE] Erro na inferência de {target_model}: {e}")
        return f"ERROR_LLM: {str(e)}"
