from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
from pydantic import BaseModel, Field

class BrandIdentity(BaseModel):
    channel_name: str = Field(default="PROJETO ARQUÉTIPO", description="Nome da marca registrada do canal")
    character_name: str = Field(default="Dr. Victor Vane (The Obsidian Analyst)", description="Nome do personagem proprietário")
    soul_id_token: str = Field(
        default='[SOUL_ID_DR_OBSIDIAN]: "Dr. Victor Vane, enigmatic 35yo male neuro-psychologist researcher, sharp angular jawline, piercing icy cyan glowing eyes, dark slate side-parted hair with subtle silver temples, wearing a tailored obsidian wool trench coat over a dark turtleneck, obsidian hourglass lapel pin, dramatic chiaroscuro volumetric lighting, deep obsidian black background, cyan neural glow accents, cinematic 85mm lens photo, hyperrealistic, 8k resolution, photorealistic masterwork"',
        description="Prompt estático imutável do personagem"
    )
    opening_hook: str = Field(default="Welcome back to the shadows of the human mind. They tell you your decisions are conscious, but the neuroscience of control proves otherwise. I am Dr. Victor Vane...", description="Bordão de entrada")
    closing_signature: str = Field(default="Mantenha a guarda alta. O inconsciente nunca dorme.", description="Bordão de fecho")

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
    layer1_identity_token: str = Field(description="SOUL ID do personagem sem descritores extras")
    layer2_keyframe_prompt: str = Field(description="Prompt estático T2I de ambiente e iluminação")
    layer3_motion_prompt: str = Field(description="Prompt imperativo I2V de câmera e movimento")

class AgentState(TypedDict):
    """
    Estado global do Grafo (StateGraph) para a automação Faceless (Fase 4.5).
    Incorpora o fluxo de 6 agentes da Esteira de Conteúdo e o Closed-Loop.
    """
    goal: str
    current_status: str
    
    # 0. Identidade de Marca & IP
    brand_identity: Dict[str, Any]
    
    # 1. Pesquisa
    factual_context: str
    
    # 2. Embalagem (Packaging)
    packaging: Dict[str, Any] # Dicionário baseado no BaseModel Packaging
    
    # 3. Arquitetura do Roteiro
    script_skeleton: Dict[str, Any] # Dicionário baseado no BaseModel ScriptSkeleton
    
    # 4. Escrita do Roteiro
    tts_prose: str
    word_count: int
    
    # 5. Visual Storyboard
    visual_blocks: List[Dict[str, Any]] # Lista de BaseModel VisualBlock
    
    # 6. Auditoria (O Guardião)
    retention_score: int
    auditor_feedback: str
    
    # Operações de memória adicionais (append)
    audit_log: Annotated[List[Dict[str, Any]], operator.add]
    research_sources: Annotated[List[Dict[str, str]], operator.add]
    active_agents: Annotated[List[str], operator.add]
