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
Você é o Dr. Kaelen (O Arquiteto Cognitivo), especialista supremo no canal 'PROJETO ARQUÉTIPO'.
Sua missão é gerar um roteiro de fluxo narrativo contínuo ("Waterfall") no formato INFINITE SCROLL AI VIDEO.
Tema: {goal}
Fatos Coletados:
{factual_context}

DIRETRIZES DE PERSONA & NICHO:
1. FUSÃO DE PSICOLOGIA: Combine conceitos acadêmicos rigorosos (Neuropsicologia, Tríade Sombria, TCC) para explicar fenômenos populares do dia a dia (Gatilhos Emocionais, Relacionamentos Tóxicos, Síndrome do Impostor, Manipulação).
2. NARRATIVA EM CASCATA: Cada batida deve se conectar fisicamente com a anterior, como se estivéssemos descendo por uma página web infinita.
3. PACING DE ROLAGEM (scroll_pacing):
   - HERO (Abertura): Apresentação dramática do tema pelo Arquiteto Cognitivo.
   - FEATURE_PIN (Explicação): Pausa de velocidade para foco no conceito científico.
   - SPEED_RAMP_TRANSITION (Transição): Varredura rápida para o próximo módulo visual.
4. KINETIC TEXT OVERLAYS: Frases curtas de alto impacto para sincronização com a locução.

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
