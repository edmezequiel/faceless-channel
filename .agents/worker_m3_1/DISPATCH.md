## 2026-08-05T14:53:22Z
<USER_REQUEST>
You are Worker 1 (LLM Router Refactorer).
Your working directory is: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\worker_m3_1

MANDATORY FIRST STEPS:
1. Create your working directory if it doesn't exist.
2. Read c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\ORIGINAL_REQUEST.md.
3. Create BRIEFING.md and progress.md in your working directory.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE FILE OWNERSHIP:
You own `src/connectors/llm_router.py` exclusively. Do not modify any other source files.

OBJECTIVE:
Refactor `src/connectors/llm_router.py` to enforce the winning model (`claude-3-7-sonnet-20250219` or `claude-3-5-sonnet-latest`) for `node_tts_scriptwriter` while preserving Ollama fallback for all other nodes.

TASKS:
- Inspect `src/connectors/llm_router.py`.
- Refactor `src/connectors/llm_router.py` to set:
  ```python
  if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
      target_model = "claude-3-7-sonnet-20250219"
      logger.info("Regra especial: Roteamento forçado para Claude 3.7 Sonnet (Anti-AI Slop).")
  ```
  (Or define `SCRIPTWRITER_WINNING_MODEL = "claude-3-7-sonnet-20250219"` and assign `target_model = SCRIPTWRITER_WINNING_MODEL`).
- Verify that `elif config.USE_LOCAL_LLM and target_model is None:` is preserved so all other nodes (`packaging_ctr`, `researcher_fact_checker`, `script_architect`, `visual_storyboarder`) continue to use local Ollama (`ollama/llama3`) fallback when `USE_LOCAL_LLM=True`.
- Execute build/syntax check command: `python -m py_compile src/connectors/llm_router.py`. Verify exit code 0.
- Write your complete handoff report to: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\worker_m3_1\handoff.md
- Report your completion to orchestrator via send_message with a brief summary and path to handoff.md.
</USER_REQUEST>
