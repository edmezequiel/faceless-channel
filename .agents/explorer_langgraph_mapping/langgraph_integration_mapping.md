# LangGraph Integration Mapping Report: Channel Niche Positioning & SOUL ID Character Bible

> **Module**: Faceless Channel Engine  
> **Milestone**: Milestone 1 — Niche & Persona Architecture  
> **Author**: `teamwork_preview_explorer` (Explorer Subagent)  
> **Target Path**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_langgraph_mapping\langgraph_integration_mapping.md`  
> **Status**: Complete Architecture & Codebase Mapping (Read-Only Phase — 0 `.py` files modified)

---

## 1. Executive Summary & Architecture Overview

This report provides the complete technical integration blueprint for embedding **Channel Niche Positioning** (Scientific Academic Psychology merged with Pop/Dark Psychology) and the **SOUL ID Character Bible** (Dr. Obsidian) into the LangGraph stateful execution engine of the Faceless Channel system.

The audit examined four core system components:
1. `src/core/state.py` — Pydantic v2 schemas and LangGraph `AgentState` TypedDict.
2. `src/nodes/visual_storyboarder.py` — Storyboard generation node, `layer1_identity_token` enforcement, static `SOUL_ID` prompt injection, and visual consistency rules.
3. `src/nodes/tts_scriptwriter.py` — Script generation node, tone of voice control, catchphrase insertion, and 60% Scientific / 40% Pop-Psychology balance.
4. `src/nodes/script_architect.py` — Waterfall narrative structure node and open loop engineering.

All proposed code modifications are designed to be 100% backward compatible with existing node interfaces and dry-run state runner (`workflows/graph_runner.py`).

---

## 2. Codebase Audit Findings

### 2.1 Audit of `src/core/state.py`
- **Current State**: Contains Pydantic models `Packaging`, `ScriptSkeleton`, `SpatialOutpaintingParams`, `KineticTextOverlayCue`, `ShotMetadata`, and `VisualBlock`. The global `AgentState` includes `goal`, `factual_context`, `packaging`, `script_skeleton`, `tts_prose`, `word_count`, `visual_blocks`, `retention_score`, `auditor_feedback`, `audit_log`, `research_sources`, `active_agents`.
- **Gaps Identified**:
  1. No structured representation for the character bible (`SOUL_ID`) or visual anchors.
  2. No representation for channel persona parameters (tone, signature catchphrases, scientific vs. pop-psychology balance).
  3. `VisualBlock` has a `layer1_identity_token` field (defined as `"SOUL ID do personagem sem descritores extras"`), but lacks a default value or schema validation against the character bible.
- **Architectural Solution**: Introduce two new Pydantic v2 models (`CharacterBible` and `ChannelPersonaConfig`) and incorporate `soul_id` and `channel_persona` fields directly into `AgentState`.

### 2.2 Audit of `src/nodes/visual_storyboarder.py`
- **Current State**: Generates `visual_blocks` using `StoryboardResponse` Pydantic parser. Enforces camera taxonomy (`Vertical Pan Down`), scroll velocity, and spatial outpainting parameters in the prompt.
- **Gaps Identified**:
  1. Does not inject `SOUL_ID` visual anchor tokens into system/user prompts.
  2. Does not enforce consistent `layer1_identity_token` generation across all scene prompts where the presenter appears.
  3. Does not enforce global visual style parameters (`art_style_token`) across `layer2_keyframe_prompt`.
- **Architectural Solution**: Update `node_visual_storyboarder` to pull `soul_id` from state, inject static prompts and visual anchor constraints into LLM instructions, and apply post-processing on `visual_blocks` to guarantee `layer1_identity_token` completeness.

### 2.3 Audit of `src/nodes/tts_scriptwriter.py`
- **Current State**: Generates script prose with 80/20 VO/Lip-sync split, AI slop blacklisting, 15-word sentence limit, and prosody tags.
- **Gaps Identified**:
  1. Lacks explicit tone of voice directives (`Clinical, Ominous, Authoritative, Forbidden Knowledge`).
  2. Lacks mandatory signature catchphrases.
  3. Lacks explicit ratio guidelines for 60% Scientific Academic Psychology (CBT, Neuropsychology, Dark Triad) vs 40% Pop/Dark Psychology (Manipulation, Impostor Syndrome, Gaslighting).
- **Architectural Solution**: Update `node_tts_scriptwriter` to pull `channel_persona` from state, dynamically format system & prompt templates, and enforce persona parameters.

### 2.4 Audit of `src/nodes/script_architect.py`
- **Current State**: Generates `script_skeleton` with waterfall beats, scroll pacing, and kinetic text overlay cues.
- **Gaps Identified**: Focuses purely on video scroll mechanics without connecting narrative beats to academic psychological studies or dark psychology hooks.
- **Architectural Solution**: Adapt prompt template to mandate psychological study hooks in the `HERO` phase and dark psychology behavioral triggers in transition beats.

---

## 3. Concrete Code Snippet Proposals

### 3.1 Proposal for `src/core/state.py`

```python
# Location: src/core/state.py (Proposed Update)
from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from pydantic import BaseModel, Field

