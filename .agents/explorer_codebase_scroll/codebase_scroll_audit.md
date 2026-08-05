# Codebase Architecture Audit & Infinite Scroll Adaptation Specification

**Project:** Infinite Scroll AI Video Architecture  
**Agent:** `explorer_codebase_scroll`  
**Date:** 2026-08-05  
**Target Files Analyzed:**
- `src/core/state.py`
- `src/core/engine.py`
- `src/nodes/script_architect.py`
- `src/nodes/visual_storyboarder.py`
- `src/nodes/tts_scriptwriter.py`
- `src/nodes/retention_auditor.py`

---

## 1. Executive Summary

This document presents a comprehensive audit of the current Faceless Channel AI Video pipeline (`src/`) and formulates exact technical adaptation requirements to transition the architecture from traditional discrete multi-shot video generation to an **uninterrupted continuous vertical scroll narrative** (inspired by modern high-end interactive websites such as *Shopify Winter 2026* and *Pear.no*).

In the current architecture, the camera taxonomy forces discrete shot switches (e.g., Dolly In, Whip Pan Left) and explicitly penalizes identical camera movements in consecutive shots. To achieve a true "Infinite Scroll" video where the camera never cuts but continuously scrolls downward:
1. **State models** (`src/core/state.py`) must be extended with vertical scroll parameters, spatial outpainting directives, top/bottom seam anchors, and motion-tracked text overlay metadata.
2. **Script Architect** (`src/nodes/script_architect.py`) must structure narrative beats as cascading "Waterfall" reveals tailored for continuous downward visual movement.
3. **Visual Storyboarder** (`src/nodes/visual_storyboarder.py`) must enforce a forced camera taxonomy (`Vertical Pan Down`, continuous downward dolly/tilt) and inject spatial outpainting / seamless edge-matching prompts.
4. **Retention Auditor** (`src/nodes/retention_auditor.py`) must update its visual checks to permit and enforce continuous vertical pan cadence rather than penalizing consecutive identical camera movements.

---

## 2. Audit of Existing Codebase

### 2.1 State Schemas (`src/core/state.py`)

The pipeline relies on Pydantic v2 models and a LangGraph `AgentState` dictionary.

- **`ShotMetadata`** (lines 15–20):
  ```python
  class ShotMetadata(BaseModel):
      shot_id: str = Field(description="ID do shot (ex: SC01_SH002)")
      duration_seconds: float = Field(description="Duração do take entre 2.0s e 4.5s")
      camera_movement: str = Field(description="Taxonomia de câmera (ex: Dolly In, Whip Pan)")
      audio_type: str = Field(description="Tipo de áudio (voiceover ou lip_sync)")
      spatial_constraints: List[str] = Field(default_factory=list, description="Restrições (ex: keep subject centered)")
  ```
  *Audit Finding:* `ShotMetadata` models isolated, discrete camera moves without spatial continuity concepts. There are no fields for scroll direction, scroll velocity, seam placement, outpainting reference boundaries, or text overlay positioning.

- **`VisualBlock`** (lines 22–26):
  ```python
  class VisualBlock(BaseModel):
      shot_metadata: ShotMetadata
      layer1_identity_token: str = Field(description="SOUL ID do personagem sem descritores extras")
      layer2_keyframe_prompt: str = Field(description="Prompt estático T2I de ambiente e iluminação")
      layer3_motion_prompt: str = Field(description="Prompt imperativo I2V de câmera e movimento")
  ```
  *Audit Finding:* Implements a 3-layer architecture (`layer1_identity_token`, `layer2_keyframe_prompt`, `layer3_motion_prompt`). However, it lacks spatial outpainting cues (linking frame N's bottom edge with frame N+1's top edge) and kinetic text tracking specifications.

- **`AgentState`** (lines 28–60):
  ```python
  class AgentState(TypedDict):
      goal: str
      current_status: str
      factual_context: str
      packaging: Dict[str, Any]
      script_skeleton: Dict[str, Any]
      tts_prose: str
      word_count: int
      visual_blocks: List[Dict[str, Any]]
      retention_score: int
      auditor_feedback: str
      audit_log: Annotated[List[Dict[str, Any]], operator.add]
      research_sources: Annotated[List[Dict[str, str]], operator.add]
      active_agents: Annotated[List[str], operator.add]
  ```
  *Audit Finding:* Holds global graph execution state. `visual_blocks` stores serialized `VisualBlock` dicts.

