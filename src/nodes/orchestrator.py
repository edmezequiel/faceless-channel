from src.core.state import AgentState
import logging

logger = logging.getLogger(__name__)

def node_orchestrator(state: AgentState) -> AgentState:
    """
    Agente 2: Orchestrator
    Age como o cérebro do LangGraph. Analisa o estado do intake e despacha 
    o trabalho para a Esteira de Conteúdo de 6 Agentes.
    """
    logger.info("=== Executando Nó: orchestrator ===")
    
    status = state.get("current_status", "")
    audit_log = state.get("audit_log", [])
    
    if status == "intake_ok":
        next_route = "researcher"
        log_entry = {"agent": "orchestrator", "action": "Enviando demanda para a Esteira (Researcher)."}
    else:
        next_route = "END"
        log_entry = {"agent": "orchestrator", "action": "Finalizando devido a status não reconhecido."}
        
    logger.info(f"Orquestrador decidiu rotear para: {next_route}")
    
    return {"current_status": f"route_{next_route}", "audit_log": [log_entry]}