# ==========================================
# Novos Modelos de Branding e Persona do Canal
# ==========================================

class CharacterBible(BaseModel):
    """
    Bíblia do personagem virtual proprietário (SOUL ID) para garantia de IP anti-cópia.
    """
    character_id: str = Field(default="SOUL_ID_DR_OBSIDIAN", description="ID único do SOUL ID")
    name: str = Field(default="Dr. Obsidian", description="Nome do arquétipo/apresentador virtual")
    archetype: str = Field(default="The Dark Architect / Enigmatic Scholar", description="Arquétipo psicológico")
    static_visual_prompt: str = Field(
        default="enigmatic scholar in dark academia attire, obsidian-trimmed scholar robes, glowing crimson monocle on left eye, silver hair tied back, seated in vintage leather-bound study, background filled with anatomical copper engravings, chiaroscuro dramatic side lighting, dark renaissance aesthetic, pencil hatching texture",
        description="Prompt estático imutável do SOUL ID para geradores T2I/I2V"
    )
    visual_anchors: List[str] = Field(
        default_factory=lambda: [
            "glowing crimson monocle on left eye",
            "obsidian-trimmed scholar robes",
            "vintage leather-bound journal with brass clasps",
            "anatomical copper engraving overlays"
        ],
        description="Âncoras visuais proprietárias anti-cópia"
    )
    art_style_token: str = Field(
        default="dark academia engraving, hyper-detailed ink hatching on aged parchment, dramatic chiaroscuro lighting",
        description="Estilo artístico global do canal"
    )

class ChannelPersonaConfig(BaseModel):
    """
    Configuração do nicho e posicionamento estratégico do canal.
    """
    niche_name: str = Field(default="Scientific Dark Psychology", description="Nicho do canal")
    scientific_balance_pct: int = Field(default=60, description="Percentual de rigor científico/acadêmico (TCC, Neuropsicologia)")
    pop_psych_balance_pct: int = Field(default=40, description="Percentual de gatilhos populares (Dark Psychology, Manipulação)")
    tone_of_voice: str = Field(default="Clinical, Ominous, Authoritative, Forbidden Knowledge", description="Tom de voz da narração")
    signature_catchphrases: List[str] = Field(
        default_factory=lambda: [
            "O cérebro não diferencia a ameaça real do veneno que você aceita degustar...",
            "A neurociência chama isso de viés de confirmação; a sua mente chama de destino...",
            "Nas sombras da psiquiatria aplicada, a verdade raramente é confortável..."
        ],
        description="Bordões e assinaturas narrativas do canal"
    )

# ==========================================
# Modelos Existentes Mantidos e Atualizados
# ==========================================

class Packaging(BaseModel):
    titles: List[str] = Field(default_factory=list, description="5 títulos com Curiosity Gap")
    thumbnail_concept: str = Field(default="", description="Conceito primário da capa")
    color_palette: str = Field(default="", description="Paleta de cores dominante (ex: neon cyberpunk)")

class ScriptSkeleton(BaseModel):
    beats: List[str] = Field(default_factory=list, description="Estrutura temporal")
    open_loops: List[str] = Field(default_factory=list, description="Ganchos retidos até o final")

