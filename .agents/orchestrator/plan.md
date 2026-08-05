# Orchestration Plan

## Objectives
1. Audit 6-agent topology in src/nodes/ & src/core/engine.py (M1).
2. Research & select optimal anti-AI slop frontier model for scriptwriting via llm_version_checker (M2).
3. Refactor src/connectors/llm_router.py to enforce winning model on node_tts_scriptwriter, maintaining Ollama fallback (M3).
4. Verify all criteria via Reviewers, Challengers, and Forensic Auditor.
5. Notify Sentinel.

## Step-by-Step Execution Plan
- Phase 1 (Parallel Exploration & Research):
  - Dispatch Explorer to investigate M1 (LangGraph topology in src/nodes/ and src/core/engine.py) and test python syntax.
  - Dispatch Explorer / Spec Miner to conduct M2 LLM research using llm_version_checker skill.
- Phase 2 (Implementation & Verification):
  - M1: Verify python syntax (`python -m py_compile`). If any fixes needed, dispatch Worker.
  - M2: Consolidate model research recommendation.
  - M3: Dispatch Worker to refactor `src/connectors/llm_router.py` with winning model.
- Phase 3 (Review, Challenge & Forensic Audit):
  - Dispatch 2 Reviewers to review `engine.py`, `nodes`, and `llm_router.py`.
  - Dispatch 2 Challengers to test py_compile and verify Ollama fallback behavior.
  - Dispatch Forensic Auditor to check code integrity.
- Phase 4 (Completion):
  - Synthesize results, update `PROJECT.md` & `progress.md`.
  - Send handoff / notification back to parent/Sentinel.
