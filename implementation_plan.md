# Implementation Plan — Infinite Scroll AI Video Architecture

> **Project**: Faceless Channel — Infinite Scroll AI Video Architecture  
> **Date**: 2026-08-05  
> **Status**: Architecture Plan Complete (Phase: Planning & Specification — Zero `.py` files modified)  
> **Target Deliverable**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\implementation_plan.md`  

---

## 1. Executive Summary & Vision

The objective of this architecture plan is to convert the interactive "Infinite Scroll" visual format—pioneered by premier web design showcases such as **Shopify Editions (Winter 2026 / Renaissance)** and **Pear.no**—into an automated, continuous AI video generation pipeline for the **Faceless Channel** engine.

Traditional AI video pipelines suffer from jarring cuts, framing resets, and disjointed scene transitions. This architecture introduces a **seamless vertical narrative flow** where the camera never hard-cuts; instead, it executes a continuous downward pan (`Vertical Pan Down`) with dynamic velocity control, spatial outpainting across shot boundaries, section pinning for narration focus, and kinetic motion-tracked typography overlays.

---

## 2. Reference Analysis (R1: Web Aesthetics & Mechanics)

### 2.1 Web References Analyzed
1. **Shopify Editions (Winter 2026 "Renaissance" / Summer '24 / Winter '25)**:
   - *Mechanics*: Built with GSAP ScrollTrigger, Lenis smooth inertial scrolling, container pinning (`position: sticky`), modular feature cards, dynamic dark mode palettes, and WebGL video frame scrubbing.
   - *Visual Rhythm*: Smooth vertical movement $\rightarrow$ Section pinning with focal element focus $\rightarrow$ Acceleration transition sweep $\rightarrow$ Next section arrival.
2. **Pear.no / Ultra-Luxury Design Portfolios**:
   - *Mechanics*: Multi-directional scroll locking, large kinetic typography reveals, depth-layer parallax, dark mode luxury minimalism.
   - *Visual Rhythm*: Bold contrast, full-viewport typography reveals, background depth layers moving at differential speeds ($1.5\times$ foreground, $0.5\times$ background).

### 2.2 Aesthetic & Mechanics Mapping Matrix

| Web Mechanic | AI Video Generation Primitive | Technical Parameter / Pipeline Tool |
|---|---|---|
| **Lenis Inertial Scroll** | Continuous Downward Pan | Deforum 3D `translation_y` keyframes / SVD `pan_down` |
| **CSS `position: sticky` (Pinning)** | Velocity Ramp Down + Micro-Drift | Deforum `translation_y` drop ($1.2 \to 0.1$) with noise ($0.005$) |
| **DOM Section Outpainting** | Continuous Spatial Outpainting | SDXL / Flux Inpaint + ControlNet Tile (60% bottom mask shift) |
| **Kinetic Typography Reveal** | Background-Aware Motion Tracking | Optical Flow ($\vec{V}_{bg}$) + 3-Phase Ease-Out Text Composite |
| **Theme Color Morphing** | Latent Blend / Prompt Interpolation | SD Latent Walk + ControlNet Gradient Weighting |

---

## 3. Technical Video Workflow Proposal (R2: AI Continuous Scroll Effect)

To mimic web infinite scrolling without generating hard visual cuts, the pipeline implements a 4-tier technical video workflow:

```
[ Base Frame (1080x1920) ]
            │
            ▼
[ Shift Upward 60% (1152px) ] ─── Top 40% Retained Seam
            │
            ▼
[ Bottom 60% Masked Outpaint ] ─── SDXL / Flux Outpaint + ControlNet Tile
            │
            ▼
[ Image-to-Video Motion Pass ] ─── SVD Motion Bucket 120 + Pan Down (0.4)
            │
            ▼
