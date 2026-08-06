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
    
    # Usa o LLM para isolar fatos
    from src.connectors.llm_router import generate_response
    raw_data = f"YouTube: {youtube_data}\nWeb: {web_data}"
    prompt = f"Analise estes dados sobre '{goal}'. Extraia APENAS fatos comprovados, nomes, datas e eventos, removendo qualquer viés ou desinformação.\n\nDados brutos:\n{raw_data}"
    
    factual_context = generate_response(prompt, system_prompt="Você é um Fact-Checker rigoroso.", agent_role="researcher")
    
    return {"factual_context": factual_context, "current_status": "research_done"}