class SpatialOutpaintingParams(BaseModel):
    top_seam_reference_id: Optional[str] = Field(None, description="ID of previous shot keyframe used as top 40% seam")
    bottom_expansion_prompt: str = Field(description="Prompt describing new visual content expanding from bottom 60%")
    seam_feather_pixels: int = Field(128, description="Alpha gradient feathering size across seam boundary")

class KineticTextOverlayCue(BaseModel):
    text_headline: str = Field(description="Main kinetic text string")
    text_body: Optional[str] = Field(None, description="Supporting bullet point text")
    pin_duration_frames: int = Field(60, description="Duration in frames to pin text in center screen")
    entry_animation: str = Field("ease_out_down", description="Arrival curve type")
    exit_animation: str = Field("fade_blur_up", description="Exit curve type")

class ShotMetadata(BaseModel):
    shot_id: str = Field(description="ID do shot (ex: SC01_SH002)")
    duration_seconds: float = Field(description="Duração do take entre 2.0s e 4.5s")
    camera_movement: str = Field(default="Vertical Pan Down", description="Forçado a Vertical Pan Down em infinite scroll mode")
    scroll_velocity: str = Field(default="MEDIUM_FLOW", description="Pacing mode: SLOW_PIN, MEDIUM_FLOW, FAST_SWEEP")
    outpainting_params: Optional[SpatialOutpaintingParams] = None
    text_overlay_cues: Optional[KineticTextOverlayCue] = None
    audio_type: str = Field(description="Tipo de áudio (voiceover ou lip_sync)")
    spatial_constraints: List[str] = Field(default_factory=list, description="Restrições (ex: keep subject centered)")

class VisualBlock(BaseModel):
    shot_metadata: ShotMetadata
    layer1_identity_token: str = Field(description="SOUL ID do personagem com âncoras (ex: SOUL_ID_DR_OBSIDIAN, glowing crimson monocle)")
    layer2_keyframe_prompt: str = Field(description="Prompt estático T2I de ambiente e iluminação")
    layer3_motion_prompt: str = Field(description="Prompt imperativo I2V de câmera e movimento")

class AgentState(TypedDict):
    """
    Estado global do Grafo (StateGraph) para a automação Faceless.
    """
    goal: str
    current_status: str
    
    # 0. Contexto de Branding & Persona (Injetado)
    soul_id: Dict[str, Any]
    channel_persona: Dict[str, Any]
    
    # 1. Pesquisa
    factual_context: str
    
    # 2. Embalagem (Packaging)
    packaging: Dict[str, Any]
    
    # 3. Arquitetura do Roteiro
    script_skeleton: Dict[str, Any]
    
    # 4. Escrita do Roteiro
    tts_prose: str
    word_count: int
    
    # 5. Visual Storyboard
    visual_blocks: List[Dict[str, Any]]
    
    # 6. Auditoria (O Guardião)
    retention_score: int
    auditor_feedback: str
    
    # Operações de memória adicionais (append)
    audit_log: Annotated[List[Dict[str, Any]], operator.add]
    research_sources: Annotated[List[Dict[str, str]], operator.add]
    active_agents: Annotated[List[str], operator.add]
