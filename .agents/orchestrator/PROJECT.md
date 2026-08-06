# Project: Viral Learning Engine & Faceless Channel Pipeline

## Architecture
- `memory/viral_knowledge_bank/`: Persistent Knowledge Storage (`knowledge_base.json` and `patterns.md`).
- `src/connectors/learning_engine.py`: Autonomous Learning & Ingestion Engine (`ViralLearningEngine`).
- `ingest_viral_script.py`: CLI script for manual/batch ingestion of YouTube script transcripts.
- `src/nodes/script_architect.py`: LangGraph Node 3, reads top patterns and formats narrative skeleton.
- `src/nodes/tts_scriptwriter.py`: LangGraph Node 4, reads top patterns and generates TTS prose with Claude 3.7 Sonnet.
- `run_test.py`: Full pipeline integration test harness with LangGraph streaming and retention score evaluation.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | R1: Knowledge Bank Storage & Schema | `knowledge_base.json` with 6 categories: `hooks`, `analogies`, `micro_twists`, `sensory_beats`, `ctas`, `retention_tactics` | M1 | ORIGINAL_REQUEST §R1 |
| 2 | R1: Human-Readable Markdown Bank | `patterns.md` cataloging narrative patterns with tables & adapted examples | M1 | ORIGINAL_REQUEST §R1 |
| 3 | R2: Autonomous Learning Engine | `learning_engine.py` extraction, atomic json update, pattern formatting | M2 | ORIGINAL_REQUEST §R2 |
| 4 | R4: Ingestion CLI Script | `ingest_viral_script.py` accepting file/text, running learning engine | M3 | ORIGINAL_REQUEST §R4 |
| 5 | R4: Voyager 1 & Pluto Transcripts Processing | Populating knowledge base with Voyager 1 and Pluto/JWST case study data | M3 | ORIGINAL_REQUEST §R4 / AC1 |
| 6 | R3: Dynamic Prompt Injection | `script_architect.py` & `tts_scriptwriter.py` reading & injecting 6 categories into prompt | M4 | ORIGINAL_REQUEST §R3 |
| 7 | AC: Code Compilation | `python -m py_compile` check on `learning_engine.py` & nodes | M2/M4 | Acceptance Criteria |
| 8 | AC: Full E2E Pipeline Test | `run_test.py` passing end-to-end with injected learnings | M5 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Knowledge Bank Storage & Schema (R1) | Create/Update `knowledge_base.json` with all 6 categories including `retention_tactics` and generate `patterns.md` | None | DONE |
| 2 | M2: Autonomous Learning Engine (`learning_engine.py`) (R2) | Update `learning_engine.py` to support `retention_tactics`, atomic updates, `patterns.md` sync, and pass `py_compile` | M1 | DONE |
| 3 | M3: CLI Ingestion Script & Transcript Processing (R4) | Finalize `ingest_viral_script.py`, process Voyager 1 & Pluto/JWST transcript data, verify KB population | M2 | IN_PROGRESS |
| 4 | M4: Dynamic Prompt Injection into LangGraph Nodes (R3) | Ensure `script_architect.py` and `tts_scriptwriter.py` format & inject all 6 categories into Claude 3.7 Sonnet prompts | M2 | IN_PROGRESS |
| 5 | M5: E2E Pipeline Integration & Audit (AC) | Run `run_test.py`, verify full pipeline execution, and perform Forensic Audit verification | M3, M4 | PLANNED |

## Interface Contracts
### `ViralLearningEngine` (`src/connectors/learning_engine.py`)
- `__init__(self, kb_path: str = "memory/viral_knowledge_bank/knowledge_base.json")`
- `format_patterns_for_prompt(self) -> str`: returns formatted text containing top patterns from all 6 categories (`hooks`, `analogies`, `micro_twists`, `sensory_beats`, `ctas`, `retention_tactics`).
- `ingest_script_text(self, title: str, niche: str, script_text: str) -> dict`: extracts patterns via LLM analysis, updates `knowledge_base.json` atomically, updates `patterns.md`.

### Nodes (`script_architect.py` & `tts_scriptwriter.py`)
- Call `ViralLearningEngine().format_patterns_for_prompt()` and inject into prompt context without disturbing Pydantic schema validation (`ScriptSkeleton` and `TTSResponse`).

## Code Layout
- `memory/viral_knowledge_bank/knowledge_base.json`: Database file
- `memory/viral_knowledge_bank/patterns.md`: Markdown catalog
- `src/connectors/learning_engine.py`: Engine logic
- `ingest_viral_script.py`: CLI runner
- `src/nodes/script_architect.py`: Architect node
- `src/nodes/tts_scriptwriter.py`: Scriptwriter node
- `run_test.py`: Test runner
