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
Você é o Visual Storyboarder de elite para vídeos em INFINITE SCROLL.
Leia este roteiro de narração:
{prose}

TAXONOMIA DE CÂMERA & PERSONAGEM OBRIGATÓRIOS:
- É ESTREITAMENTE PROIBIDO usar cortes secos, Dolly In, Orbit, ou Whip Pan.
- TODOS os blocos visuais DEVEM utilizar o movimento "Vertical Pan Down".
- PERSONAGEM RECORRENTE: Sempre que o apresentador ou narrador aparecer em cena (especialmente nas partes de LIP_SYNC), o `layer1_identity_token` DEVE ser obrigatoriamente `[SOUL_ID_ARCHITECT]`.
- Defina a velocidade de rolagem (scroll_velocity): SLOW_PIN (pausa táctil), MEDIUM_FLOW (fluxo constante), FAST_SWEEP (varredura de transição).

DIRETIVAS DE OUTPAINTING ESPACIAL:
- Para o Bloco N (onde N > 1), a metade superior da imagem (top 40%) DEVE se conectar de forma contínua com a base do Bloco N-1.
- Especifique a prompt de expansão inferior (bottom_expansion_prompt) descrevendo os elementos visuais emergindo da parte inferior da tela.

OVERLAYS DE TEXTO E TRACKING:
- Para cada bloco, descreva a posição e animação do texto overlay em sincronia com o vetor de rolagem.

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