### 2.2 LangGraph Workflow Engine (`src/core/engine.py`)

- **Topology** (lines 21–67):
  `intake` $\rightarrow$ `orchestrator` $\rightarrow$ `researcher` $\rightarrow$ `packaging` $\rightarrow$ `architect` $\rightarrow$ `scriptwriter` $\rightarrow$ `storyboarder` $\rightarrow$ `auditor`.
- **Closed Loop**: `auditor` routes back to `scriptwriter` if `retention_score < 85`.
- *Audit Finding:* The node chain is modular and clean. Transitioning to continuous scroll requires updating the prompt schemas and auditor rules within the existing node graph structure without breaking engine topology.

### 2.3 Script Architect (`src/nodes/script_architect.py`)

- **Function**: `node_script_architect(state: AgentState)` (lines 10–54)
- **Prompt Structure** (lines 25–38):
  - Theme & factual context injection.
  - Enforces MrBeast-style 10-minute script breakdown.
  - Beat 1: "2-Second Hook".
  - Shot timing: 2.0s to 4.5s max to prevent AI morphing fatigue.
  - Open loops: 1–2 open loops resolved at climax.
- *Audit Finding:* Script beats are generated assuming independent discrete scenes. For an infinite scroll, script beats must align with continuous downward visual visual reveals (narration entering sync with elements scrolling from the bottom).

### 2.4 Visual Storyboarder (`src/nodes/visual_storyboarder.py`)

- **Function**: `node_visual_storyboarder(state: AgentState)` (lines 14–56)
- **Prompt Structure** (lines 29–43):
  - Divides TTS script (`tts_prose`) into visual blocks using 3-layer architecture.
  - Defines `camera_movement` using discrete physical camera movements: `Dolly In`, `Whip Pan Left`, `Orbit 360°`, `Truck Right`.
  - **Cadence Rule (Line 40)**: `REGRA DE CADÊNCIA DE ENQUADRAMENTO: Proibido repetir enquadramentos consecutivos (ex: Close-Up seguido de Close-Up é proibido). Alterne entre Close-Up, Medium e Wide.`
- *Audit Finding:* This rule directly contradicts an infinite scroll. In an infinite scroll, camera motion is intentionally continuous and uniform (`Vertical Pan Down`).

### 2.5 Retention Auditor (`src/nodes/retention_auditor.py`)

- **Function**: `node_retention_auditor(state: AgentState)` (lines 7–91)
- **Cadence Conflict** (lines 62–70):
  ```python
  for i in range(1, len(visual_blocks)):
      prev_cam = visual_blocks[i-1].get("shot_metadata", {}).get("camera_movement", "").lower()
      curr_cam = visual_blocks[i].get("shot_metadata", {}).get("camera_movement", "").lower()
      if prev_cam and curr_cam and prev_cam == curr_cam:
          score -= 15
          feedback_notes.append(f"Cadência visual repetitiva detectada no shot {i}. Movimento '{curr_cam}' usado consecutivamente.")
          break
  ```
- *Audit Finding:* If `visual_storyboarder` outputs `Vertical Pan Down` for all shots (as required by infinite scroll), `retention_auditor` will flag it as repetitive, subtract 15 points, and force a retry loop!

---

## 3. Analysis of Camera Taxonomy, Continuity, and Prompt Generation

| Category | Current Implementation | Infinite Scroll Requirements |
|---|---|---|
| **Camera Taxonomy** | Physical discrete camera moves (`Dolly In`, `Whip Pan Left`, `Orbit 360°`, `Truck Right`). | Forced Vertical Scroll Taxonomy (`Vertical Pan Down (Constant)`, `Downward Tilt-Dolly`, `Fast Downward Whip Scroll`, `Pause & Vertical Pan`). |
| **Shot-to-Shot Continuity** | Hard cuts with alternating framing sizes (CU, Med, Wide). | Seamless spatial continuity (Bottom edge of Block $N$ outpaints into Top edge of Block $N+1$). |
| **Prompt Schemas** | Static keyframe + motion prompt without boundary coupling. | Keyframe prompt includes top-edge seam anchor reference; motion prompt includes steady vertical downward scroll vector. |
| **Auditor Validation** | Penalizes consecutive identical camera movements. | Requires and validates vertical downward camera vectors across all storyboard blocks. |
| **Text & UI Layers** | Audio-visual focus; no text overlay metadata. | Explicit kinetic text overlay cues, motion tracking anchors, and scroll velocity alignment. |

