# Project: Faceless Channel LangGraph & LLM Router Optimization

## Architecture
- LangGraph topology: src/core/engine.py defines state graph wiring 6 nodes in src/nodes/
- LLM Router: src/connectors/llm_router.py manages model selection, routing rules, and fallback mechanisms (Ollama local fallback)

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | 6-Agent LangGraph Topology Audit | Confirm 6 nodes exist in src/nodes/ and are wired in engine.py; py_compile passes | M1 | ORIGINAL_REQUEST R1 | DONE |
| 2 | Anti-AI Slop Frontier LLM Selection | Evaluate models using llm_version_checker skill for highest human prose quality scriptwriting | M2 | ORIGINAL_REQUEST R2 | DONE |
| 3 | LLM Router Refactor | Update llm_router.py with winning model for node_tts_scriptwriter, preserve Ollama fallback | M3 | ORIGINAL_REQUEST R3 | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1_LangGraph_Audit | Audit src/nodes/ & src/core/engine.py, run py_compile | None | DONE |
| 2 | M2_LLM_Selection | Run llm_version_checker research for scriptwriting model | None | DONE |
| 3 | M3_Router_Refactor | Refactor llm_router.py with M2 winner & test fallback | M1, M2 | DONE |

## Code Layout
- `src/nodes/`: Agent node implementations
- `src/core/engine.py`: LangGraph workflow definition and state orchestration
- `src/connectors/llm_router.py`: LLM routing and fallback configuration
