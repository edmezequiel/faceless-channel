from src.core.state import AgentState, Packaging
from src.connectors.llm_router import generate_response
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
import logging

logger = logging.getLogger(__name__)

def node_packaging_ctr(state: AgentState) -> AgentState:
    """
    Agente 2 (Esteira): Packaging & CTR
    Gera títulos e conceitos de thumbnail baseados no Curiosity Gap com Pydantic Parser.
    """
    logger.info("=== Executando Nó: packaging_ctr ===")
    
    factual_context = state.get("factual_context", "")
    goal = state.get("goal", "")
    
    parser = PydanticOutputParser(pydantic_object=Packaging)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é um Especialista de Empacotamento (Thumbnails e Títulos) obcecado em Click-Through Rate (CTR).
Sua missão é vender o vídeo antes mesmo dele começar.
Tema: {goal}
Contexto:
{factual_context}

Regras para Títulos:
1. Devem usar a técnica de 'Curiosity Gap' (ex: "Eles esconderam isso por 100 anos").
2. Máximo de 50 caracteres (otimizado para celular).
3. Seja extremo, mas baseado na verdade.

Regras para a Thumbnail:
1. Descreva o conceito com 3 elementos visuais no máximo (Ex: Fundo vermelho escuro, Rosto com expressão de choque, Setas apontando para um detalhe minúsculo).

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um gênio de CTR e Psicologia Humana.")
        parsed_pkg = parser.parse(response)
        packaging_data = parsed_pkg.model_dump()
        logger.info("Packaging gerado e parseado com sucesso via Pydantic.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Packaging: {e}")
        packaging_data = {
            "titles": [f"O segredo chocante sobre {goal}", "A verdade oculta", "Eles mentiram", "O que ninguém te conta", "A revelação final"],
            "thumbnail_concept": "Imagem simples gerando curiosidade."
        }
    
    return {"packaging": packaging_data, "current_status": "packaging_done"}
