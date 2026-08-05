# Handoff Report: LangGraph Integration Mapping for Niche & Persona Architecture

> **Agent**: `teamwork_preview_explorer` (Explorer Subagent)  
> **Working Directory**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_langgraph_mapping`  
> **Handoff Type**: Hard (Task Complete)  
> **Deliverable Report**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_langgraph_mapping\langgraph_integration_mapping.md`

---

## 1. Observation

Direct code observations from `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL`:
- **`src/core/state.py`**: Lines 37–42 define `VisualBlock` with `layer1_identity_token: str = Field(description="SOUL ID do personagem sem descritores extras")`. Lines 43–75 define `AgentState` (TypedDict) with fields `goal`, `current_status`, `factual_context`, `packaging`, `script_skeleton`, `tts_prose`, `word_count`, `visual_blocks`, `retention_score`, `auditor_feedback`, `audit_log`, `research_sources`, `active_agents`. Neither `CharacterBible` nor `ChannelPersonaConfig` exist in state models.
- **`src/nodes/visual_storyboarder.py`**: Lines 29–47 construct LLM prompt forcing `Vertical Pan Down` camera taxonomy, outpainting, and text overlays, but do not inject static character prompts or validate `layer1_identity_token` against a character bible.
- **`src/nodes/tts_scriptwriter.py`**: Lines 28–47 construct LLM prompt forcing 80/20 VO/Lip-sync split, AI slop blacklisting, 15-word breath limit, and prosody tags, but lack explicit persona tone guidelines, mandatory catchphrases, or 60/40 scientific/pop-psychology balance rules.
- **`src/nodes/script_architect.py`**: Lines 24–40 construct narrative beats prompt for infinite scroll, but lack integration of academic psychology studies fused with dark psychology retention hooks.
- **Code modification status**: Zero `.py` files modified (100% read-only compliance).

---

## 2. Logic Chain

1. **State Enrichment (`src/core/state.py`)**: To enable downstream nodes to access persona and character bible attributes deterministically, `AgentState` must store `soul_id` (instance of `CharacterBible`) and `channel_persona` (instance of `ChannelPersonaConfig`).
2. **Visual Consistency Enforcement (`src/nodes/visual_storyboarder.py`)**: By pulling `soul_id` from state, the node can inject `static_visual_prompt`, `visual_anchors`, and `art_style_token` into LLM instructions, while post-processing enforces `layer1_identity_token` presence.
3. **Tone & Catchphrase Control (`src/nodes/tts_scriptwriter.py`)**: Pulling `channel_persona` allows dynamic injection of `tone_of_voice` (`Clinical, Ominous, Authoritative, Forbidden Knowledge`), signature catchphrases, and 60% Scientific Academic / 40% Pop-Psychology balance rules into Claude Sonnet's scriptwriter prompt.
4. **Narrative Waterfall Alignment (`src/nodes/script_architect.py`)**: Instructing the architect node on persona parameters ensures that initial beats pair academic studies (CBT, Neuropsychology) with dark psychology curiosity hooks.

---

## 3. Caveats

- **Assumptions**: The system assumes LiteLLM / Claude Sonnet routing is active for `tts_scriptwriter` node as configured in system default settings.
- **Scope Limit**: Code modification was strictly prohibited in this phase. Code snippet proposals must be applied during the implementation phase by the designated implementer agent.

---

## 4. Conclusion

The technical integration strategy for embedding Channel Niche Positioning and SOUL ID Character Bible into LangGraph is fully mapped, backward compatible, and documented in `langgraph_integration_mapping.md`. Complete, ready-to-apply code proposals have been formulated for `state.py`, `visual_storyboarder.py`, `tts_scriptwriter.py`, and `script_architect.py`.

---

## 5. Verification Method

To verify the findings and proposed implementation plan:
1. Inspect `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_langgraph_mapping\langgraph_integration_mapping.md`.
2. Verify syntactical correctness of proposed Pydantic v2 models in §3.1 against Pydantic v2 specifications.
3. Execute dry-run validation using `python workflows/graph_runner.py --dry-run` to confirm existing state structure integrity.