---

## 4. Technical Adaptation Requirements for Continuous Vertical Scroll Narrative

### 4.1 Narrative & Beat Structuring (`script_architect.py`)

1. **Waterfall Narrative Rhythm**:
   - The script must be structured as a uninterrupted downward journey.
   - Beats must follow a "cascade" model: as one concept scrolls out at the top of the frame, the next concept is introduced at the bottom.
   - Elimination of abrupt scene transitions in favor of continuous spatial progression transitions (e.g. descending from sky $\rightarrow$ skyscraper top $\rightarrow$ building interior $\rightarrow$ underground vault $\rightarrow$ core).
2. **Text Overlay Cues**:
   - `ScriptSkeleton` should output `on_screen_text_headers` aligned with each beat to support kinetic web-style text overlays.

### 4.2 Forced Camera Taxonomy & Spatial Outpainting (`visual_storyboarder.py`)

1. **Forced Camera Taxonomy**:
   - Restrict allowed camera movements in `shot_metadata` to the Vertical Scroll Taxonomy:
     - `Vertical Pan Down (Standard 1.0x)`: Steady downward scroll.
     - `Vertical Pan Down (Fast Scroll 2.0x)`: High-speed section transition.
     - `Downward Tilt-Dolly`: Tilting down while moving inward vertically.
     - `Scroll Pause & Reveal`: Momentary slow pan/pause on key asset before resuming downward scroll.
2. **Spatial Outpainting Cues (Layer 2 & 3 Prompts)**:
   - `layer2_keyframe_prompt`: Must include top-edge seam alignment directives:
     - *"Continuous vertical panoramic canvas, top boundary seamlessly connects to bottom edge of [PREVIOUS_BLOCK_DESCRIPTOR], lower region expands into [NEW_ENVIRONMENT_DESCRIPTOR], unified vertical color palette."*
   - `layer3_motion_prompt`: Must enforce continuous downward motion:
     - *"Smooth uninterrupted downward camera motion, steady 60fps downward vertical pan, elements scroll upwards as camera moves down."*
3. **Text Overlay & Motion Tracking Representation**:
   - Storyboard output must include `text_overlay_cues` with parameters:
     - `text_content`: Text string to display.
     - `tracking_anchor`: E.g. `scroll_relative` (moves at camera speed), `pinned_element` (locked to visual subject), `header_reveal` (fades in as section enters from bottom).
     - `typography_style`: Minimalist web, kinetic bold, translucent frosted panel.

### 4.3 Auditor Rule Re-alignment (`retention_auditor.py`)

1. **Scroll Taxonomy Enforcement**:
   - Remove check penalizing identical consecutive camera moves.
   - Replace with validation ensuring `camera_movement` contains valid downward scroll keywords (`vertical pan down`, `downward dolly`, `downward tilt`, `vertical scroll`).
2. **Outpainting Keyframe Audit**:
   - Verify that `layer2_keyframe_prompt` contains spatial outpainting descriptors (`top boundary`, `seamless connection`, `vertical canvas`, `expanding downward`).

---

## 5. Detailed Change Mapping Table

Below is the complete mapping of functions, classes, prompt templates, and state fields that require modification during implementation.

```
====================================================================================================
FILE                             COMPONENT TYPE     NAME                          LINE RANGE (APPROX)
====================================================================================================
src/core/state.py                Pydantic Model     ShotMetadata                  Lines 15-20
                                 Modification: Add `scroll_vector` (dict), `outpainting_params` (dict),
                                 `text_overlay_cues` (list). Update `camera_movement` description.

src/core/state.py                Pydantic Model     VisualBlock                   Lines 22-26
                                 Modification: Add `top_seam_anchor` (str), `bottom_reveal_prompt` (str),
                                 and `text_overlay_cues` (list of dicts).

src/core/state.py                Pydantic Model     ScriptSkeleton                Lines 11-14
                                 Modification: Add `waterfall_beats` and `on_screen_text_headers`.

src/nodes/script_architect.py    Prompt Template    `prompt` string               Lines 25-38
                                 Modification: Replace discrete shot beats with Waterfall continuous
                                 scroll narrative rules; enforce continuous visual progression.

src/nodes/script_architect.py    Function           `node_script_architect`       Lines 10-54
                                 Modification: Process expanded `ScriptSkeleton` parser instructions
                                 and update fallback skeleton dict.

src/nodes/visual_storyboarder.py Pydantic Model     StoryboardResponse            Lines 11-12
                                 Modification: Ensure wrapper handles extended `VisualBlock` schema.

src/nodes/visual_storyboarder.py Prompt Template    `prompt` string               Lines 29-43
                                 Modification: Force Vertical Pan Down taxonomy; remove no-consecutive-CU
                                 framing rule; add outpainting seam instructions & text tracking metadata.

src/nodes/visual_storyboarder.py Function           `node_visual_storyboarder`     Lines 14-56
                                 Modification: Pass previous block's bottom context into prompt for
                                 block-to-block outpainting coupling.

src/nodes/retention_auditor.py   Function           `node_retention_auditor`       Lines 62-76
                                 Modification: Replace duplicate camera move penalty with Vertical
                                 Scroll Taxonomy validation & spatial outpainting keyword verification.
====================================================================================================
```

