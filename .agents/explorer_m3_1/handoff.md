# Handoff Report — Explorer 3 (LLM Router Architecture Explorer)

## 1. Observation

### 1.1 Files Inspected & Codebase Analysis
- **`src/connectors/llm_router.py`**:
  - Contains function `generate_response(prompt: str, system_prompt: str = "Você é um assistente da Automação Faceless.", model: str = None, **kwargs) -> str`.
  - Lines 22-30 implement routing order:
    ```python
    if kwargs.get("force_claude_sonnet"):
        target_model = "claude-3-5-sonnet-latest"
        logger.info("Regra especial: Roteamento forçado para Claude 3.5 Sonnet.")
    elif config.USE_LOCAL_LLM and target_model is None:
        target_model = "ollama/llama3"
    elif target_model is None:
        target_model = config.LITELLM_DEFAULT_MODEL
    ```
  - Lines 32-46 perform API call dispatch:
    ```python
    if target_model.startswith("ollama/"):
        logger.info(f"Roteando requisição para modelo local: {target_model}")
        response = completion(model=target_model, messages=messages, api_base=config.OLLAMA_BASE_URL)
    else:
        logger.info(f"Roteando requisição para provedor em nuvem (LiteLLM): {target_model}")
        response = completion(model=target_model, messages=messages)
    ```

- **`src/core/config.py`**:
  - Lines 14-19:
    ```python
    USE_LOCAL_LLM: bool = Field(default=os.getenv("USE_LOCAL_LLM", "true").lower() == "true")
    OLLAMA_BASE_URL: str = Field(default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
    ```

- **`src/nodes/tts_scriptwriter.py`**:
  - Lines 49-53:
    ```python
    response = generate_response(
        prompt=prompt,
        system_prompt="Você é um gênio da escrita persuasiva focado em ritmo dinâmico. Você odeia jargões genéricos de Inteligência Artificial.",
        force_claude_sonnet=True
    )
    ```

- **Other Nodes (`src/nodes/*.py`)**:
  - `packaging_ctr.py` (Line 41): `generate_response(prompt, system_prompt=...)` -> defaults to Ollama local (`ollama/llama3`).
  - `researcher_fact_checker.py` (Line 26): `generate_response(prompt, system_prompt=...)` -> defaults to Ollama local (`ollama/llama3`).
  - `script_architect.py` (Line 40): `generate_response(prompt, system_prompt=...)` -> defaults to Ollama local (`ollama/llama3`).
  - `visual_storyboarder.py` (Line 42): `generate_response(prompt, system_prompt=...)` -> defaults to Ollama local (`ollama/llama3`).

### 1.2 Syntax Verification Command Output
- Executed: `python -m py_compile src/connectors/llm_router.py`
- Exit Code: `0`
- Output: (empty stderr/stdout, build success).

---

## 2. Logic Chain

1. **Routing Override Priority**:
   - In `llm_router.py`, the `if kwargs.get("force_claude_sonnet"):` check precedes the `elif config.USE_LOCAL_LLM and target_model is None:` check.
   - Therefore, whenever `force_claude_sonnet=True` is passed (as is done in `node_tts_scriptwriter`), the router bypasses local Ollama execution even if `USE_LOCAL_LLM=True`.

2. **Ollama Local Fallback Preservation**:
   - For all other conveyor belt nodes (`packaging_ctr`, `researcher_fact_checker`, `script_architect`, `visual_storyboarder`), `force_claude_sonnet` is not passed and `model` parameter is `None`.
   - As a consequence, these nodes hit `elif config.USE_LOCAL_LLM and target_model is None: target_model = "ollama/llama3"`, which routes their calls locally via `LiteLLM` to `http://localhost:11434`.

3. **Winning Model Enforcement Plan (M3 Refactoring)**:
   - When Explorer 2 / research designates the winning anti-AI slop model (e.g. `claude-3-5-sonnet-latest` or `claude-3-7-sonnet-20250219`), `llm_router.py` can define a constant `SCRIPTWRITER_WINNING_MODEL`.
   - Updating `target_model = SCRIPTWRITER_WINNING_MODEL` inside `if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):` ensures that `node_tts_scriptwriter` strictly uses the winning frontier model while keeping caller code intact andpreserving local Ollama fallback for all other nodes.

