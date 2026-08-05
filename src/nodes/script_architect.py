from src.core.state import AgentState, ScriptSkeleton
from src.connectors.llm_router import generate_response
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
import logging
import json

logger = logging.getLogger(__name__)

def node_script_architect(state: AgentState) -> AgentState:
    """
    Agente 3 (Esteira): Script Architect
    Desenha o esqueleto lógico e os open loops da narrativa usando parsing rigoroso.
    """
    logger.info("=== Executando Nó: script_architect ===")
    
    factual_context = state.get("factual_context", "")
    goal = state.get("goal", "")
    
    # Parser do LangChain para forçar saída estruturada
    parser = PydanticOutputParser(pydantic_object=ScriptSkeleton)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é o Script Architect especializado no formato INFINITE SCROLL AI VIDEO.
Sua missão é gerar um roteiro de fluxo narrativo contínuo ("Waterfall") sem cortes secos.
Tema: {goal}
Fatos Coletados:
{factual_context}

Regras do Roteiro:
1. NARRATIVA EM CASCATA: Cada batida de roteiro deve se conectar fisicamente com a anterior, como se a câmera estivesse descendo continuamente em uma página web infinita.
2. PACING DE ROLAGEM (scroll_pacing):
   - HERO (Abertura): Apresentação do tema com texto em destaque.
   - FEATURE_PIN (Explicação): Momento onde a velocidade de rolagem desacelera para foco no conceito.
   - SPEED_RAMP_TRANSITION (Transição): Varredura rápida para o próximo módulo visual.
3. KINETIC TEXT OVERLAYS: Para cada batida, forneça uma frase curta e de alto impacto para ser renderizada sobre o vídeo em sincronia com a locução.

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um roteirista analítico especializado em gráficos de retenção (AVD).")
        parsed_skeleton = parser.parse(response)
        skeleton_dict = parsed_skeleton.model_dump()
        logger.info("Script Skeleton gerado e parseado com sucesso via Pydantic.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Architect: {e}")
        # Fallback de segurança se a IA alucinar e não mandar JSON
        skeleton_dict = {
            "beats": ["00:00 - Gancho de emergência", "01:30 - Conflito", "04:00 - Clímax"],
            "open_loops": ["Revelação no final"]
        }
        
    return {"script_skeleton": skeleton_dict, "current_status": "architect_done"}
