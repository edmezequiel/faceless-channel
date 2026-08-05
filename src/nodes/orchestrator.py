from src.core.state import AgentState
from src.connectors.llm_router import generate_response
import logging

logger = logging.getLogger(__name__)

def node_orchestrator(state: AgentState) -> AgentState:
    """
    Agente 2: Orchestrator
    Age como o cérebro do LangGraph. Analisa o estado atual e decide 
    qual é a próxima transição.
    """
    logger.info("=== Executando Nó: orchestrator ===")
    
    status = state.get("current_status", "")
    plan = state.get("plan", "")
    
    # Lógica simples de transição baseada no status
    if status == "intake_ok":
        next_route = "research_agent"
        plan = "Passo 1: Pesquisar tendências."
    elif status == "research_ok":
        next_route = "cultural_graph_engineer"
        plan = "Passo 2: Desenhar estratégia semiótica."
    else:
        # Padrão para finalizar o fluxo nos testes atuais
        next_route = "END"
        
    logger.info(f"Orquestrador decidiu rotear para: {next_route}")
    
    return {"current_status": f"route_{next_route}", "plan": plan}
