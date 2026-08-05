from src.core.state import AgentState, VisualBlock
from src.connectors.llm_router import generate_response
from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
import logging

logger = logging.getLogger(__name__)

class StoryboardResponse(BaseModel):
    visual_blocks: List[VisualBlock] = Field(description="Lista de blocos visuais sincronizados com o roteiro.")

def node_visual_storyboarder(state: AgentState) -> AgentState:
    """
    Agente 5 (Esteira): Visual Storyboarder
    Decompõe o áudio em blocos visuais sincronizados usando técnicas de roteirização.
    """
    logger.info("=== Executando Nó: visual_storyboarder ===")
    
    prose = state.get("tts_prose", "")
    
    if not prose:
        return {"visual_blocks": [], "current_status": "storyboarder_failed"}
        
    parser = PydanticOutputParser(pydantic_object=StoryboardResponse)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é um Diretor de Arte focado em retenção do YouTube (estilo MrBeast).
Leia este roteiro de narração:
{prose}

Sua tarefa é fatiar esse roteiro em "Blocos Visuais". Para cada bloco de texto, defina:
- O que deve aparecer na tela (b_roll_description).
- Qual técnica de câmera/iluminação usar (grokfilm_technique).

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um Cinematógrafo Especialista em AI Video.")
        parsed_board = parser.parse(response)
        # Convert models to dicts for the state
        visual_blocks = [block.model_dump() for block in parsed_board.visual_blocks]
        logger.info("Visual Blocks gerados com sucesso via Pydantic.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Storyboarder: {e}")
        visual_blocks = []
    
    return {"visual_blocks": visual_blocks, "current_status": "storyboarder_done"}