```

---

### 3.2 Proposal for `src/nodes/visual_storyboarder.py`

```python
# Location: src/nodes/visual_storyboarder.py (Proposed Update)
from src.core.state import AgentState, VisualBlock, CharacterBible
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
    Decompõe o áudio em blocos visuais sincronizados, injetando o SOUL ID e garantindo a consistência estética do canal.
    """
    logger.info("=== Executando Nó: visual_storyboarder ===")
    
    prose = state.get("tts_prose", "")
    soul_id_dict = state.get("soul_id", CharacterBible().model_dump())
    
    if not prose:
        return {"visual_blocks": [], "current_status": "storyboarder_failed"}
        
    soul_token = soul_id_dict.get("character_id", "SOUL_ID_DR_OBSIDIAN")
    static_prompt = soul_id_dict.get("static_visual_prompt", "")
    visual_anchors = ", ".join(soul_id_dict.get("visual_anchors", []))
    art_style = soul_id_dict.get("art_style_token", "dark academia engraving")
    
    parser = PydanticOutputParser(pydantic_object=StoryboardResponse)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é o Visual Storyboarder de elite para vídeos em INFINITE SCROLL com PERSONAGEM RECORRENTE (SOUL ID).

SOUL ID CHARACTER BIBLE INJETADO:
- Token de Identidade (layer1_identity_token): `{soul_token}`
- Prompt Estático da Bíblia: `{static_prompt}`
- Âncoras Visuais Obrigatórias: {visual_anchors}
- Estilo Artístico Global: `{art_style}`

Leia este roteiro de narração:
{prose}

REGRAS DE INJEÇÃO E CONSISTÊNCIA VISUAL:
1. LAYER 1 (IDENTITY TOKEN): O campo `layer1_identity_token` de TODOS os blocos onde o personagem aparece DEVE conter exatamente o token `{soul_token}` acompanhado das âncoras visuais: `{soul_token}, {visual_anchors}`.
2. LAYER 2 (KEYFRAME PROMPT): Todo prompt de ambiente deve obrigatoriamente incluir a tag de estilo `{art_style}` mantendo chiaroscuro dramático e textura de pergaminho/gravura.
3. TAXONOMIA DE CÂMERA OBRIGATÓRIA:
   - É ESTREITAMENTE PROIBIDO usar cortes secos, Dolly In, Orbit, ou Whip Pan.
   - TODOS os blocos visuais DEVEM utilizar o movimento "Vertical Pan Down".
   - Defina a velocidade de rolagem (scroll_velocity): SLOW_PIN (pausa táctil), MEDIUM_FLOW (fluxo constante), FAST_SWEEP (varredura de transição).
4. DIRETIVAS DE OUTPAINTING ESPACIAL:
   - Para o Bloco N (onde N > 1), a metade superior da imagem (top 40%) DEVE se conectar de forma contínua com a base do Bloco N-1.
   - Especifique a prompt de expansão inferior (bottom_expansion_prompt) descrevendo os elementos visuais emergindo da parte inferior da tela.

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um Cinematógrafo Especialista em AI Video e Identidade de Marca.")
        parsed_board = parser.parse(response)
        
        # Pós-processamento para garantia estrita de consistência no layer1_identity_token
        processed_blocks = []
        for block in parsed_board.visual_blocks:
            block_dict = block.model_dump()
            # Garante que o layer1_identity_token incorpore o SOUL_ID oficial se omitido pela LLM
            if soul_token not in block_dict.get("layer1_identity_token", ""):
                block_dict["layer1_identity_token"] = f"{soul_token}, {visual_anchors}"
            processed_blocks.append(block_dict)
            
        visual_blocks = processed_blocks
        logger.info("Visual Blocks gerados com sucesso com SOUL ID injetado.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Storyboarder: {e}")
        visual_blocks = []
    
    return {"visual_blocks": visual_blocks, "current_status": "storyboarder_done"}
```

---

### 3.3 Proposal for `src/nodes/tts_scriptwriter.py`

```python
# Location: src/nodes/tts_scriptwriter.py (Proposed Update)
from src.core.state import AgentState, ChannelPersonaConfig
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
    Gera o texto falado com extrema qualidade (Claude Sonnet), aplicando o tom de voz do canal, bordões e o equilíbrio 60/40 entre Ciência e Pop Psychology.
    """
    logger.info("=== Executando Nó: tts_scriptwriter ===")
    
    skeleton = state.get("script_skeleton", {})
    factual_context = state.get("factual_context", "")
    auditor_feedback = state.get("auditor_feedback", "")
    persona_dict = state.get("channel_persona", ChannelPersonaConfig().model_dump())
    
    tone_of_voice = persona_dict.get("tone_of_voice", "Clinical, Ominous, Authoritative, Forbidden Knowledge")
    catchphrases = "\n- ".join(persona_dict.get("signature_catchphrases", []))
    sci_pct = persona_dict.get("scientific_balance_pct", 60)
    pop_pct = persona_dict.get("pop_psych_balance_pct", 40)
    
    parser = PydanticOutputParser(pydantic_object=TTSResponse)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é um Roteirista de Elite para canais Faceless do YouTube (nível Netflix Documentaries) e a voz oficial do canal.

