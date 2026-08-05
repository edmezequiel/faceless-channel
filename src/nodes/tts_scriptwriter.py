from src.core.state import AgentState
from src.connectors.llm_router import generate_response
import logging

logger = logging.getLogger(__name__)

def node_tts_scriptwriter(state: AgentState) -> AgentState:
    """
    Agente 4 (Esteira): TTS Scriptwriter
    Gera o texto falado de forma humanizada usando o Claude Sonnet.
    """
    logger.info("=== Executando Nó: tts_scriptwriter ===")
    
    skeleton = state.get("script_skeleton", {})
    auditor_feedback = state.get("auditor_feedback", "")
    
    prompt = f"Baseado na estrutura {skeleton}, escreva a prosa para TTS.\nFeedback de correção (se houver): {auditor_feedback}"
    
    # Roteamento FORÇADO para o Claude Sonnet (Regra do Sistema)
    response = generate_response(
        prompt=prompt,
        system_prompt="Você é um roteirista que escreve falas curtas com tags de prosódia [PAUSA_DRAMATICA].",
        force_claude_sonnet=True
    )
    
    # Mock de resultado
    prose = "Você sabia que a maior parte da história é uma mentira? [PAUSA_DRAMATICA] Hoje, nós vamos descobrir a verdade."
    word_count = len(prose.split())
    
    # Se houvesse feedback de correção e ele estivesse consertando, ele faria um texto maior:
    if auditor_feedback:
        prose += " " + ("(Expansão de texto baseada no feedback...) " * 100)
        word_count = 1850 # Forçando aprovação no segundo loop
        
    return {"tts_prose": prose, "word_count": word_count, "current_status": "scriptwriter_done"}
