## 2026-08-05T21:13:31Z
<USER_REQUEST>
You are a teamwork_preview_worker agent executing implementation for Milestones M1, M2, and M3.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\worker_m3_1

MANDATORY READ FIRST: Read c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\ORIGINAL_REQUEST.md
Also read the explorer reports:
- c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_audit_r1\analysis.md
- c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_matrix_r1\analysis.md
- c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_router_r1\analysis.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your Tasks:

1. **R1 — Dependencies & Repository Setup**:
   - Create `requirements.txt` in workspace root listing all Python dependencies (`langchain-core>=1.5.3`, `langgraph>=1.2.10`, `litellm>=1.95.0`, `pydantic>=2.13.4`, `python-dotenv>=1.0.0`, `yt-dlp`, `httpx`, `Pillow`, `numpy`, `opencv-python`, `moviepy`, `ffmpeg-python`, `edge-tts`).
   - Update `pyproject.toml` to list these dependencies in `dependencies = [...]`.
   - Check `.venv\Lib\site-packages\faceless_channel.pth` on Windows, and replace any UTF-8 absolute path with relative path `../../../src` if needed to fix `UnicodeDecodeError`.

2. **R2 — OmniRoute Multi-Model Matrix Configuration**:
   - Update `.env.example` to configure `OMNIROUTE_BASE_URL="http://localhost:20128/v1"` and define environment variables for the 6 stage models:
     `MODEL_RESEARCHER="gemini-2.0-flash"`
     `MODEL_PACKAGING="gpt-4o-mini"`
     `MODEL_ARCHITECT="claude-3-7-sonnet-20250219"`
     `MODEL_SCRIPTWRITER="claude-3-7-sonnet-20250219"`
     `MODEL_STORYBOARDER="gemini-2.0-flash"`
     `MODEL_AUDITOR="groq/llama-3.3-70b"`
   - Update `src/core/config.py` to declare settings for these stage models and `MODEL_ROUTING_MATRIX` mapping each agent role (`researcher`, `packaging`, `architect`, `scriptwriter`, `storyboarder`, `auditor`, `default`) to its primary model and fallback array.

3. **R3 — Refactor `src/connectors/llm_router.py` & Graph Nodes**:
   - Refactor `src/connectors/llm_router.py` to accept `agent_role: Optional[str] = None` in `generate_response()`.
   - Resolve primary model and fallbacks via `config.MODEL_ROUTING_MATRIX`. Ensure model names are properly formatted with `openai/` prefix for LiteLLM OmniRoute proxy (`http://localhost:20128/v1`).
   - Implement fallback retry iteration: attempt primary model, then fallback models, returning response upon success or returning informative error if all fail.
   - Update `src/nodes/` files (`researcher_fact_checker.py`, `packaging_ctr.py`, `script_architect.py`, `tts_scriptwriter.py`, `visual_storyboarder.py`, `retention_auditor.py`) to pass `agent_role="..."` to `generate_response()`.

4. **Verification**:
   - Execute `python -m py_compile` across all files in `src/connectors/llm_router.py`, `src/core/config.py`, `src/core/engine.py`, and all files in `src/nodes/*.py`.
   - Document commands executed and exact output results.

Deliverables:
- Implement code changes directly in project source files (`requirements.txt`, `.env.example`, `pyproject.toml`, `src/core/config.py`, `src/connectors/llm_router.py`, `src/nodes/*.py`).
- Save implementation report to `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\worker_m3_1\changes.md`.
- Save handoff report to `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\worker_m3_1\handoff.md` following the Handoff Protocol.
- Send a message to parent when finished.
</USER_REQUEST>
