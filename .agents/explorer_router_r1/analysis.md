# LangGraph Router & Engine Architecture Audit & Refactoring Design (Milestone M3)

**Author:** `teamwork_preview_explorer` (explorer_router_r1)  
**Date:** 2026-08-05  
**Target System:** EDM ARCHETYPE LAB (`FACELESS CHANNEL`)  
**Scope:** `src/connectors/llm_router.py`, `src/core/config.py`, `src/core/engine.py`, and all node modules in `src/nodes/`.

---

## 1. Executive Summary

This document presents the complete architectural audit and refactoring specification for the LLM Router and LangGraph Engine in `EDM ARCHETYPE LAB`. 

The primary objective is to upgrade `src/connectors/llm_router.py` from a simple pass-through LiteLLM wrapper into a resilient, dynamic multi-model routing engine connected to the **OmniRoute proxy** (`http://localhost:20128/v1`). The refactored router will dynamically select models based on agent roles across the 6-stage content pipeline, execute automatic model fallback chains when a provider fails, and guarantee 100% syntax compliance (`python -m py_compile`) across all graph nodes and `src/core/engine.py`.

---

## 2. Current Architecture Audit

### 2.1 `src/connectors/llm_router.py` Audit
- **Current Behavior:** Imports `completion` from `litellm` and exposes `generate_response(prompt, system_prompt, model, **kwargs)`.
- **Deficiencies:**
  1. **Single-Attempt Failure:** If OmniRoute or an upstream provider returns an error (429 rate limit, 500 server error, timeout), the router catches the exception and immediately returns `"ERROR_LLM: <str(e)>"`. This causes downstream Pydantic parsers (`PydanticOutputParser`) to fail with `OutputParserException`.
  2. **No Role-Aware Routing Matrix:** Lacks built-in knowledge of agent roles (`researcher`, `packaging`, `architect`, `scriptwriter`, `storyboarder`, `auditor`). It only checks a legacy kwarg (`force_claude_sonnet` / `force_scriptwriter`), otherwise falling back to a single global default (`config.LITELLM_DEFAULT_MODEL`).
  3. **No Dynamic Fallback Chain:** Does not support defining or iterating over fallback models per agent role.

### 2.2 `src/core/config.py` Audit
- **Current Behavior:** Defines `OMNIROUTE_BASE_URL` (`http://localhost:20128/v1`), `OMNIROUTE_API_KEY` (`sk-omniroute-master`), `LITELLM_DEFAULT_MODEL` (`gpt-4o-mini`), and `SCRIPTWRITER_MODEL` (`claude-3-7-sonnet-20250219`).
- **Deficiencies:** Does not define a centralized `MODEL_ROUTING_MATRIX` for per-role model selection and fallback lists.

### 2.3 `src/nodes/` Audit
Currently, 6 pipeline nodes + 2 flow control nodes exist in `src/nodes/`:
1. `src/nodes/intake.py`: Local Pydantic validation (no LLM call yet).
2. `src/nodes/orchestrator.py`: Deterministic state router (no LLM call yet).
3. `src/nodes/researcher_fact_checker.py`: Calls `generate_response(prompt, system_prompt=...)` without passing model or role (defaults to `gpt-4o-mini`).
4. `src/nodes/packaging_ctr.py`: Calls `generate_response(prompt, system_prompt=...)` without passing model or role (defaults to `gpt-4o-mini`).
5. `src/nodes/script_architect.py`: Calls `generate_response(prompt, system_prompt=...)` without passing model or role (defaults to `gpt-4o-mini`).
6. `src/nodes/tts_scriptwriter.py`: Calls `generate_response(prompt, system_prompt=..., force_claude_sonnet=True)`.
7. `src/nodes/visual_storyboarder.py`: Calls `generate_response(prompt, system_prompt=...)` without passing model or role (defaults to `gpt-4o-mini`).
8. `src/nodes/retention_auditor.py`: Runs heuristic Python validations on script prose and storyboard metadata (no direct LLM call yet).

### 2.4 `src/core/engine.py` Audit
- Imports all 8 node functions, builds `StateGraph(AgentState)`, wires entry points, conditional edges, closed-loop retries, and compiles cleanly.

---

## 3. OmniRoute Multi-Model Routing Matrix Design

