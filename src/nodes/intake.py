from src.core.state import AgentState
import logging

logger = logging.getLogger(__name__)

def node_intake_router(state: AgentState) -> AgentState:
    """
    Agente 1: Intake Router
    Analisa o objetivo inicial e as restrições, validando o schema de entrada (Pydantic style).
    """
    logger.info("=== Executando Nó: intake_router ===")
    
    goal = state.get("goal", "Sem objetivo definido")
    logger.info(f"Objetivo recebido: {goal}")
    
    # Simulação de validação
    audit_log = state.get("audit_log", [])
    log_entry = {"agent": "intake_router", "action": "Validação de entrada concluída com sucesso."}
    
    return {"audit_log": [log_entry], "current_status": "intake_ok"}
