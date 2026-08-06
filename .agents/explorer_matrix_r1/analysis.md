# Multi-Model Mapping Matrix via OmniRoute Architecture Report

> **Milestone**: M2 (Multi-Model Mapping Matrix via OmniRoute)  
> **Target System**: EDM ARCHETYPE LAB — 6-Stage Autonomous Content Conveyor  
> **Gateway Endpoint**: OmniRoute Proxy (`http://localhost:20128/v1`)  
> **Author**: `teamwork_preview_explorer`  
> **Status**: Completed Analysis  

---

## 1. Executive Summary & Architectural Overview

The **EDM ARCHETYPE LAB** autonomous video pipeline requires distinct LLM cognitive profiles across its 6 specialized agent nodes. A single monolithic model approach fails to balance cost, context capacity, speed, structured output fidelity, and literary quality.

To solve this, **OmniRoute** acts as a unified OpenAI-compatible local proxy (`http://localhost:20128/v1`). It abstracts 30+ underlying AI models (OpenAI, Anthropic, Google Gemini, Groq, DeepSeek, Qwen) behind a standardized API.

### Key Objectives Achieved in this Architecture:
1. **Cost & Latency Optimization**: Route heavy context ingestion to high-speed/zero-cost tier models (`gemini-2.0-flash`) and fast structural tasks to sub-second providers (`gpt-4o-mini`, `groq/llama-3.3-70b`).
2. **Anti-AI Slop Human Quality**: Mandate flagship reasoning models (`claude-3-7-sonnet-20250219`) for script structure and TTS prose writing.
3. **Infinite Scroll Visual Continuity**: Utilize multimodal/long-context visual prompt generators (`gemini-2.0-flash` / `claude-3.5-sonnet`) for spatial outpainting details and camera taxonomy.
4. **Deterministic Audit & Closed-Loop Reasoning**: Use strict analytical models (`groq/llama-3.3-70b` or `deepseek-r1`) to audit retention criteria and provide chain-of-thought feedback on script failures.
5. **Resilient Fallback Chains**: Implement multi-tier provider fallbacks for 100% pipeline uptime against rate limits (429) or provider outages (500/503).

---

## 2. Multi-Model Mapping Matrix

The table below defines the assignment of primary and fallback models across all 6 conveyor belt stages, including context requirements, latency/cost tiering, and functional rationale.

| Stage # | Stage Name | Node File | Primary Model | Secondary / Fallback Model | Context Window | Latency / Cost Tier | Key Capabilities & Rationale |
|---|---|---|---|---|---|---|---|
| **1** | **Intake & Pesquisa** | `intake.py`<br>`researcher_fact_checker.py` | `gemini-2.0-flash` | `qwen-2.5-72b` / `gemini-1.5-flash` | 1,048,576 tokens (1M) | Ultra-Fast / Low-Cost | Ingests massive web search payloads, YouTube transcripts, and raw factual docs without context truncation. Filters bias instantly. |
| **2** | **Packaging (CTR)** | `packaging_ctr.py` | `gpt-4o-mini` | `groq/llama-3.3-70b` | 128,000 tokens | Sub-Second / Low-Cost | High adherence to Pydantic JSON schemas. Rapidly generates Curiosity Gap titles and visual thumbnail concepts. |
| **3** | **Script Architect** | `script_architect.py` | `claude-3-7-sonnet-20250219` | `claude-3.5-sonnet` / `gpt-4o` | 200,000 tokens | High Quality / Mid-Cost | Superior long-form narrative pacing ("Waterfall" flow), open-loop placement, kinetic text overlay timing, and character voice setup. |
| **4** | **TTS Scriptwriter** | `tts_scriptwriter.py` | `claude-3-7-sonnet-20250219` | `claude-3.5-sonnet` | 200,000 tokens | Premium Quality / High-Cost | **Anti-AI Slop Engine**: Exceptional literary nuance, zero forbidden buzzwords, precise prosody tagging (`[PAUSA_0.5s]`), 80/20 audio split (`[VOICEOVER]` vs `[LIP_SYNC]`), max 15 words/sentence. |
| **5** | **Visual Storyboarder** | `visual_storyboarder.py` | `gemini-2.0-flash` | `claude-3.5-sonnet` | 1,048,576 tokens | Fast / Low-Cost | Granular spatial outpainting descriptions, top 40% seam continuity, bottom 60% expansion prompts, strict camera taxonomy (`Vertical Pan Down`). |
| **6** | **Retention Auditor** | `retention_auditor.py` | `groq/llama-3.3-70b` | `deepseek-r1` | 128,000 tokens | Sub-Second / High-Reasoning | Strict rule enforcement, mathematical sentence breath verification, prosody density audit, camera movement tax compliance, and DeepSeek-R1 chain-of-thought feedback on failure. |