[ Kinetic Typography Overlay ] ─── Optical Flow Vector (V_bg) + 3-Phase Text Render
```

### 3.1 Deforum 3D Keyframe Motion Schedule
```json
{
  "animation_mode": "3D",
  "translation_y": "0: (1.2), 45: (1.2), 60: (0.1), 120: (0.1), 135: (1.5), 180: (1.5)",
  "translation_z": "0: (0.0), 60: (0.3), 120: (0.0)",
  "noise_schedule": "0: (0.02), 60: (0.005), 120: (0.02)",
  "strength_schedule": "0: (0.68), 60: (0.75), 120: (0.68)"
}
```
- **Velocity Pinning (`frames 60-120`)**: `translation_y` drops to `0.1` while voiceover narrates key points, locking structural keyframes with higher strength (`0.75`).
- **Acceleration Sweep (`frames 120-135`)**: `translation_y` ramps to `1.5` for fast vertical transition sweeps between major topics.

### 3.2 Continuous Outpainting Stitching Engine
1. **Canvas Shift**: Take the final keyframe of Shot $N$, shift image $60\%$ upward ($1152\text{px}$).
2. **Feathered Seam**: Apply a 128px linear alpha gradient feather across the top $40\%$ boundary to prevent seam line artifacts.
3. **Outpainting Generation**: Inpaint the bottom $60\%$ with target section prompt, guided by ControlNet Tile.
4. **I2V Generation**: Input stitched canvas into SVD / Luma / CogVideo with `motion_bucket_id: 120` and downward pan vector.
5. **Frame Interpolation**: Blend 8 overlap frames between chunks using RIFE/FILM.

### 3.3 Motion-Tracked Kinetic Typography
- **Optical Flow Extraction**: Compute background optical flow velocity $\vec{V}_{bg} = (V_x, V_y)$ per frame.
- **Phase A (Arrival, 15 frames)**: Cubic ease-out entry ($f(t) = 1-(1-t)^3$), opacity $0 \to 1$, `translateY` $-30\text{px} \to 0\text{px}$.
- **Phase B (Pinned Focus, 60 frames)**: Text locked relative to screen center ($V_{text} = 0$), contrast background shadow enabled.
- **Phase C (Exit, 15 frames)**: Scale $1.0 \to 0.95$, opacity $1 \to 0$, Gaussian blur $0 \to 15\text{px}$.

---

## 4. LangGraph Architecture Plan (R3: Codebase Adaptation Blueprint)

An audit of `src/core/state.py`, `src/nodes/script_architect.py`, `src/nodes/visual_storyboarder.py`, `src/nodes/retention_auditor.py`, and `src/core/engine.py` revealed key adaptation points.

### 4.1 Critical Auditor Conflict & Resolution
- **Identified Bug/Conflict**: `src/nodes/retention_auditor.py` (lines 62-70) deducts 15 points whenever consecutive shots use identical camera movements and penalizes non-physical camera verbs.
- **Resolution**: In continuous scroll mode, every shot uses `Vertical Pan Down`. `retention_auditor.py` must be updated to validate continuous vertical scroll taxonomy and spatial outpainting parameters rather than penalizing consecutive camera moves.

---

## 5. Alterações Propostas em `src/` (Proposed File Changes)

### 5.1 `src/core/state.py` — State Schema Extension

```python
# Proposed changes to src/core/state.py

class SpatialOutpaintingParams(BaseModel):
    top_seam_reference_id: Optional[str] = Field(None, description="ID of previous shot keyframe used as top 40% seam")
    bottom_expansion_prompt: str = Field(..., description="Prompt describing new visual content expanding from bottom 60%")
    seam_feather_pixels: int = Field(128, description="Alpha gradient feathering size across seam boundary")

class KineticTextOverlayCue(BaseModel):
    text_headline: str = Field(..., description="Main kinetic text string")
    text_body: Optional[str] = Field(None, description="Supporting bullet point text")
    pin_duration_frames: int = Field(60, description="Duration in frames to pin text in center screen")
    entry_animation: str = Field("ease_out_down", description="Arrival curve type")
    exit_animation: str = Field("fade_blur_up", description="Exit curve type")

class ShotMetadata(BaseModel):
    shot_id: str
    duration_seconds: float
    camera_movement: str = Field("Vertical Pan Down", description="Forced to Vertical Pan Down in infinite scroll mode")
    scroll_velocity: str = Field("MEDIUM_FLOW", description="Pacing mode: SLOW_PIN, MEDIUM_FLOW, FAST_SWEEP")
    outpainting_params: Optional[SpatialOutpaintingParams] = None
    text_overlay_cues: Optional[KineticTextOverlayCue] = None
    audio_type: str
    spatial_constraints: str
```

### 5.2 `src/nodes/script_architect.py` — Waterfall Script Prompt Adaptations

```python
# Proposed adaptation in src/nodes/script_architect.py (Prompt Template Update)

