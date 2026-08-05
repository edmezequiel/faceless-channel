from typing import TypedDict, Annotated, List, Dict, Any
import operator

class AgentState(TypedDict):
    """
    Estado global do Grafo (StateGraph) para a automação Faceless.
    Espelha o schema definido no state.json (Etapa 2).
    Usamos `operator.add` nas listas para que os nós anexem (append) 
    dados em vez de sobrescrever a lista inteira.
    """
    goal: str
    constraints: List[str]
    plan: str
    artifacts: Annotated[List[str], operator.add]
    findings: Annotated[List[str], operator.add]
    memory: Dict[str, Any]
    verification: Dict[str, Any]
    audit_log: Annotated[List[Dict[str, Any]], operator.add]
    model_routing: Dict[str, str]
    research_sources: Annotated[List[Dict[str, str]], operator.add]
    active_agents: Annotated[List[str], operator.add]
    
    # Campo auxiliar para controle de erros ou status do roteamento
    current_status: str