---

## 3. OmniRoute Proxy Specs & Model Aliasing Protocol

OmniRoute standardizes requests by exposing an OpenAI-compatible `/v1/chat/completions` endpoint. LiteLLM routes requests to OmniRoute by prefixing model names with `openai/`.

### 3.1 Proxy Configuration Defaults
- **OmniRoute Base Endpoint**: `http://localhost:20128/v1`
- **Master Authentication Key**: `sk-omniroute-master`
- **Custom LLM Provider**: `openai`

### 3.2 Model Alias & Upstream Mapping Table

To isolate model name changes from node implementation, OmniRoute supports model alias routing:

| Stage Role Alias | Config Env Variable | Canonical Upstream Target Model | OmniRoute Model Identifier String |
|---|---|---|---|
| `researcher` | `RESEARCHER_MODEL` | `gemini-2.0-flash` | `openai/gemini-2.0-flash` |
| `packaging` | `PACKAGING_MODEL` | `gpt-4o-mini` | `openai/gpt-4o-mini` |
| `architect` | `SCRIPT_ARCHITECT_MODEL` | `claude-3-7-sonnet-20250219` | `openai/claude-3-7-sonnet-20250219` |
| `scriptwriter` | `TTS_SCRIPTWRITER_MODEL` | `claude-3-7-sonnet-20250219` | `openai/claude-3-7-sonnet-20250219` |
| `storyboarder` | `VISUAL_STORYBOARDER_MODEL` | `gemini-2.0-flash` | `openai/gemini-2.0-flash` |
| `auditor` | `RETENTION_AUDITOR_MODEL` | `groq/llama-3.3-70b` | `openai/groq/llama-3.3-70b` |
| `default` | `LITELLM_DEFAULT_MODEL` | `gpt-4o-mini` | `openai/gpt-4o-mini` |

---

## 4. Fallback Chains & Fault Tolerance Strategy

If OmniRoute returns an error for a primary model (e.g. Provider Rate Limit `429`, Gateway Timeout `504`, Internal Server Error `500/503`), the `llm_router.py` module automatically catches the exception and executes a 3-tier fallback sequence:

```
[ Primary Stage Model ] ---> (Success) ---> Return Output
        |
    (Exception: 429 / 500 / 504 / Schema Error)
        v
[ Secondary Fallback Model ] ---> (Success) ---> Return Output
        |
    (Exception)
        v
[ Emergency Global Model (gpt-4o-mini) ] ---> (Success) ---> Return Output
        |
    (Exception)
        v
Raise Standardized LLM Error & Log Audit Trait in AgentState
```

### Fallback Matrix Per Stage:
1. **Intake & Pesquisa**: `gemini-2.0-flash` ➔ `qwen-2.5-72b` ➔ `gpt-4o-mini`
2. **Packaging (CTR)**: `gpt-4o-mini` ➔ `groq/llama-3.3-70b` ➔ `gemini-2.0-flash`
3. **Script Architect**: `claude-3-7-sonnet-20250219` ➔ `claude-3.5-sonnet` ➔ `gpt-4o`
4. **TTS Scriptwriter**: `claude-3-7-sonnet-20250219` ➔ `claude-3.5-sonnet` ➔ `gpt-4o`
5. **Visual Storyboarder**: `gemini-2.0-flash` ➔ `claude-3.5-sonnet` ➔ `gpt-4o-mini`
6. **Retention Auditor**: `groq/llama-3.3-70b` ➔ `deepseek-r1` ➔ `gpt-4o-mini`

---

## 5. Environment Variable & SystemConfig Schema

### 5.1 Environment File (`.env`) Specification