DIRETIVAS DE BRANDING E PERSONA:
- Tom de Voz Obrigatório: {tone_of_voice}
- Equilíbrio Narrativo: EXACTLY {sci_pct}% Psicologia Científica/Acadêmica (TCC, Neuropsicologia, Tríade Sombria) e {pop_pct}% Pop/Dark Psychology (Gatilhos de manipulação, viés da mente, síndrome do impostor).
- Bordões de Assinatura (Insira ao menos um no momento clímax/abertura):
- {catchphrases}

Sua missão é escrever o roteiro falado baseando-se NESTA ESTRUTURA exata:
{skeleton}

Contexto Factual (Use apenas fatos, sem alucinar):
{factual_context}

FEEDBACK DO AUDITOR (Se estiver reescrevendo, CORRIJA ISSO):
{auditor_feedback if auditor_feedback else "Primeira tentativa. Faça perfeito."}

REGRAS ABSOLUTAS E INQUEBRÁVEIS:
1. DIVISÃO DE ÁUDIO 80/20: Separe o roteiro usando as tags `[VOICEOVER]` (80% do texto para conduzir a narrativa através de planos abertos) e `[LIP_SYNC]` (apenas 20% do texto, restrito a close-ups dramáticos do SOUL ID e confissões diretas para a câmera).
2. EQUILÍBRIO CIÊNCIA vs DARK PSYCHOLOGY: Funda termos como "Córtex Pré-Frontal", "Amígdala Lateral" e "Terapia Cognitivo-Comportamental" com conceitos de alta retenção como "Gatilho de Rejeição", "Efeito Camaleão Sombrio" e "Manipulação Silenciosa".
3. BANIMENTO DE 'AI SLOP': NUNCA use palavras proibidas ("mergulhar", "desvendar", "paisagem", "jornada", "descubra", "vamos explorar", "fascinante", "cativante", "sinfonia").
4. FÔLEGO CURTO: Nenhuma frase pode ter mais que 15 palavras. Use pontos finais constantes.
5. PROSÓDIA OBRIGATÓRIA: Insira marcações teatrais como `[PAUSA_0.5s]`, `[PAUSA_1s]`, `[TOM_MISTERIOSO]`, `[TOM_AGRESSIVO]`, `[ACELERAR]`.

{format_instructions}
    """
    
    try:
        response = generate_response(
            prompt=prompt,
            system_prompt=f"Você é um gênio da escrita persuasiva em psicologia clínica e dark psychology. Seu tom é {tone_of_voice}.",
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
```

---

### 3.4 Proposal for `src/nodes/script_architect.py`

```python
# Location: src/nodes/script_architect.py (Proposed Update)
from src.core.state import AgentState, ScriptSkeleton, ChannelPersonaConfig
from src.connectors.llm_router import generate_response
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
import logging

logger = logging.getLogger(__name__)

def node_script_architect(state: AgentState) -> AgentState:
    """
    Agente 3 (Esteira): Script Architect
    Desenha o esqueleto lógico e os open loops da narrativa unindo rigor acadêmico com hooks de Dark Psychology.
    """
    logger.info("=== Executando Nó: script_architect ===")
    
    factual_context = state.get("factual_context", "")
    goal = state.get("goal", "")
    persona_dict = state.get("channel_persona", ChannelPersonaConfig().model_dump())
    
    parser = PydanticOutputParser(pydantic_object=ScriptSkeleton)
    format_instructions = parser.get_format_instructions()
    
    prompt = f"""
Você é o Script Architect especializado no formato INFINITE SCROLL AI VIDEO para canais de Psicologia & Dark Psychology.
Sua missão é gerar um roteiro de fluxo narrativo contínuo ("Waterfall") alinhado ao posicionamento do canal:
- Nicho: {persona_dict.get('niche_name', 'Scientific Dark Psychology')}
- Proporção: 60% Psicologia Científica Acadêmica / 40% Pop & Dark Psychology.

