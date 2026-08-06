# Project: Dependency Audit, OmniRoute Model Matrix & LangGraph Router Refactoring

## Architecture
Comprehensive audit of codebase dependencies and tools, mapping of OmniRoute Multi-Model Matrix for 6 pipeline stages, dynamic routing refactoring in `src/connectors/llm_router.py` and `src/nodes/`, and syntax compilation verification across all graph nodes and `src/core/engine.py`.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | Dependency & Tool Audit | Audit `requirements.txt`, `src/`, `docs/`, `scripts/`, external tools/repos, and READMEs for Windows compilation & installation | M1 | Codebase / Specs | PLANNED |
| 2 | Multi-Model Mapping Matrix | Map ideal models for 6 stages via OmniRoute proxy (`http://localhost:20128/v1`) with fallbacks | M2 | Requirements | PLANNED |
| 3 | LLM Router Refactoring | Refactor `src/connectors/llm_router.py` to route through OmniRoute proxy with dynamic model selection and fallbacks | M3 | Architecture | PLANNED |
| 4 | Graph Nodes & Engine Refactoring | Update nodes in `src/nodes/` and `src/core/engine.py` to use dynamic model selection via `llm_router.py` | M3 | Refactoring | PLANNED |
| 5 | Graph Syntax Verification | Verify all `.py` files in `src/nodes/` and `src/core/engine.py` compile cleanly via `python -m py_compile` | M3 | Verification | PLANNED |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Dependency & Repository Audit | Analyze `requirements.txt`, READMEs, external tools/repos, verify Windows compatibility | None | IN_PROGRESS |
| M2 | Multi-Model Matrix Architecture | Document and map 6-stage model selection matrix with fallbacks via OmniRoute proxy | M1 | IN_PROGRESS |
| M3 | Router Refactoring & Graph Compilation | Refactor `llm_router.py`, `src/nodes/`, `src/core/engine.py` + verify `py_compile` clean pass | M2 | IN_PROGRESS |

## Code Layout
- `requirements.txt` - Dependency specification
- `src/connectors/llm_router.py` - LLM Connector & Dynamic Router via OmniRoute
- `src/nodes/` - LangGraph node definitions (intake, packaging, script architect, tts scriptwriter, visual storyboarder, retention auditor, etc.)
- `src/core/engine.py` - LangGraph workflow engine & state graph builder
- `docs/` and `scripts/` - Project documentation and setup/execution scripts

