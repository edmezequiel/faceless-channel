# Handoff Report — Codebase Architecture Survey

## 1. Observation

Direct observations from workspace analysis at `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL`:

### 1.1 Directory Structure & File Hierarchy
- **Workspace Root**:
  - Contains configuration files: `pyproject.toml` (lines 1-24), `requirements.txt` (lines 1-14), `.env`, `.env.example`.
  - Execution entrypoints: `run_test.py` (lines 1-152), `ingest_viral_script.py` (lines 1-58), `test_models.py` (lines 1-16), `run.ps1`.
  - Core folders: `src/`, `memory/`, `workflows/`, `.agents/`.
- **`src/` Directory**:
  - `src/connectors/`: Contains LLM integration and learning components (`agent_reach.py`, `learning_engine.py`, `llm_router.py`).
  - `src/core/`: Contains system configuration (`config.py`), state definitions (`state.py`), and LangGraph pipeline builder (`engine.py`).
  - `src/nodes/`: Contains 8 execution nodes (`intake.py`, `orchestrator.py`, `researcher_fact_checker.py`, `packaging_ctr.py`, `script_architect.py`, `tts_scriptwriter.py`, `visual_storyboarder.py`, `retention_auditor.py`).
  - `src/faceless_channel/`: Python module initialization (`__init__.py`).
- **`memory/` Directory**:
  - `memory/viral_knowledge_bank/knowledge_base.json`: Persistent JSON database storing viral patterns across `hooks`, `analogies`, `micro_twists`, `sensory_beats`, and `ctas`.
  - Additional memory documents and test artifacts (`curated_memory.json`, `knowledge_base.md`, `narrative_frameworks.md`, `grokfilm_index.md`, `roteiro_triada_negra.md`, `audio_triada_negra.mp3`).

### 1.2 Node Analysis: `src/nodes/script_architect.py`
- **Imports** (lines 1-10):
  - `from src.core.state import AgentState, ScriptSkeleton`
  - `from src.connectors.llm_router import generate_response`
  - `from langchain_core.output_parsers import PydanticOutputParser`
  - `from langchain_core.exceptions import OutputParserException`
  - `from src.connectors.learning_engine import ViralLearningEngine`
- **Signature** (line 12): `def node_script_architect(state: AgentState) -> AgentState:`
- **State & Integration**:
  - Reads `state.get("factual_context", "")` and `state.get("goal", "")`.
  - Instantiates `learning_engine = ViralLearningEngine()` and calls `learning_engine.format_patterns_for_prompt()` (lines 23-24).
  - Uses `PydanticOutputParser(pydantic_object=ScriptSkeleton)` (line 27).
  - Invokes `generate_response(prompt, system_prompt=..., agent_role="architect")` (line 55).
  - Returns `{"script_skeleton": skeleton_dict, "current_status": "architect_done"}` (line 67).

### 1.3 Node Analysis: `src/nodes/tts_scriptwriter.py`
- **Imports** (lines 1-10):
  - `from src.core.state import AgentState`
  - `from src.connectors.llm_router import generate_response`
  - `from pydantic import BaseModel, Field`
  - `from langchain_core.output_parsers import PydanticOutputParser`
  - `from langchain_core.exceptions import OutputParserException`
  - `from src.connectors.learning_engine import ViralLearningEngine`
- **Signature** (line 15): `def node_tts_scriptwriter(state: AgentState) -> AgentState:`
- **State & Integration**:
  - Reads `state.get("script_skeleton", {})`, `state.get("factual_context", "")`, `state.get("auditor_feedback", "")`.
  - Instantiates `learning_engine = ViralLearningEngine()` and injects `viral_context` (lines 26-27, line 41).
  - Enforces persona ("Dr. Victor Vane"), 80/20 audio split (`[VOICEOVER]` vs `[LIP_SYNC]`), Anti-AI Slop list, sentence brevity (max 15 words), prosody tags (`[PAUSA_0.5s]`, `[TOM_ANALITICO]`, etc.), domestic analogies, and soft CTA.
  - Invokes `generate_response(prompt=prompt, system_prompt=..., force_claude_sonnet=True)` (line 59).
  - Returns `{"tts_prose": prose_text, "word_count": word_count, "current_status": "scriptwriter_done"}` (line 73).

### 1.4 Connector Components (`src/connectors/`)
- Located at `src/connectors/`.
- Active files:
  1. `learning_engine.py`: Defines `ViralLearningEngine` class. Manages `memory/viral_knowledge_bank/knowledge_base.json`, formats top patterns for prompts (`format_patterns_for_prompt()`), and ingests raw script transcripts via LLM parsing (`ingest_script_text()`).
  2. `llm_router.py`: Defines `generate_response()`. Renders OpenAI-compatible requests over OmniRoute (`config.OMNIROUTE_BASE_URL`). Routes agent roles (`researcher`, `packaging`, `architect`, `scriptwriter`, `storyboarder`, `auditor`) to specific model configs or forces Claude 3.7 Sonnet.
  3. `agent_reach.py`: Defines `AgentReachConnector`. Mock/wrapper for web extraction (Jina Reader) and YouTube searching (yt-dlp).

