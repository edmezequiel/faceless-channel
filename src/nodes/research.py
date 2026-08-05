from src.core.state import AgentState
from src.connectors.agent_reach import AgentReachConnector
import logging

logger = logging.getLogger(__name__)

def node_research_agent(state: AgentState) -> AgentState:
    """
    Agente 3: Research Agent
    Coleta dados usando o Capability Layer (Agent-Reach, Crawl4AI).
    """
    logger.info("=== Executando Nó: research_agent ===")
    
    goal = state.get("goal", "")
    
    # Simulação da busca (Metodologia SurfSense)
    logger.info("Fase 1: Planejando busca...")
    logger.info("Fase 2: Executando Agent-Reach...")
    
    # Usa o conector que construímos
    youtube_data = AgentReachConnector.search_youtube(goal)
    web_data = AgentReachConnector.read_webpage("wikipedia.org/wiki/Estoicismo")
    
    sources = state.get("research_sources", [])
    sources.append({"source": "YouTube", "data": youtube_data})
    sources.append({"source": "Web", "data": web_data})
    
    findings = state.get("findings", [])
    findings.append(f"[Research] Dados coletados via Agent-Reach para o tópico: {goal}")
    
    return {"research_sources": sources, "findings": findings, "current_status": "research_ok"}