To leverage the 30+ providers supported by OmniRoute, each pipeline stage is assigned a specialized primary model and fallback hierarchy:

| Pipeline Stage / Agent Role | Primary Model | Fallback Models | Rationale |
|---|---|---|---|
| **`researcher`** (Researcher & Fact-Checker) | `gemini-2.0-flash` | `['groq/llama-3.3-70b', 'gpt-4o-mini']` | 1M token context window, fast retrieval, zero cost for high volume. |
| **`packaging`** (Packaging & CTR) | `gpt-4o-mini` | `['groq/llama-3.3-70b', 'gemini-2.0-flash']` | High speed and strict adherence to JSON schema output. |
| **`architect`** (Script Architect) | `claude-3-7-sonnet-20250219` | `['claude-3-5-sonnet', 'gpt-4o']` | Sophisticated narrative structure, open-loop design. |
| **`scriptwriter`** (TTS Scriptwriter) | `claude-3-7-sonnet-20250219` | `['claude-3-5-sonnet', 'gpt-4o']` | Highest human prose quality, strict Anti-AI Slop enforcement. |
| **`storyboarder`** (Visual Storyboarder) | `gemini-2.0-flash` | `['claude-3-5-sonnet', 'gpt-4o-mini']` | Multi-layered visual detail, spatial outpainting descriptions. |
| **`auditor`** (Retention Auditor) | `groq/llama-3.3-70b` | `['deepseek-r1', 'gpt-4o-mini']` | Fast, strict logical reasoning for retention scoring & feedback. |
| **`default`** (Fallback / General) | `gpt-4o-mini` | `['gemini-2.0-flash', 'groq/llama-3.3-70b']` | Reliable baseline lightweight model. |

---

## 4. Refactoring Diffs & Specifications

### 4.1 `src/core/config.py` Update Proposal

Add `MODEL_ROUTING_MATRIX` to `SystemConfig` in `src/core/config.py`:

```python
from typing import Dict, List, Any

class SystemConfig(BaseModel):
    # Endpoint base e chave do OmniRoute Proxy
    OMNIROUTE_BASE_URL: str = Field(
        default=os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1"),
        description="Endpoint base da API OpenAI-compatible do OmniRoute"
    )
    OMNIROUTE_API_KEY: str = Field(
        default=os.getenv("OMNIROUTE_API_KEY", "sk-omniroute-master"),
        description="Chave de autenticação mestre do OmniRoute"
    )
    
    # Modelos Globais
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
    SCRIPTWRITER_MODEL: str = Field(default=os.getenv("SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219"))
    
    # Matriz Multi-Modelo por Função do Agente (OmniRoute Gateway)
    MODEL_ROUTING_MATRIX: Dict[str, Dict[str, Any]] = Field(
        default={
            "researcher": {
                "primary": os.getenv("MODEL_RESEARCHER", "gemini-2.0-flash"),
                "fallbacks": ["groq/llama-3.3-70b", "gpt-4o-mini"]
            },
            "packaging": {
                "primary": os.getenv("MODEL_PACKAGING", "gpt-4o-mini"),
                "fallbacks": ["groq/llama-3.3-70b", "gemini-2.0-flash"]
            },
            "architect": {
                "primary": os.getenv("MODEL_ARCHITECT", "claude-3-7-sonnet-20250219"),
                "fallbacks": ["claude-3-5-sonnet", "gpt-4o"]
            },
            "scriptwriter": {
                "primary": os.getenv("MODEL_SCRIPTWRITER", "claude-3-7-sonnet-20250219"),
                "fallbacks": ["claude-3-5-sonnet", "gpt-4o"]
            },
            "storyboarder": {
                "primary": os.getenv("MODEL_STORYBOARDER", "gemini-2.0-flash"),
                "fallbacks": ["claude-3-5-sonnet", "gpt-4o-mini"]
            },
            "auditor": {
                "primary": os.getenv("MODEL_AUDITOR", "groq/llama-3.3-70b"),
                "fallbacks": ["deepseek-r1", "gpt-4o-mini"]
            },
            "default": {
                "primary": os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"),
                "fallbacks": ["gemini-2.0-flash", "groq/llama-3.3-70b"]
            }
        }
    )
    
    MAX_CONCURRENT_AGENTS: int = 1
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")
```

