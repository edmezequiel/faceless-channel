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

Regras para a Thumbnail & Estética:
1. Descreva o conceito com 3 elementos visuais no máximo (Ex: Fundo vermelho escuro, Rosto de choque, Setas).
2. A Thumbnail DEVE usar a lógica do "Keyframe Hero Frame" (Foco absoluto estático e super contraste).
3. Defina a `color_palette` dominante que vai ditar toda a direção de arte do vídeo (ex: "neon_cyberpunk", "desaturated_monochrome").

{format_instructions}
    """
    
    COMPLIANCE_DISCLAIMER = (
        "⚠️ AVISO DE CONTEÚDO SINTÉTICO/IA:\n"
        "Este vídeo utiliza representações visuais cinematográficas e sintetização de voz geradas por inteligência artificial "
        "para ilustrar conceitos educacionais de psicologia.\n\n"
        "ISENÇÃO DE RESPONSABILIDADE MÉDICA/LEGAL:\n"
        "O conteúdo apresentado pelo Dr. Victor Vane e EDM ARCHETYPE LAB destina-se exclusivamente a fins educativos, analíticos e de entretenimento. "
        "Não substitui o diagnóstico ou tratamento psicológico/psiquiátrico profissional."
    )

    try:
        response = generate_response(prompt, system_prompt="Você é um gênio de CTR e Psicologia Humana.", agent_role="packaging")
        parsed_pkg = parser.parse(response)
        packaging_data = parsed_pkg.model_dump()
        packaging_data["compliance_disclaimer"] = COMPLIANCE_DISCLAIMER
        if not packaging_data.get("description"):
            packaging_data["description"] = f"{goal}\n\nAnálise comportamental detalhada por Dr. Victor Vane.\n\n{COMPLIANCE_DISCLAIMER}"
        logger.info("Packaging gerado e parseado com sucesso via Pydantic com regras de compliance.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Packaging: {e}")
        packaging_data = {
            "titles": [f"O segredo chocante sobre {goal}", "A verdade oculta", "Eles mentiram", "O que ninguém te conta", "A revelação final"],
            "thumbnail_concept": "Imagem simples gerando curiosidade.",
            "color_palette": "obsidian_cyan",
            "description": f"{goal}\n\n{COMPLIANCE_DISCLAIMER}",
            "compliance_disclaimer": COMPLIANCE_DISCLAIMER
        }
    
    return {"packaging": packaging_data, "current_status": "packaging_done"}
