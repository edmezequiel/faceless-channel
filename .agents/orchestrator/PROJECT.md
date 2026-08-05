# Project: Channel Niche Positioning, Brand Identity & LangGraph Integration

## Architecture
Strategic positioning, brand identity design, proprietary virtual presenter character bible (SOUL ID), and LangGraph architecture integration mapping for the Faceless Channel.
- Input: User specifications in `ORIGINAL_REQUEST.md`, existing codebase (`src/nodes/visual_storyboarder.py`, `src/nodes/tts_scriptwriter.py`, `src/core/state.py`).
- Output: Complete Character Bible / SOUL ID specification + `implementation_plan.md` in workspace root.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | Niche Research & Positioning | Benchmark successful channels (Academy of Ideas, Einzelgänger, Psych2Go, Netflix Dark Psych) and map scientific vs pop psych fusion | M1 | Browser / Web | IN_PROGRESS |
| 2 | Brand Identity & SOUL ID Bible | Define virtual presenter archetype, visual anchors, static prompt of SOUL_ID, palette, recurring symbols, catchphrase | M2 | Synthesis | IN_PROGRESS |
| 3 | LangGraph Codebase Audit | Audit `visual_storyboarder.py`, `tts_scriptwriter.py`, and `state.py` for integration points | M3 | Codebase | IN_PROGRESS |
| 4 | Implementation Plan Generation | Produce `implementation_plan.md` in workspace root detailing LangGraph integration without modifying `.py` files | M3 | Synthesis | IN_PROGRESS |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Niche Research & Positioning | Deep-dive research on top psychology channels, defining scientific + pop psychology balance | None | IN_PROGRESS |
| M2 | Brand Identity & SOUL ID Bible | Complete specification of channel identity, anti-copy character bible, static prompt, visual anchors, tone | M1 | IN_PROGRESS |
| M3 | LangGraph Architecture & Plan | Detailed mapping of `layer1_identity_token`, `SOUL_ID`, `tts_scriptwriter.py` tone, and creation of `implementation_plan.md` | M1, M2 | IN_PROGRESS |

## Code Layout (Read-Only Audit Scope)
- `src/nodes/visual_storyboarder.py` - Storyboard generation, camera prompts, `layer1_identity_token` injection
- `src/nodes/tts_scriptwriter.py` - Script generation, narration pacing, tone of voice control
- `src/core/state.py` - Pydantic state schemas, `SOUL_ID` definition
- `implementation_plan.md` - Target deliverable artifact in workspace root
