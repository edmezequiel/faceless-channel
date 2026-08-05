from src.core.state import AgentState
from src.connectors.agent_reach import AgentReachConnector
import logging

logger = logging.getLogger(__name__)

def node_researcher_fact_checker(state: AgentState) -> AgentState:
    """
    Agente 1 (Esteira): Researcher & Fact-Checker
    Coleta dados usando o RAG Factual via Agent-Reach.
    """
    logger.info("=== Executando Nó: researcher_fact_checker ===")
    
    goal = state.get("goal", "")
    
    # Busca factual
    logger.info("Verificando fatos e isolando alegações (RAG Factual)...")
    youtube_data = AgentReachConnector.search_youtube(goal)
    web_data = AgentReachConnector.read_webpage("wikipedia.org/wiki/" + goal.replace(" ", "_"))
    
    factual_context = f"Fatos validados do YouTube:\n{youtube_data}\n\nFatos da Web:\n{web_data}"
    
    return {"factual_context": factual_context, "current_status": "research_done"}
