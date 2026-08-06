# Viral Learning Engine — Orchestration Plan

## Overview
Implement an autonomous Viral Learning Engine for the `EDM ARCHETYPE LAB` faceless channel pipeline. The system ingests YouTube viral script transcripts/case studies, extracts narrative patterns (hooks, analogies, micro-twists, sensory beats, CTAs, retention tactics), updates a structured knowledge base (`knowledge_base.json` and `patterns.md`), dynamically injects learnings into LangGraph nodes (`script_architect.py` and `tts_scriptwriter.py`), provides a CLI entrypoint (`ingest_viral_script.py`), and validates via `run_test.py`.

## Phases & Milestones

### Survey & Architectural Mapping (Phase 0)
- Dispatch 3 `teamwork_preview_explorer` agents to examine current project layout, existing nodes (`src/nodes/script_architect.py`, `src/nodes/tts_scriptwriter.py`), existing test scripts (`run_test.py`), existing data files, and any pre-existing Voyager 1 / Pluto/JWST transcripts.

### Milestone Decomposition
1. **Milestone 1 (M1): Viral Knowledge Bank Storage & Schema (R1)**
   - Target files: `memory/viral_knowledge_bank/knowledge_base.json`, `memory/viral_knowledge_bank/patterns.md`
   - Schema requirements: JSON file with valid schema and top-level categories: `hooks`, `analogies`, `micro_twists`, `sensory_beats`, `ctas`, `retention_tactics`.
   - Markdown human-readable reference file `patterns.md`.

2. **Milestone 2 (M2): Ingestion & Autonomous Learning Module (R2)**
   - Target file: `src/connectors/learning_engine.py`
   - Capability: Parse viral script text/transcripts, analyze narrative anatomy, extract structured patterns, compute success/weight factors, atomically update `knowledge_base.json` and sync `patterns.md`.
   - Verification: `python -m py_compile src/connectors/learning_engine.py` + unit tests.

3. **Milestone 3 (M3): CLI Learning Script & Initial Transcripts Ingestion (R4)**
   - Target file: `ingest_viral_script.py`
   - CLI script capable of taking file paths or direct text, calling `learning_engine.py`, populating `knowledge_base.json`.
   - Verification: Process Voyager 1 and Pluto/JWST transcripts through `ingest_viral_script.py` and verify `knowledge_base.json` entries.

4. **Milestone 4 (M4): Dynamic Injection into LangGraph Pipeline (R3)**
   - Target files: `src/nodes/script_architect.py`, `src/nodes/tts_scriptwriter.py`
   - Dynamically load top patterns from `Viral Knowledge Bank` and inject into Claude 3.7 Sonnet prompt formatting during script generation.

5. **Milestone 5 (M5): E2E Pipeline Integration & Verification**
   - Target test: `run_test.py`
   - Verification: Execute `run_test.py` to confirm full LangGraph workflow generates scripts incorporating injected viral learnings.
   - Forensic audit: `teamwork_preview_auditor` verification for zero hardcoding/facades.

## Execution Strategy
- Follow Project Orchestration Pattern: Explorer -> Worker -> Reviewers -> Challengers -> Forensic Auditor.
- DISPATCH-ONLY discipline: spawn subagents under `.agents/` working directories.