---

## 6. Proposed Code Patch Blueprint (Reference Only — No Code Edited)

### 6.1 `src/core/state.py` Proposed Blueprint
```python
# Proposed additions to state.py
class TextOverlayCue(BaseModel):
    text: str = Field(description="Texto para sobreposição na tela")
    tracking_anchor: str = Field(description="Âncora de movimento (ex: scroll_relative, pinned_element)")
    entry_y_position: str = Field(default="bottom", description="Posição de entrada no canvas (bottom)")

class OutpaintingParams(BaseModel):
    spatial_direction: str = Field(default="bottom_expansion")
    top_boundary_reference: str = Field(description="Referência da borda inferior do bloco anterior")
    overlap_ratio: float = Field(default=0.20, description="Taxa de sobreposição e mesclagem (20%)")

class ShotMetadata(BaseModel):
    shot_id: str = Field(description="ID do shot (ex: SC01_SH002)")
    duration_seconds: float = Field(description="Duração do take entre 2.0s e 4.5s")
    camera_movement: str = Field(description="Taxonomia de Scroll Vertical: Vertical Pan Down, Downward Tilt-Dolly, Fast Downward Scroll")
    audio_type: str = Field(description="Tipo de áudio (voiceover)")
    spatial_constraints: List[str] = Field(default_factory=list)
    outpainting_params: Optional[OutpaintingParams] = None

class VisualBlock(BaseModel):
    shot_metadata: ShotMetadata
    layer1_identity_token: str
    layer2_keyframe_prompt: str  # Inclui instruções de outpainting e seam matching no topo
    layer3_motion_prompt: str    # Inclui movimento imperativo contínuo para baixo
    text_overlay_cues: List[TextOverlayCue] = Field(default_factory=list)
```

### 6.2 `src/nodes/visual_storyboarder.py` Proposed Prompt Blueprint
```text
Você é um Diretor de Arte focado na estética INFINITE SCROLL (estilo Shopify Winter 2026 / Pear.no).
A câmera NUNCA corta ou troca de ângulo lateral. A câmera realiza um MOVIMENTO VERTICAL CONTÍNUO PARA BAIXO (Vertical Pan Down).

Para cada bloco de roteiro, defina:
- camera_movement: Escolha OBRIGATORIAMENTE entre: ['Vertical Pan Down (Standard)', 'Vertical Pan Down (Fast Scroll)', 'Downward Tilt-Dolly', 'Pause & Vertical Pan Down'].
- layer2_keyframe_prompt: Descreva o ambiente como um canvas panorâmico vertical. A borda SUPERIOR DEVE conectar perfeitamente à borda inferior do bloco anterior. A região INFERIOR revela o novo elemento visual.
- layer3_motion_prompt: Comando imperativo de movimento contínuo para baixo (ex: "Smooth steady downward vertical pan, 60fps downward scroll vector").
- text_overlay_cues: Texto de apoio visual que rola junto com o canvas.
```

---

## 7. Verification & Invalidation Protocol

1. **Independent Inspection**: Verify line numbers and existing implementations in `src/core/state.py`, `src/nodes/script_architect.py`, `src/nodes/visual_storyboarder.py`, and `src/nodes/retention_auditor.py`.
2. **Schema Invalidation Condition**: If `retention_auditor.py` is not updated to remove lines 67–70 (repetitive camera movement check), any run of `visual_storyboarder.py` generating infinite vertical scroll blocks will fail auditor validation.
3. **Execution Safety**: Confirm no `.py` source files were modified during this exploration phase.

---
*End of Codebase Scroll Audit Report.*
