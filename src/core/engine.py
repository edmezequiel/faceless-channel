from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from src.nodes.researcher_fact_checker import node_researcher_fact_checker
from src.nodes.packaging_ctr import node_packaging_ctr
from src.nodes.script_architect import node_script_architect
from src.nodes.tts_scriptwriter import node_tts_scriptwriter
from src.nodes.visual_storyboarder import node_visual_storyboarder
from src.nodes.retention_auditor import node_retention_auditor
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def build_graph():
    """
    Constrói o StateGraph para a Esteira Autônoma de 6 Agentes (Content Factory).
    Implementa o Closed-Loop de retenção.
    """
    builder = StateGraph(AgentState)
    
    # 1. Adiciona os 6 nós da esteira de conteúdo
    builder.add_node("researcher", node_researcher_fact_checker)
    builder.add_node("packaging", node_packaging_ctr)
    builder.add_node("architect", node_script_architect)
    builder.add_node("scriptwriter", node_tts_scriptwriter)
    builder.add_node("storyboarder", node_visual_storyboarder)
    builder.add_node("auditor", node_retention_auditor)
    
    # 2. Define o fluxo de arestas (Edges sequenciais)
    builder.set_entry_point("researcher")
    builder.add_edge("researcher", "packaging")
    builder.add_edge("packaging", "architect")
    builder.add_edge("architect", "scriptwriter")
    builder.add_edge("scriptwriter", "storyboarder")
    builder.add_edge("storyboarder", "auditor")
    
    # 3. O CLOSED-LOOP (Aresta Condicional do Auditor)
    def auditor_router(state: AgentState):
        status = state.get("current_status", "")
        if status == "auditor_failed":
            logger.warning(">>> CLOSED LOOP ATIVADO: Roteiro reprovado (< 85). Voltando para o Scriptwriter.")
            # Volta para o Scriptwriter para corrigir o tamanho/ritmo
            return "scriptwriter" 
        else:
            logger.info(">>> Roteiro APROVADO! Finalizando esteira.")
            return END

    builder.add_conditional_edges(
        "auditor",
        auditor_router,
        {
            "scriptwriter": "scriptwriter",
            END: END
        }
    )
    
    # Compila o grafo
    graph = builder.compile()
    return graph

if __name__ == "__main__":
    logger.info("Iniciando a compilação do Grafo LangGraph (Esteira de 6 Agentes)...")
    graph = build_graph()
    
    # Teste simples (Simulando o input)
    initial_state = {
        "goal": "A História Oculta do Império Romano",
        "current_status": "init",
        "research_sources": []
    }
    
    logger.info("Executando a Esteira Autônoma...")
    for event in graph.stream(initial_state):
        for node_name, state_update in event.items():
            logger.info(f"-- Atualização do Nó [{node_name}] --")
            if "current_status" in state_update:
                logger.info(f"   Status: {state_update['current_status']}")
