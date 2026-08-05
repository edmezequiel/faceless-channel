from src.core.state import AgentState
from src.connectors.llm_router import generate_response
import logging

logger = logging.getLogger(__name__)

def node_packaging_ctr(state: AgentState) -> AgentState:
    """
    Agente 2 (Esteira): Packaging & CTR
    Gera títulos e conceitos de thumbnail baseados no Curiosity Gap.
    """
    logger.info("=== Executando Nó: packaging_ctr ===")
    
    factual_context = state.get("factual_context", "")
    goal = state.get("goal", "")
    
    prompt = f"Com base neste tema '{goal}' e contexto factual:\n{factual_context}\nCrie 5 títulos polêmicos e um conceito visual de thumbnail."
    
    # Usa o roteador LLM para criar os títulos
    response = generate_response(prompt, system_prompt="Você é um gênio de CTR focado em Curiosity Gap.")
    
    # Mock de extração estruturada
    packaging_data = {
        "titles": [f"Título Curiosity Gap 1 para {goal}", "Título 2", "Título 3", "Título 4", "Título 5"],
        "thumbnail_concept": f"Visual: {response[:50]}..."
    }
    
    return {"packaging": packaging_data, "current_status": "packaging_done"}