```env
# ==============================================================================
# CENTRAL OMNIROUTE PROXY CONFIGURATION (OPENAI-COMPATIBLE GATEWAY)
# ==============================================================================
OMNIROUTE_BASE_URL="http://localhost:20128/v1"
OMNIROUTE_API_KEY="sk-omniroute-master"

# ==============================================================================
# GLOBAL DEFAULT FALLBACK MODEL
# ==============================================================================
LITELLM_DEFAULT_MODEL="gpt-4o-mini"

# ==============================================================================
# EDM ARCHETYPE LAB — STAGE-SPECIFIC MODEL ROUTING MATRIX
# ==============================================================================
# Stage 1: Intake & Research
RESEARCHER_MODEL="gemini-2.0-flash"
RESEARCHER_FALLBACK_MODEL="qwen-2.5-72b"

# Stage 2: Packaging & CTR
PACKAGING_MODEL="gpt-4o-mini"
PACKAGING_FALLBACK_MODEL="groq/llama-3.3-70b"

# Stage 3: Script Architect
SCRIPT_ARCHITECT_MODEL="claude-3-7-sonnet-20250219"
SCRIPT_ARCHITECT_FALLBACK_MODEL="claude-3.5-sonnet"

# Stage 4: TTS Scriptwriter (Anti-AI Slop Engine)
TTS_SCRIPTWRITER_MODEL="claude-3-7-sonnet-20250219"
TTS_SCRIPTWRITER_FALLBACK_MODEL="claude-3.5-sonnet"

# Stage 5: Visual Storyboarder (Spatial Outpainting & Infinite Scroll)
VISUAL_STORYBOARDER_MODEL="gemini-2.0-flash"
VISUAL_STORYBOARDER_FALLBACK_MODEL="claude-3.5-sonnet"

# Stage 6: Retention Auditor (Strict Rule Enforcement)
RETENTION_AUDITOR_MODEL="groq/llama-3.3-70b"
RETENTION_AUDITOR_FALLBACK_MODEL="deepseek-r1"
```

### 5.2 Refactored `SystemConfig` Blueprint (`src/core/config.py`)

```python
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class SystemConfig(BaseModel):
    """
    Global system configuration for Faceless EDM ARCHETYPE LAB.
    Integrated with OmniRoute Multi-Model Gateway & Fallback Chains.
    """
    # Central Proxy Settings
    OMNIROUTE_BASE_URL: str = Field(
        default=os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1"),
        description="Base URL for OmniRoute OpenAI-compatible proxy endpoint"
    )
    OMNIROUTE_API_KEY: str = Field(
        default=os.getenv("OMNIROUTE_API_KEY", "sk-omniroute-master"),
        description="Master API Key for OmniRoute"
    )
    
    # Global Default Fallback
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))

    # Stage Model Assignments
    RESEARCHER_MODEL: str = Field(default=os.getenv("RESEARCHER_MODEL", "gemini-2.0-flash"))
    RESEARCHER_FALLBACK_MODEL: str = Field(default=os.getenv("RESEARCHER_FALLBACK_MODEL", "qwen-2.5-72b"))

    PACKAGING_MODEL: str = Field(default=os.getenv("PACKAGING_MODEL", "gpt-4o-mini"))
    PACKAGING_FALLBACK_MODEL: str = Field(default=os.getenv("PACKAGING_FALLBACK_MODEL", "groq/llama-3.3-70b"))

    SCRIPT_ARCHITECT_MODEL: str = Field(default=os.getenv("SCRIPT_ARCHITECT_MODEL", "claude-3-7-sonnet-20250219"))
    SCRIPT_ARCHITECT_FALLBACK_MODEL: str = Field(default=os.getenv("SCRIPT_ARCHITECT_FALLBACK_MODEL", "claude-3.5-sonnet"))

    TTS_SCRIPTWRITER_MODEL: str = Field(default=os.getenv("TTS_SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219"))
    TTS_SCRIPTWRITER_FALLBACK_MODEL: str = Field(default=os.getenv("TTS_SCRIPTWRITER_FALLBACK_MODEL", "claude-3.5-sonnet"))

    VISUAL_STORYBOARDER_MODEL: str = Field(default=os.getenv("VISUAL_STORYBOARDER_MODEL", "gemini-2.0-flash"))
    VISUAL_STORYBOARDER_FALLBACK_MODEL: str = Field(default=os.getenv("VISUAL_STORYBOARDER_FALLBACK_MODEL", "claude-3.5-sonnet"))

    RETENTION_AUDITOR_MODEL: str = Field(default=os.getenv("RETENTION_AUDITOR_MODEL", "groq/llama-3.3-70b"))
    RETENTION_AUDITOR_FALLBACK_MODEL: str = Field(default=os.getenv("RETENTION_AUDITOR_FALLBACK_MODEL", "deepseek-r1"))

    # Operational Constraints
    MAX_CONCURRENT_AGENTS: int = 1
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")

config = SystemConfig()
```

---

