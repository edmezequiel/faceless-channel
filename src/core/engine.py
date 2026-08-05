from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from src.nodes.intake import node_intake_router
from src.nodes.orchestrator import node_orchestrator
from src.nodes.research import node_research_agent
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def build_graph():
    """
    Constrói o StateGraph mapeando os nós e arestas baseados no main_graph.json
    """
    builder = StateGraph(AgentState)
    
    # 1. Adiciona os nós
    builder.add_node("intake_router", node_intake_router)
    builder.add_node("orchestrator", node_orchestrator)
    builder.add_node("research_agent", node_research_agent)
    
    # Nós stub (apenas para teste de compilação por enquanto)
    def dummy_node(state): 
        return {"current_status": "done"}
        
    builder.add_node("cultural_graph_engineer", dummy_node)
    
    # 2. Define o fluxo de arestas (Edges)
    builder.set_entry_point("intake_router")
    
    # O intake sempre vai para o orquestrador
    builder.add_edge("intake_router", "orchestrator")
    
    # O orquestrador tem arestas condicionais baseadas no state["current_status"]
    def orchestrator_router(state: AgentState):
        status = state.get("current_status", "")
        if status == "route_research_agent":
            return "research_agent"
        elif status == "route_cultural_graph_engineer":
            return "cultural_graph_engineer"
        return END

    builder.add_conditional_edges(
        "orchestrator",
        orchestrator_router,
        {
            "research_agent": "research_agent",
            "cultural_graph_engineer": "cultural_graph_engineer",
            END: END
        }
    )
    
    # O research_agent retorna ao orquestrador (ou vai pro próximo)
    # Segundo nosso JSON, research -> cultural_graph_engineer, mas para manter
    # o orchestrator no controle, a gente pode rotear de volta para o orchestrator.
    # Seguiremos o JSON original: research -> cultural_graph_engineer
    builder.add_edge("research_agent", "orchestrator")
    
    # Finaliza no dummy
    builder.add_edge("cultural_graph_engineer", END)
    
    # Compila o grafo
    graph = builder.compile()
    return graph

if __name__ == "__main__":
    logger.info("Iniciando a compilação do Grafo LangGraph...")
    graph = build_graph()
    
    # Teste simples
    initial_state = {
        "goal": "Criar canal sobre Estoicismo",
        "findings": [],
        "research_sources": []
    }
    
    logger.info("Executando o fluxo inicial do grafo...")
    # O stream permite iterar por cada nó executado
    for event in graph.stream(initial_state):
        for node_name, state_update in event.items():
            logger.info(f"-- Atualização do Nó [{node_name}] --")
            if "current_status" in state_update:
                logger.info(f"   Status: {state_update['current_status']}")
