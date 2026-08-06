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
Você é o Dr. Victor Vane ("The Obsidian Analyst"), especialista supremo e apresentador do canal 'EDM ARCHETYPE LAB'.
Sua missão é gerar um roteiro de fluxo narrativo contínuo ("Waterfall") no formato INFINITE SCROLL AI VIDEO.
Tema: {goal}
Fatos Coletados:
{factual_context}

DIRETRIZES DE PERSONA & NICHO:
1. FUSÃO DE PSICOLOGIA: Combine conceitos acadêmicos rigorosos (Neuropsicologia, Tríade Sombria, TCC) para explicar fenômenos populares do dia a dia (Gatilhos Emocionais, Relacionamentos Tóxicos, Síndrome do Impostor, Manipulação).
2. PARADOX HOOK (00:00-01:00): A abertura DEVE apresentar um paradoxo fascinante e contraintuitivo sobre a mente humana que desafie o senso comum.
3. IMERSÃO SENSORIAL EM 1ª PESSOA: Inclua obrigatoriamente um Beat de simulação sensorial ("Agora imagine por um segundo como é estar sentado na sala onde um manipulador de elite está presente... sinta a tensão física antes da palavra.").
4. MICRO-TWISTS & INVERSÃO DE EXPECTATIVAS: Use viradas conceituais ("Durante décadas acreditou-se que X era verdade... até que novos exames neurobiológicos provaram que estávamos completamente errados.").
5. NARRATIVA EM CASCATA: Cada batida deve se conectar fisicamente com a anterior, como se estivéssemos descendo por uma página web infinita.
6. PACING DE ROLAGEM (scroll_pacing):
   - HERO (Abertura): Apresentação dramática do tema pelo Dr. Victor Vane.
   - FEATURE_PIN (Explicação): Pausa de velocidade para foco no conceito científico.
   - SPEED_RAMP_TRANSITION (Transição): Varredura rápida para o próximo módulo visual.
7. KINETIC TEXT OVERLAYS: Frases curtas de alto impacto para sincronização com a locução.

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um roteirista analítico especializado em gráficos de retenção (AVD).", agent_role="architect")
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
