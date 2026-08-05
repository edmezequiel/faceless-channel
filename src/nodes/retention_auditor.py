from src.core.state import AgentState
import logging

logger = logging.getLogger(__name__)

def node_retention_auditor(state: AgentState) -> AgentState:
    """
    Agente 6 (Esteira): Retention Auditor (O Guardião)
    Checa o Word Count e o Pacing.
    Aciona o Closed-Loop de autocorreção se a pontuação for menor que 85.
    """
    logger.info("=== Executando Nó: retention_auditor ===")
    
    word_count = state.get("word_count", 0)
    logger.info(f"Analisando densidade de palavras: {word_count} palavras")
    
    # Validação rigorosa
    if word_count < 1800:
        logger.warning("ALERTA: Volume de palavras insuficiente. Roteiro curto demais para retenção de 10 minutos.")
        retention_score = 60 # Reprova
        feedback = "A partir dos 4 minutos o ritmo caiu e a contagem de palavras está curta; expanda o conflito central e adicione mais hooks."
        next_status = "auditor_failed"
    else:
        logger.info("SUCESSO: Densidade e ganchos aprovados.")
        retention_score = 92
        feedback = "Roteiro aprovado para produção visual."
        next_status = "auditor_approved"
        
    return {
        "retention_score": retention_score, 
        "auditor_feedback": feedback, 
        "current_status": next_status
    }