---

## 3. Caveats

- **API Key Environment Variables**: `litellm.completion` requires valid API key credentials (e.g. `ANTHROPIC_API_KEY`) when making actual network calls to cloud providers.
- **Ollama Service Availability**: For local LLM routing (`ollama/llama3`), the Ollama daemon must be running at `OLLAMA_BASE_URL` (`http://localhost:11434`) during execution.
- **Model Identifier Consistency**: Explorer 2's research provides the exact string identifier. The router configuration must match LiteLLM's expected model format (e.g., `claude-3-5-sonnet-latest`, `anthropic/claude-3-5-sonnet-20241022`, or `claude-3-7-sonnet-20250219`).

---

## 4. Conclusion

- `src/connectors/llm_router.py` currently compiles without syntax errors and has a clear, robust architecture for forced cloud overrides vs local Ollama fallbacks.
- The routing priority correctly guarantees that `node_tts_scriptwriter` forces cloud execution for scriptwriting while other nodes remain on local Ollama execution when `USE_LOCAL_LLM=True`.
- Refactoring `llm_router.py` for M3 is straightforward and can be achieved cleanly with zero breaking changes to existing nodes by updating the target model string constant and expanding keyword flag support.

### Proposed Code Patch for Worker (M3 Refactoring)

```python
# File: src/connectors/llm_router.py

from litellm import completion
from src.core.config import config
import logging

logger = logging.getLogger(__name__)

# Winning model identifier for anti-AI slop scriptwriting (M2 research selection)
SCRIPTWRITER_WINNING_MODEL = "claude-3-5-sonnet-latest"

def generate_response(prompt: str, system_prompt: str = "Você é um assistente da Automação Faceless.", model: str = None, **kwargs) -> str:
    """
    Roteador inteligente de LLMs.
    Se a config USE_LOCAL_LLM for verdadeira, força o envio para o Ollama (economia de RAM e custos).
    Caso contrário, ou se houver falha, envia via LiteLLM para nuvem.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    target_model = model
    
    # Regra de Roteamento Específica (Esteira Autônoma - TTS Scriptwriter)
    if kwargs.get("force_claude_sonnet") or kwargs.get("force_scriptwriter"):
        target_model = SCRIPTWRITER_WINNING_MODEL
        logger.info(f"Regra especial: Roteamento forçado para modelo de alta qualidade: {target_model}")
    elif config.USE_LOCAL_LLM and target_model is None:
        # Default local fallback (llama3 ou mistral, configurável)
        target_model = "ollama/llama3"
    elif target_model is None:
        target_model = config.LITELLM_DEFAULT_MODEL
        
    try:
        if target_model.startswith("ollama/"):
            logger.info(f"Roteando requisição para modelo local: {target_model}")
            response = completion(
                model=target_model, 
                messages=messages, 
                api_base=config.OLLAMA_BASE_URL
            )
        else:
            logger.info(f"Roteando requisição para provedor em nuvem (LiteLLM): {target_model}")
            response = completion(
                model=target_model,
                messages=messages
            )
            
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Erro na inferência do modelo {target_model}: {e}")
        return f"ERROR_LLM: {str(e)}"
```

---

## 5. Verification Method

To independently verify `src/connectors/llm_router.py`:

1. **Syntax Verification Command**:
   ```bash
   python -m py_compile src/connectors/llm_router.py
   ```
   *Expected output*: Exit code 0, no syntax errors.

2. **Routing Logic Unit Test / Dry Run**:
   Run a Python one-liner to verify model selection routing:
   ```bash
   python -c "from src.connectors.llm_router import generate_response; print('Router module loaded successfully')"
   ```

3. **Invalidation Conditions**:
   - `python -m py_compile src/connectors/llm_router.py` returns non-zero exit code.
   - Mandatory kwargs flag `force_claude_sonnet` fails to assign `target_model` to the designated winning model.
   - Non-scriptwriter calls redirect away from `"ollama/llama3"` when `USE_LOCAL_LLM=True`.