---

### 4.2 `src/connectors/llm_router.py` Proposed Full Implementation

```python
import logging
import time
from typing import Optional, List, Tuple
from litellm import completion
from src.core.config import config

logger = logging.getLogger(__name__)

SCRIPTWRITER_WINNING_MODEL = config.SCRIPTWRITER_MODEL


def resolve_model_chain(
    model: Optional[str] = None,
    agent_role: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    **kwargs
) -> Tuple[str, List[str]]:
    """
    Resolve o modelo primário e a lista de fallbacks considerando:
    1. Kwargs legados (force_claude_sonnet / force_scriptwriter)
    2. Modelo explicitamente passado
    3. Papel do agente (agent_role) registrado na matriz de roteamento
    4. Modelo padrão global
    """
    # 1. Compatibilidade com chamadas legadas
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        primary = getattr(config, "SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219")
        chain = fallback_models or ["claude-3-5-sonnet", "gpt-4o"]
        return primary, [f for f in chain if f != primary]

    # 2. Modelo explícito informado pelo chamador
    if model:
        primary = model
        chain = fallback_models or ["gpt-4o-mini", "gemini-2.0-flash"]
        return primary, [f for f in chain if f != primary]

    # 3. Mapeamento por Agent Role via config.MODEL_ROUTING_MATRIX
    if agent_role and hasattr(config, "MODEL_ROUTING_MATRIX") and agent_role in config.MODEL_ROUTING_MATRIX:
        role_cfg = config.MODEL_ROUTING_MATRIX[agent_role]
        primary = role_cfg["primary"]
        chain = fallback_models or role_cfg.get("fallbacks", [])
        return primary, [f for f in chain if f != primary]

    # 4. Fallback padrão global
    primary = getattr(config, "LITELLM_DEFAULT_MODEL", "gpt-4o-mini")
    chain = fallback_models or ["gemini-2.0-flash", "groq/llama-3.3-70b"]
    return primary, [f for f in chain if f != primary]


def generate_response(
    prompt: str,
    system_prompt: str = "Você é um assistente da Automação Faceless.",
    model: Optional[str] = None,
    agent_role: Optional[str] = None,
    fallback_models: Optional[List[str]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    max_retries_per_model: int = 1,
    **kwargs
) -> str:
    """
    Roteador inteligente de LLMs via OmniRoute proxy (http://localhost:20128/v1) + LiteLLM.
    Suporta seleção dinâmica de modelos por papel de agente e fallback automático em cascata.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    primary_model, fallbacks = resolve_model_chain(
        model=model,
        agent_role=agent_role,
        fallback_models=fallback_models,
        **kwargs
    )

    candidate_models = [primary_model] + [f for f in fallbacks if f != primary_model]
    errors = []

    for candidate in candidate_models:
        llm_model_name = candidate if candidate.startswith("openai/") else f"openai/{candidate}"

        for attempt in range(1, max_retries_per_model + 1):
            try:
                logger.info(
                    f"Roteando via OmniRoute ({config.OMNIROUTE_BASE_URL}) | "
                    f"Role: {agent_role or 'general'} | Modelo: {candidate} (Tentativa {attempt}/{max_retries_per_model})"
                )

                completion_kwargs = {
                    "model": llm_model_name,
                    "messages": messages,
                    "api_base": config.OMNIROUTE_BASE_URL,
                    "api_key": config.OMNIROUTE_API_KEY,
                    "custom_llm_provider": "openai",
                    "temperature": temperature,
                }
                if max_tokens:
                    completion_kwargs["max_tokens"] = max_tokens

                response = completion(**completion_kwargs)
                content = response.choices[0].message.content
                if content:
                    return content
                else:
                    raise ValueError("Resposta do LLM retornou vazia.")

            except Exception as e:
                err_msg = f"Modelo '{candidate}' falhou na tentativa {attempt}: {str(e)}"
                logger.warning(f"OmniRoute Warning: {err_msg}")
                errors.append(err_msg)
                if attempt < max_retries_per_model:
                    time.sleep(1)

        logger.warning(f"Alternando para fallback após falha total no modelo '{candidate}'.")

    final_error = f"ERROR_LLM: Todos os modelos falharam na rota OmniRoute. Histórico: {'; '.join(errors)}"
    logger.error(final_error)
    return final_error
```