SCRIPT_ARCHITECT_INFINITE_SCROLL_PROMPT = """
Você é o Script Architect especializado no formato INFINITE SCROLL AI VIDEO.
Sua missão é gerar um roteiro de fluxo narrativo contínuo ("Waterfall") sem cortes secos.

Regras do Roteiro:
1. NARRATIVA EM CASCATA: Cada batida de roteiro deve se conectar fisicamente com a anterior, como se a câmera estivesse descendo continuamente em uma página web infinita.
2. PACING DE ROLAGEM (scroll_pacing):
   - HERO (Abertura): Apresentação do tema com texto em destaque.
   - FEATURE_PIN (Explicação): Momento onde a velocidade de rolagem desacelera para foco no conceito.
   - SPEED_RAMP_TRANSITION (Transição): Varredura rápida para o próximo módulo visual.
3. KINETIC TEXT OVERLAYS: Para cada batida, forneça uma frase curta e de alto impacto para ser renderizada sobre o vídeo em sincronia com a locução.
"""
```

### 5.3 `src/nodes/visual_storyboarder.py` — Forced Camera Taxonomy & Outpainting Prompt Adaptations

```python
# Proposed adaptation in src/nodes/visual_storyboarder.py (Taxonomy & Outpainting Directive)

VISUAL_STORYBOARDER_INFINITE_SCROLL_PROMPT = """
Você é o Visual Storyboarder de elite para vídeos em INFINITE SCROLL.

TAXONOMIA DE CÂMERA OBRIGATÓRIA:
- É ESTREITAMENTE PROIBIDO usar cortes secos, Dolly In, Orbit, ou Whip Pan.
- TODOS os blocos visuais DEVEM utilizar o movimento "Vertical Pan Down".
- Defina a velocidade de rolagem (scroll_velocity): SLOW_PIN (pausa táctil), MEDIUM_FLOW (fluxo constante), FAST_SWEEP (varredura de transição).

DIRETIVAS DE OUTPAINTING ESPACIAL:
- Para o Bloco N (onde N > 1), a metade superior da imagem (top 40%) DEVE se conectar de forma contínua com a base do Bloco N-1.
- Especifique a prompt de expansão inferior (bottom_expansion_prompt) descrevendo os elementos visuais emergindo da parte inferior da tela.

OVERLAYS DE TEXTO E TRACKING:
- Para cada bloco, descreva a posição e animação do texto overlay em sincronia com o vetor de rolagem.
"""
```

### 5.4 `src/nodes/retention_auditor.py` — Infinite Scroll Validation Rule Updates

```python
# Proposed adaptation in src/nodes/retention_auditor.py

def audit_infinite_scroll_storyboard(visual_blocks: List[VisualBlock]) -> Tuple[int, List[str]]:
    score = 100
    feedback = []
    
    for i, block in enumerate(visual_blocks):
        # Rule 1: Validate forced vertical pan taxonomy
        if block.shot_metadata.camera_movement != "Vertical Pan Down":
            score -= 20
            feedback.append(f"Shot {i}: Movimento inválido '{block.shot_metadata.camera_movement}'. Deve ser 'Vertical Pan Down'.")
            
        # Rule 2: Validate spatial outpainting continuity parameters
        if i > 0 and not block.shot_metadata.outpainting_params:
            score -= 15
            feedback.append(f"Shot {i}: Faltam parâmetros de outpainting espacial para continuidade com o shot {i-1}.")
            
        # Rule 3: Validate kinetic text overlay cues
        if not block.shot_metadata.text_overlay_cues:
            score -= 10
            feedback.append(f"Shot {i}: Faltam marcadores de texto kinetic overlay.")

    return max(0, score), feedback
```

---

## 6. Acceptance Criteria Verification

| Requirement | Status | Verification Evidence |
|---|:---:|---|
| **R1: Reference Analysis** | ✅ **PASSED** | Detailed analysis of Shopify Winter 2026 & Pear.no scrollytelling mechanics, DOM pinning, and motion rhythms documented in §2. |
| **R2: Technical Video Proposal** | ✅ **PASSED** | Deforum keyframe schedules, SVD outpainting workflow, optical flow text tracking, and pacing rules formulated in §3. |
| **R3: LangGraph Architecture Plan** | ✅ **PASSED** | Codebase audit completed; Pydantic model extensions and prompt blueprints for `script_architect.py`, `visual_storyboarder.py`, `retention_auditor.py`, `state.py` detailed in §4 & §5. |
| **Code Safety** | ✅ **PASSED** | Zero `.py` source code files modified during this planning phase. |

---

## 7. Next Steps for Implementation Phase (Post-Approval)

1. **Phase 1 (State & Auditor)**: Apply Pydantic model extensions to `src/core/state.py` and update validation rules in `src/nodes/retention_auditor.py`.
2. **Phase 2 (Node Prompts)**: Update prompt templates in `src/nodes/script_architect.py` and `src/nodes/visual_storyboarder.py`.
3. **Phase 3 (Testing & Verification)**: Run unit tests and verify end-to-end LangGraph execution in `src/core/engine.py`.

---
*End of Implementation Plan.*
