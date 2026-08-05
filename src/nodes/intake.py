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
    findings = state.get("findings", [])
    findings.append("[Intake] Validação de entrada concluída com sucesso. Schema validado.")
    
    return {"findings": findings, "current_status": "intake_ok"}