---

### 4.3 Node Calls Code Changes

#### 1. `src/nodes/researcher_fact_checker.py`
```python
# ANTES:
factual_context = generate_response(prompt, system_prompt="Você é um Fact-Checker rigoroso.")

# DEPOIS:
factual_context = generate_response(
    prompt,
    system_prompt="Você é um Fact-Checker rigoroso.",
    agent_role="researcher"
)
```

#### 2. `src/nodes/packaging_ctr.py`
```python
# ANTES:
response = generate_response(prompt, system_prompt="Você é um gênio de CTR e Psicologia Humana.")

# DEPOIS:
response = generate_response(
    prompt,
    system_prompt="Você é um gênio de CTR e Psicologia Humana.",
    agent_role="packaging"
)
```

#### 3. `src/nodes/script_architect.py`
```python
# ANTES:
response = generate_response(prompt, system_prompt="Você é um roteirista analítico especializado em gráficos de retenção (AVD).")

# DEPOIS:
response = generate_response(
    prompt,
    system_prompt="Você é um roteirista analítico especializado em gráficos de retenção (AVD).",
    agent_role="architect"
)
```

#### 4. `src/nodes/tts_scriptwriter.py`
```python
# ANTES:
response = generate_response(
    prompt=prompt,
    system_prompt="Você é um gênio da escrita persuasiva focado em ritmo dinâmico. Você odeia jargões genéricos de Inteligência Artificial.",
    force_claude_sonnet=True
)

# DEPOIS:
response = generate_response(
    prompt=prompt,
    system_prompt="Você é um gênio da escrita persuasiva focado em ritmo dinâmico. Você odeia jargões genéricos de Inteligência Artificial.",
    agent_role="scriptwriter"
)
```

#### 5. `src/nodes/visual_storyboarder.py`
```python
# ANTES:
response = generate_response(prompt, system_prompt="Você é um Cinematógrafo Especialista em AI Video.")

# DEPOIS:
response = generate_response(
    prompt,
    system_prompt="Você é um Cinematógrafo Especialista em AI Video.",
    agent_role="storyboarder"
)
```

#### 6. `src/nodes/retention_auditor.py`
Optional qualitative LLM verification call (if enabled):
```python
# Nova funcionalidade opcional para auditoria qualitativa:
response = generate_response(
    prompt=audit_prompt,
    system_prompt="Você é o Retention Auditor e Guardião de Qualidade do canal.",
    agent_role="auditor"
)
```

#### 7. `src/nodes/intake.py` and `src/nodes/orchestrator.py`
No syntax changes required for pure rule routing; if LLM classification is enabled, supply `agent_role="researcher"` or `agent_role="orchestrator"`.

#### 8. `src/core/engine.py`
No internal signature changes needed. `build_graph()` imports node functions directly and compiles cleanly.

---

## 5. Verification Method

To verify that the refactored files satisfy all syntax and compilation constraints:

1. **Compilation Command:**
   ```bash
   python -m py_compile src/connectors/llm_router.py src/core/config.py src/core/engine.py src/nodes/intake.py src/nodes/orchestrator.py src/nodes/researcher_fact_checker.py src/nodes/packaging_ctr.py src/nodes/script_architect.py src/nodes/tts_scriptwriter.py src/nodes/visual_storyboarder.py src/nodes/retention_auditor.py
   ```
2. **StateGraph Build Verification:**
   ```bash
   python -c "from src.core.engine import build_graph; g = build_graph(); print('Graph compiled successfully:', g is not None)"
   ```

---

## 6. Summary of Impact

- **Zero Breaking Changes:** Maintains full signature backward compatibility for existing callers.
- **Fail-safe Operations:** Upstream timeouts or quota failures on primary models automatically degrade to backup providers via OmniRoute proxy.
- **Role Optimization:** Each agent node utilizes the optimal LLM for its workload (e.g. Gemini 2.0 Flash for 1M context research/storyboarding, Claude 3.7 Sonnet for Anti-AI Slop scriptwriting, Groq Llama 3.3 70B for fast packaging/auditing).
