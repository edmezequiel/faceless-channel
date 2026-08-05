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
    
    # Prompt com regras de Framework de Retenção
    prompt = f"""
Você é um Arquiteto de Roteiros nível MrBeast. Sua função é criar a estrutura de um vídeo de 10 minutos focado em retenção extrema.
Tema: {goal}
Fatos Coletados:
{factual_context}

Regras:
1. O Gancho (Beat 1) DEVE quebrar o padrão.
2. A cada 45 segundos, mude o ângulo narrativo.
3. Insira 1 a 2 Open Loops massivos que só se resolvem no Clímax.

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