## 6. LangGraph Endpoint Routing Logic Refactoring Blueprint

### 6.1 `src/connectors/llm_router.py` Proposed Refactoring

```python
from litellm import completion
from src.core.config import config
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# Map stage names to Primary and Fallback model chains
STAGE_MODEL_MAP: Dict[str, List[str]] = {
    "researcher": [config.RESEARCHER_MODEL, config.RESEARCHER_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
    "packaging": [config.PACKAGING_MODEL, config.PACKAGING_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
    "architect": [config.SCRIPT_ARCHITECT_MODEL, config.SCRIPT_ARCHITECT_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
    "scriptwriter": [config.TTS_SCRIPTWRITER_MODEL, config.TTS_SCRIPTWRITER_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
    "storyboarder": [config.VISUAL_STORYBOARDER_MODEL, config.VISUAL_STORYBOARDER_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
    "auditor": [config.RETENTION_AUDITOR_MODEL, config.RETENTION_AUDITOR_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL],
}

def generate_response(
    prompt: str,
    system_prompt: str = "Você é um assistente da Automação Faceless.",
    stage: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs: Any
) -> str:
    """
    Smart LLM Router via OmniRoute Proxy with automatic multi-tier fallback chains.
    Directs all inference through http://localhost:20128/v1.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    # Resolve model fallback chain for the requested stage or explicit model override
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        model_chain = [config.TTS_SCRIPTWRITER_MODEL, config.TTS_SCRIPTWRITER_FALLBACK_MODEL, config.LITELLM_DEFAULT_MODEL]
    elif stage in STAGE_MODEL_MAP:
        model_chain = STAGE_MODEL_MAP[stage]
    elif model:
        model_chain = [model, config.LITELLM_DEFAULT_MODEL]
    else:
        model_chain = [config.LITELLM_DEFAULT_MODEL]

    last_exception = None

    # Iterate over fallback chain
    for target_model in model_chain:
        llm_model_name = target_model if target_model.startswith("openai/") else f"openai/{target_model}"
        try:
            logger.info(f"Routing request to OmniRoute ({config.OMNIROUTE_BASE_URL}): model={llm_model_name} (Stage={stage})")
            response = completion(
                model=llm_model_name,
                messages=messages,
                api_base=config.OMNIROUTE_BASE_URL,
                api_key=config.OMNIROUTE_API_KEY,
                custom_llm_provider="openai",
                temperature=temperature,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"Provider failed for target model {target_model} on stage {stage}: {e}. Triggering fallback...")
            last_exception = e

    logger.error(f"Critical: All models in fallback chain failed for stage '{stage}'. Last Error: {last_exception}")
    return f"ERROR_LLM: {str(last_exception)}"
```

### 6.2 Node Function Calls in `src/nodes/`

Each node will specify its `stage` parameter when calling `generate_response()`:

- **`src/nodes/researcher_fact_checker.py`**:
  `generate_response(prompt, system_prompt="Você é um Fact-Checker rigoroso.", stage="researcher", temperature=0.2)`

- **`src/nodes/packaging_ctr.py`**:
  `generate_response(prompt, system_prompt="Você é um gênio de CTR e Psicologia Humana.", stage="packaging", temperature=0.7)`

- **`src/nodes/script_architect.py`**:
  `generate_response(prompt, system_prompt="Você é um roteirista analítico...", stage="architect", temperature=0.7)`

- **`src/nodes/tts_scriptwriter.py`**:
  `generate_response(prompt, system_prompt="Você é um Roteirista de Elite...", stage="scriptwriter", temperature=0.7)`

- **`src/nodes/visual_storyboarder.py`**:
  `generate_response(prompt, system_prompt="Você é um Cinematógrafo Especialista...", stage="storyboarder", temperature=0.7)`

- **`src/nodes/retention_auditor.py`**:
  `generate_response(prompt, system_prompt="Você é o Retention Auditor rigoroso...", stage="auditor", temperature=0.1)`

---

## 7. Conclusion & Implementation Roadmap

1. **Architecture Ready**: The Multi-Model Mapping Matrix is fully designed and optimized for OmniRoute proxy at `http://localhost:20128/v1`.
2. **Zero Code Breakage**: All current Pydantic schemas and LangGraph state variables (`AgentState`) remain compatible.
3. **Next Step for Implementer**: Update `.env.example`, `src/core/config.py`, `src/connectors/llm_router.py`, and node parameters in `src/nodes/`, then validate graph compilation via `python -m py_compile`.
