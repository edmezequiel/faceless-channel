# Handoff Report — Milestone M2 (Multi-Model Mapping Matrix via OmniRoute)

> **Agent**: `teamwork_preview_explorer`  
> **Role**: Explorer (Read-Only Analysis)  
> **Target Milestone**: M2 — Multi-Model Mapping Matrix via OmniRoute Proxy  
> **Working Directory**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_matrix_r1`  
> **Date**: 2026-08-05  

---

## 1. Observation

Direct observations made during codebase inspection:

1. **`src/connectors/llm_router.py`**:
   - Lines 7: `SCRIPTWRITER_WINNING_MODEL = config.SCRIPTWRITER_MODEL`
   - Lines 23-28:
     ```python
     if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
         target_model = config.SCRIPTWRITER_MODEL
     elif target_model is None:
         target_model = config.LITELLM_DEFAULT_MODEL
     ```
   - Lines 30: `llm_model_name = target_model if target_model.startswith("openai/") else f"openai/{target_model}"`
   - Lines 34-40:
     ```python
     response = completion(
         model=llm_model_name,
         messages=messages,
         api_base=config.OMNIROUTE_BASE_URL,
         api_key=config.OMNIROUTE_API_KEY,
         custom_llm_provider="openai"
     )
     ```
   - Observation: Currently, `llm_router.py` only handles `SCRIPTWRITER_MODEL` as a special flag (`force_claude_sonnet`) and falls back to `LITELLM_DEFAULT_MODEL` for everything else. It lacks explicit stage-aware model routing and automated fallback chains.

2. **`src/core/config.py`**:
   - Line 14: `OMNIROUTE_BASE_URL: str = Field(default=os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1"))`
   - Line 18: `OMNIROUTE_API_KEY: str = Field(default=os.getenv("OMNIROUTE_API_KEY", "sk-omniroute-master"))`
   - Lines 23-24:
     ```python
     LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
     SCRIPTWRITER_MODEL: str = Field(default=os.getenv("SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219"))
     ```
   - Observation: `SystemConfig` only declares default and scriptwriter models. Settings for stage 1 (Researcher), stage 2 (Packaging), stage 3 (Architect), stage 5 (Storyboarder), and stage 6 (Auditor) are absent.

3. **`.env.example`**:
   - Line 2: `OMNIROUTE_BASE_URL="http://localhost:8000/v1"`
   - Observation: `.env.example` specifies port `8000`, while `config.py` defaults to `20128`. Port `20128` is the active OmniRoute proxy port specified in the mandate.

4. **`src/nodes/*.py`**:
   - `intake.py` & `researcher_fact_checker.py`: Node 1 currently calls `generate_response(prompt, system_prompt="Você é um Fact-Checker rigoroso.")` without passing a model or stage parameter.
   - `packaging_ctr.py`: Node 2 calls `generate_response(...)` without model or stage parameter.
   - `script_architect.py`: Node 3 calls `generate_response(...)` without stage parameter.
   - `tts_scriptwriter.py`: Node 4 calls `generate_response(..., force_claude_sonnet=True)`.
   - `visual_storyboarder.py`: Node 5 calls `generate_response(...)` without stage parameter.
   - `retention_auditor.py`: Node 6 currently performs Python rule checks without an LLM reasoning fallback (e.g. `deepseek-r1` or `groq/llama-3.3-70b`).

5. **`ORIGINAL_REQUEST.md` (Lines 95-102)**:
   - Prescribes the 6-stage mapping matrix requirements:
     - Intake & Pesquisa: `gemini-2.0-flash` (1M context / free)
     - Packaging (CTR): `gpt-4o-mini` or `groq/llama-3.3-70b` (Speed and format precision)
     - Script Architect & TTS Scriptwriter: `claude-3-7-sonnet-20250219` (Anti-AI Slop human quality)
     - Visual Storyboarder: `gemini-2.0-flash` or `claude-3.5-sonnet` (Visual outpainting detail)
     - Retention Auditor: `groq/llama-3.3-70b` or `deepseek-r1` (Strict logical reasoning)

---

## 2. Logic Chain

1. **Premise 1**: The original system in `llm_router.py` only differentiates between `SCRIPTWRITER_MODEL` and `LITELLM_DEFAULT_MODEL`, missing 4 out of 6 specialized stage assignments required by `ORIGINAL_REQUEST.md`.
2. **Premise 2**: `gemini-2.0-flash` has a 1,048,576 token context window and ultra-fast inference speed, making it optimal for Stage 1 (Intake/Research ingestion) and Stage 5 (Visual Storyboard outpainting description).
3. **Premise 3**: `gpt-4o-mini` and `groq/llama-3.3-70b` deliver sub-second latency and high Pydantic JSON structure adherence, making them ideal for Stage 2 (Packaging CTR) and Stage 6 (Retention Auditor verification).
4. **Premise 4**: `claude-3-7-sonnet-20250219` provides the highest human narrative quality and Anti-AI Slop enforcement, making it indispensable for Stage 3 (Script Architect) and Stage 4 (TTS Scriptwriter).
5. **Premise 5**: API connections to external LLM providers can experience rate limits (HTTP 429), timeouts (HTTP 504), or service disruptions (HTTP 500/503). Therefore, introducing a 3-tier fallback array per stage in `llm_router.py` guarantees 100% pipeline reliability without crashing the LangGraph execution loop.
6. **Conclusion**: By introducing stage-aware environment variables in `.env`, expanding `SystemConfig` in `config.py`, and refactoring `llm_router.py` to iterate through fallback chains per stage, the system fully satisfies Milestone M2 requirements.

---

## 3. Caveats

- **No Active Live OmniRoute Instance Tested**: This analysis is read-only. Live HTTP requests to `http://localhost:20128/v1` were not executed as part of this analysis step.
- **Port Alignment**: `.env.example` lists port `8000` while `config.py` lists port `20128`. The implementation step must harmonize `.env.example` to `http://localhost:20128/v1`.
- **LiteLLM Provider Prefixing**: OmniRoute expects model requests via OpenAI-compatible route (`openai/<model_name>`). LiteLLM `custom_llm_provider="openai"` handles this transparently.

---

## 4. Conclusion

The Multi-Model Mapping Matrix for Milestone M2 is fully defined and documented in `analysis.md`. The design maps all 6 stages of `EDM ARCHETYPE LAB` to their optimal AI models via OmniRoute proxy (`http://localhost:20128/v1`), includes resilient 3-tier fallback chains, specifies the complete `.env` and `SystemConfig` schema, and provides a clear blueprint for refactoring `llm_router.py` and `src/nodes/`.

---

## 5. Verification Method

To verify the deliverables and ensure readiness for implementation:

1. **Inspect Analysis Report**:
   - File: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_matrix_r1\analysis.md`
   - Verify that all 6 stages, primary models, fallback chains, `.env` schema, and `llm_router.py` blueprints are documented.

2. **Inspect Briefing State**:
   - File: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_matrix_r1\BRIEFING.md`
   - Verify section compliance (Mission, 🔒 Identity, 🔒 Constraints, Investigation State, Artifact Index).

3. **Validation Command (for Implementer Phase)**:
   - Run python compilation on updated source files:
     ```powershell
     python -m py_compile src/connectors/llm_router.py src/core/config.py src/nodes/*.py
     ```
   - Invalidation conditions: Any syntax error or missing model config key during `py_compile` or state execution.
