from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from pydantic import BaseModel, Field

# Modelos Pydantic v2 para estruturar os dados rígidos
class Packaging(BaseModel):
    titles: List[str] = Field(default_factory=list, description="5 títulos com Curiosity Gap")
    thumbnail_concept: str = Field(default="", description="Conceito primário da capa")

class ScriptSkeleton(BaseModel):
    beats: List[str] = Field(default_factory=list, description="Estrutura temporal")
    open_loops: List[str] = Field(default_factory=list, description="Ganchos retidos até o final")

class VisualBlock(BaseModel):
    timestamp_start: str
    timestamp_end: str
    b_roll_description: str
    grokfilm_technique: str

class AgentState(TypedDict):
    """
    Estado global do Grafo (StateGraph) para a automação Faceless (Fase 4.5).
    Incorpora o fluxo de 6 agentes da Esteira de Conteúdo e o Closed-Loop.
    """
    goal: str
    current_status: str
    
    # 1. Pesquisa
    factual_context: str
    
    # 2. Embalagem (Packaging)
    packaging: Dict[str, Any] # Dicionário baseado no BaseModel Packaging
    
    # 3. Arquitetura do Roteiro
    script_skeleton: Dict[str, Any] # Dicionário baseado no BaseModel ScriptSkeleton
    
    # 4. Escrita do Roteiro
    tts_prose: str
    word_count: int
    
    # 5. Visual Storyboard
    visual_blocks: List[Dict[str, Any]] # Lista de BaseModel VisualBlock
    
    # 6. Auditoria (O Guardião)
    retention_score: int
    auditor_feedback: str
    
    # Operações de memória adicionais (append)
    audit_log: Annotated[List[Dict[str, Any]], operator.add]
    research_sources: Annotated[List[Dict[str, str]], operator.add]
    active_agents: Annotated[List[str], operator.add]
