# Project: Faceless Channel — Hell Grind Improvement Plan

## Architecture
This is a planning and architecture audit phase.
- Input: `https://higgsfield.ai/@higgsfield.studio/projects/hell-grind` & existing codebase in `src/nodes/` and `src/core/engine.py`.
- Output: `implementation_plan.md` in root and `.agents/orchestrator/implementation_plan.md`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Hell Grind Knowledge Extraction | Extract scripting methods, prompt engineering styles, visual direction, camera movements, color/mood guidelines, transition logic, agent workflows | M1 | Web Page / Search |
| 2 | Codebase Architecture Audit | Audit all files in `src/nodes/` and `src/core/engine.py` to document node responsibilities, prompt structure, workflow links | M2 | Codebase |
| 3 | Comparative Gap Analysis | Compare Hell Grind techniques vs current nodes, identifying specific gaps in prompt engineering, script structuring, visual directions, multi-agent coordination | M2 | Synthesis |
| 4 | Implementation Plan Creation | Generate `implementation_plan.md` with detailed improvements to absorb and "Alterações Propostas" mapped to specific files in `src/nodes/` | M3 | Synthesis |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Hell Grind Knowledge Extraction | Extract deep insights from Higgsfield Hell Grind project page | None | DONE |
| M2 | Codebase Audit & Comparative Analysis | Audit `src/nodes/` & `src/core/engine.py` and analyze gaps against M1 findings | M1 | DONE |
| M3 | Implementation Plan Generation | Produce final `implementation_plan.md` | M1, M2 | DONE |

## Code Layout (Read-Only Audit Scope)
- `src/nodes/` - Individual pipeline nodes (topic, scriptwriter, visual prompt generator, tts, video generator, publisher, etc.)
- `src/core/engine.py` - LangGraph orchestrator engine linking all nodes
- `implementation_plan.md` - Target deliverable file