Tema: {goal}
Fatos Coletados:
{factual_context}

Regras da Arquitetura do Roteiro:
1. NARRATIVA EM CASCATA COM HOOKS PSICOLÓGICOS: Cada batida deve conectar um estudo acadêmico ou mecanismo neuropsicológico a um comportamento de Dark Psychology do cotidiano.
2. OPEN LOOPS ESTRATÉGICOS: Insira ao menos 2 open loops focados em "Mecanismo Oculto da Mente" e "Revelação no Clímax".
3. PACING DE ROLAGEM (scroll_pacing):
   - HERO (Abertura): Gancho chocante unindo estatística/estudo a uma vulnerabilidade psicológica.
   - FEATURE_PIN (Explicação): Pausa tática para dissecção neuropsicológica.
   - SPEED_RAMP_TRANSITION (Transição): Aceleração para o próximo gatilho comportamental.

{format_instructions}
    """
    
    try:
        response = generate_response(prompt, system_prompt="Você é um arquiteto narrativo especializado em retenção e psicologia cognitiva.")
        parsed_skeleton = parser.parse(response)
        skeleton_dict = parsed_skeleton.model_dump()
        logger.info("Script Skeleton gerado e parseado com sucesso via Pydantic.")
    except OutputParserException as e:
        logger.error(f"Falha ao extrair JSON do Architect: {e}")
        skeleton_dict = {
            "beats": ["00:00 - Gancho de emergência", "01:30 - Conflito", "04:00 - Clímax"],
            "open_loops": ["Revelação no final"]
        }
        
    return {"script_skeleton": skeleton_dict, "current_status": "architect_done"}
```

---

## 4. Data Flow & State Lifecycle Analysis

The execution lifecycle of state through the modified nodes is illustrated below:

```
[ Graph Execution Start ]
          │
          ▼
[ State Initialization (state.py) ]
  ├── Inject `soul_id` (CharacterBible defaults)
  └── Inject `channel_persona` (ChannelPersonaConfig defaults)
          │
          ▼
[ node_script_architect ]
  └── Merges factual context with 60% Sci / 40% Pop-Psych rules -> generates `script_skeleton`
          │
          ▼
[ node_tts_scriptwriter ]
  └── Applies `tone_of_voice`, catchphrases, and prosody tags -> generates `tts_prose`
          │
          ▼
[ node_visual_storyboarder ]
  └── Injects `SOUL_ID` static prompt & anchors into `visual_blocks` (Layer 1-3)
          │
          ▼
[ node_retention_auditor ]
  └── Audits narrative rhythm, audio split (80/20), and identity token presence
```

---

## 5. Risk Assessment & Invalidation Conditions

1. **LLM Omission of `layer1_identity_token`**:
   - *Risk*: The LLM might generate generic text in `layer1_identity_token` instead of the rigid `SOUL_ID` token.
   - *Mitigation*: The proposed code for `node_visual_storyboarder` includes deterministic post-processing Python logic (`soul_token not in block_dict["layer1_identity_token"]`) to guarantee fallback injection.

2. **Context Window Expansion**:
   - *Risk*: Injecting character bible and persona prompts increases token count per LLM request.
   - *Mitigation*: The `CharacterBible` and `ChannelPersonaConfig` schemas are lightweight (<300 tokens total), preserving performance under the 8 GB RAM / LiteLLM constraints.

3. **Tone Drift over Extended Scripts**:
   - *Risk*: System might lose clinical/ominous tone during longer script sections.
   - *Mitigation*: The system prompt for `node_tts_scriptwriter` explicitly enforces `force_claude_sonnet=True` and re-injects tone directives per execution.

---

## 6. Verification Method

To verify the integration after code application:
1. Run `python workflows/graph_runner.py --dry-run` to validate `state.json` schema compatibility.
2. Execute node unit test suite for `state.py`, `visual_storyboarder.py`, `tts_scriptwriter.py`, and `script_architect.py`.
3. Inspect generated `visual_blocks` to confirm `layer1_identity_token` contains `SOUL_ID_DR_OBSIDIAN` and required visual anchors.

---
*End of LangGraph Integration Mapping Report.*
