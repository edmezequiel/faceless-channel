from src.core.state import AgentState
from src.connectors.llm_router import generate_response
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
import logging

logger = logging.getLogger(__name__)

class TTSResponse(BaseModel):
    tts_prose: str = Field(description="O roteiro completo escrito em prosa, formatado para TTS com tags de prosódia.")

def node_tts_scriptwriter(state: AgentState) -> AgentState:
    """
    Agente 4 (Esteira): TTS Scriptwriter (O Coração do Roteiro)
    Gera o texto falado com extrema qualidade (Claude Sonnet), banindo AI Slop.
    """
    logger.info("=== Executando Nó: tts_scriptwriter ===")
    
    skeleton = state.get("script_skeleton", {})
    factual_context = state.get("factual_context", "")
    auditor_feedback = state.get("auditor_feedback", "")
    
    parser = PydanticOutputParser(pydantic_object=TTSResponse)
    format_instructions = parser.get_format_instructions()
    
    # O Prompt Supremo
    prompt = f"""
Você é um Roteirista de Elite para canais Faceless do YouTube (nível Netflix Documentaries).
Sua missão é escrever o roteiro falado baseando-se NESTA ESTRUTURA exata:
{skeleton}

Contexto Factual (Use apenas fatos, sem alucinar):
{factual_context}

FEEDBACK DO AUDITOR (Se estiver reescrevendo, CORRIJA ISSO):
{auditor_feedback if auditor_feedback else "Primeira tentativa. Faça perfeito."}

REGRAS ABSOLUTAS E INQUEBRÁVEIS (O Roteiro será REJEITADO se você violar qualquer uma):
1. PERSONA E BORDÕES PROPRIETÁRIOS DO CANAL 'EDM ARCHETYPE LAB': Escreva com a voz grave, calculista e serena do Dr. Victor Vane ("The Obsidian Analyst"). O vídeo DEVE obrigatoriamente iniciar com a fala: "Welcome back to the shadows of the human mind. They tell you your decisions are conscious, but the neuroscience of control proves otherwise. I am Dr. Victor Vane..." e encerrar com a assinatura: "Mantenha a guarda alta. O inconsciente nunca dorme."
2. DIVISÃO DE ÁUDIO 80/20: Separe o roteiro usando as tags `[VOICEOVER]` (80% do texto para conduzir a narrativa através de planos abertos) e `[LIP_SYNC]` (apenas 20% do texto, restrito a close-ups dramáticos de Dr. Victor Vane).
3. BANIMENTO DE 'AI SLOP' (Lista Negra): NUNCA use as palavras narrativas ("mergulhar", "desvendar", "paisagem", "em um mundo onde", "jornada", "descubra", "vamos explorar", "hoje vamos falar sobre", "fascinante", "cativante", "teia", "intrincado", "testamento", "sinfonia", "dança", "imaginem") e também palavras visuais batidas ("hyperrealistic", "masterpiece", "trending on artstation", "4K", "8K", "oversaturated").
4. FÔLEGO CURTO: Nenhuma frase pode ter mais que 15 palavras. Use pontos finais constantes. O motor de TTS precisa respirar.
5. PROSÓDIA OBRIGATÓRIA: Insira mecanicamente marcações teatrais como `[PAUSA_0.5s]`, `[PAUSA_1s]`, `[TOM_ANALITICO]`, `[TOM_MISTERIOSO]`, `[ACELERAR]` para guiar a voz gerada por IA.

{format_instructions}
    """
    
    try:
        response = generate_response(
            prompt=prompt,
            system_prompt="Você é um gênio da escrita persuasiva focado em ritmo dinâmico. Você odeia jargões genéricos de Inteligência Artificial.",
            force_claude_sonnet=True
        )
        parsed_prose = parser.parse(response)
        prose_text = parsed_prose.tts_prose
        logger.info("Prosa TTS extraída e formatada com sucesso.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Scriptwriter: {e}")
        prose_text = "ERRO NA GERAÇÃO. O sistema falhou ao interpretar o roteiro."
        
    word_count = len(prose_text.split())
    
    return {"tts_prose": prose_text, "word_count": word_count, "current_status": "scriptwriter_done"}