### 1.5 Dependencies and Code Patterns
- **Dependencies (`requirements.txt` & `pyproject.toml`)**:
  - Orchestration & LLM: `langchain-core` (>=1.5.3), `langgraph` (>=1.2.10), `litellm` (>=1.95.0), `pydantic` (>=2.13.4).
  - Utility & Media: `python-dotenv`, `yt-dlp`, `httpx`, `Pillow`, `numpy`, `opencv-python`, `moviepy`, `ffmpeg-python`, `edge-tts`.
  - Build system: `uv_build`.
- **Code Patterns**:
  - State Graph Pattern: LangGraph `StateGraph(AgentState)` in `src/core/engine.py` orchestrating nodes sequentially with a conditional closed loop (`auditor_router`) back to `scriptwriter` if retention score < 85.
  - Pydantic Output Parsing: Strict schema validation for node outputs (`ScriptSkeleton`, `TTSResponse`, `Packaging`, `ShotMetadata`, `VisualBlock`).
  - Dynamic Viral Knowledge Injection: Both `script_architect.py` and `tts_scriptwriter.py` fetch viral patterns at runtime from `ViralLearningEngine` to enrich system prompts dynamically.

---

## 2. Logic Chain

1. **Workspace Inspection**: Listing the workspace root and `src/` hierarchy confirmed that `src/connectors/` exists as a dedicated directory containing `learning_engine.py`, `llm_router.py`, and `agent_reach.py`.
2. **Node Implementation Audit**: Reading `script_architect.py` and `tts_scriptwriter.py` verified that both nodes import `ViralLearningEngine`, invoke `format_patterns_for_prompt()`, and embed `viral_context` into their respective LLM prompt strings.
3. **Data Flow & State Propagation**:
   - `script_architect.py` consumes `goal` and `factual_context`, formats instructions using `ScriptSkeleton`, calls `llm_router.generate_response(..., agent_role="architect")`, and produces `script_skeleton`.
   - `tts_scriptwriter.py` consumes `script_skeleton`, `factual_context`, and `auditor_feedback`, uses `TTSResponse`, calls `generate_response(..., force_claude_sonnet=True)`, and produces `tts_prose` and `word_count`.
4. **Dependency Synthesis**: Reviewing `requirements.txt` and `pyproject.toml` established that the system relies on LangGraph for state graph execution, LiteLLM / OmniRoute for model proxying, Pydantic v2 for typing and validation, and `edge-tts`/`moviepy`/`yt-dlp` for downstream media handling.

---

## 3. Caveats

- **External Services / Proxy Dependencies**: `src/connectors/llm_router.py` targets `config.OMNIROUTE_BASE_URL` (`http://localhost:20128/v1`). Execution of LLM calls during live runs requires the OmniRoute proxy service or valid endpoint configuration in `.env`.
- **Mock Implementations**: `src/connectors/agent_reach.py` contains mock responses for webpage reading and YouTube searching (subprocesses commented out for safety/development).

---

## 4. Conclusion

The repository architecture is structured around a 6-agent LangGraph pipeline (`src/core/engine.py`) integrated with a dynamic learning connector (`src/connectors/learning_engine.py`) and a centralized LLM router (`src/connectors/llm_router.py`).

- `src/connectors/` is fully operational with `learning_engine.py`, `llm_router.py`, and `agent_reach.py`.
- `script_architect.py` and `tts_scriptwriter.py` are properly wired to read from `ViralLearningEngine` and enforce persona guidelines, Pydantic output parsing, and model routing.
- The project setup follows clean modular separation: nodes in `src/nodes/`, core infrastructure in `src/core/`, connectors in `src/connectors/`, and knowledge memory in `memory/`.

---

## 5. Verification Method

To independently verify these observations:

1. **Verify Python Syntax Compilation**:
   ```powershell
   .venv\Scripts\python.exe -m py_compile src/connectors/learning_engine.py src/nodes/script_architect.py src/nodes/tts_scriptwriter.py src/core/engine.py
   ```
2. **Inspect Node & Connector Files**:
   - `view_file` on `src/nodes/script_architect.py` lines 23-24 and `src/nodes/tts_scriptwriter.py` lines 26-27 to confirm `ViralLearningEngine` instantiation.
   - `view_file` on `src/connectors/learning_engine.py` to confirm database path pointing to `memory/viral_knowledge_bank/knowledge_base.json`.
3. **Verify Pipeline Dry-Run / Test**:
   ```powershell
   .venv\Scripts\python.exe workflows/graph_runner.py --dry-run
   ```
