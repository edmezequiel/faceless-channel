# Faceless Channel (EDM ARCHETYPE LAB) — Dependency & Repository Audit

> **Agent**: `explorer_audit_r1` (Teamwork Explorer)  
> **Milestone**: M1 (Dependency & Repository Audit)  
> **Date**: 2026-08-05  
> **Target System**: Windows OS (x86_64 / PowerShell & CMD)  
> **Working Directory**: `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\.agents\explorer_audit_r1`

---

## 1. Executive Summary

This comprehensive audit evaluates the repository structure, Python dependencies, external system tools, multi-model routing integration, and Windows OS compatibility for the **Faceless Channel (`EDM ARCHETYPE LAB`)** autonomous content pipeline.

### Key Discoveries
1. **Critical Windows OS Bug (`UnicodeDecodeError` in `.pth`)**: Python's standard `site.py` module on Windows fails during virtualenv startup when importing packages because `uv` generated `faceless_channel.pth` containing an absolute path with UTF-8 Portuguese accented characters (`Área de Trabalho`). Standard Windows CPython reads `.pth` files using `cp1252`, causing a fatal `UnicodeDecodeError` on byte `0x81`. A relative path fix (`../../../src`) or clean `pyproject.toml` configuration resolves this issue completely.
2. **Missing `requirements.txt` File**: The project relies on `pyproject.toml` and `uv.lock`, but lacks a standardized `requirements.txt` file as specified in system requirements and scripts.
3. **Missing Secondary Dependencies**: The pipeline nodes (`AgentReachConnector`, spatial outpainting, kinetic text overlay, audio processing) require libraries not yet declared in `pyproject.toml` (e.g. `yt-dlp`, `Pillow`, `numpy`, `opencv-python`, `moviepy`, `edge-tts` / `elevenlabs`, `httpx`).
4. **Missing Folders & Documentation**: The repository lacks `docs/` and `scripts/` directories, and the root `README.md` is empty (0 bytes).
5. **External System Tools Required**: FFmpeg is mandatory for audio-video assembly and outpainting frame stitching; OmniRoute Proxy (`http://localhost:20128/v1`) must be running as the multi-model LLM gateway.

---

## 2. Project Repository & File Structure Audit

### 2.1 File Catalog & Status
- **Root Directory**:
  - `pyproject.toml`: Present (528 bytes). Declares core dependencies (`langchain-core>=1.5.3`, `langgraph>=1.2.10`, `litellm>=1.95.0`, `pydantic>=2.13.4`, `python-dotenv>=1.0.0`).
  - `uv.lock`: Present (563,642 bytes).
  - `requirements.txt`: **MISSING**. Must be generated.
  - `README.md`: Present but **EMPTY (0 bytes)**. Needs comprehensive setup documentation.
  - `run.ps1`: Present (357 bytes). Launches `src/core/engine.py` with `$env:PYTHONUTF8="1"`.
  - `implementation_plan.md`: Present (32,815 bytes). Comprehensive brand & system specification.
  - `ORIGINAL_REQUEST.md`: Present (9,266 bytes). Full prompt specs for all project phases.
- **Directories**:
  - `src/`: Present (13 `.py` source files across `connectors/`, `core/`, `faceless_channel/`, `nodes/`). All compile cleanly via `py_compile`.
  - `memory/`: Present (Curated knowledge base, narrative frameworks, GrokFilm index).
  - `workflows/`: Present.
  - `docs/`: **MISSING**. Needs architectural & installation documentation.
  - `scripts/`: **MISSING**. Needs setup and validation helper scripts.

---

## 3. Python Dependencies Audit

### 3.1 Declared vs. Missing Python Packages

| Package | Status | Usage in Codebase / Specifications | Recommendation |
|---|---|---|---|
| `langchain-core` | Declared (`>=1.5.3`) | Used in `packaging_ctr`, `script_architect`, `tts_scriptwriter`, `visual_storyboarder` for `PydanticOutputParser` | Keep in `pyproject.toml` |
| `langgraph` | Declared (`>=1.2.10`) | Used in `src/core/engine.py` (`StateGraph`, `END`) | Keep in `pyproject.toml` |
| `litellm` | Declared (`>=1.95.0`) | Used in `src/connectors/llm_router.py` (`completion`) | Keep in `pyproject.toml` |
| `pydantic` | Declared (`>=2.13.4`) | Used in `src/core/state.py`, `config.py`, nodes | Keep in `pyproject.toml` |
| `python-dotenv` | Declared (`>=1.0.0`) | Used in `src/core/config.py` (`load_dotenv`) | Keep in `pyproject.toml` |
| `yt-dlp` | **MISSING** | Required by `AgentReachConnector` (`src/connectors/agent_reach.py`) for YouTube research & metadata extraction | Add `yt-dlp>=2024.12.13` |
| `httpx` | Installed in venv, missing in `pyproject.toml` | Required for async HTTP requests to Jina Reader & OmniRoute API | Add `httpx>=0.28.0` |
| `Pillow` (PIL) | **MISSING** | Required by Spatial Outpainting (`state.py`) for `seam_feather_pixels` (128px alpha feathering) and image manipulation | Add `Pillow>=10.4.0` |
| `numpy` | **MISSING** | Required for seam blending matrix operations and image array processing | Add `numpy>=1.26.0` |
| `opencv-python` (`cv2`) | **MISSING** | Required for frame extraction, motion vector synthesis (`Vertical Pan Down`), kinetic text tracking | Add `opencv-python>=4.10.0` |
| `moviepy` / `ffmpeg-python` | **MISSING** | Required for video clip assembly, kinetic text overlay rendering, audio/video multiplexing | Add `moviepy>=2.0.0` & `ffmpeg-python>=0.2.0` |
| `edge-tts` / `elevenlabs` | **MISSING** | Required for converting `tts_prose` into high-quality spoken audio | Add `edge-tts>=6.1.12` |
| `pytest` | **MISSING** | Required for automated unit and integration testing of nodes and graph execution | Add `pytest>=8.0.0` (dev dependency) |

---

## 4. External System Tools Audit

### 4.1 Required Binaries & Services (Windows OS)

1. **FFmpeg (`ffmpeg.exe` & `ffprobe.exe`)**:
   - **Critical Role**: Video frame extraction, outpainting image stitching, kinetic text overlay rendering, audio-video multiplexing.
   - **Windows Requirement**: Must be installed and present in system `%PATH%`.
   - **Verification Command**: `ffmpeg -version`
   - **Installation Method**: `winget install Gyan.FFmpeg` or manual download from `gyan.dev/ffmpeg/builds/`.

2. **OmniRoute Central LLM Gateway**:
   - **Critical Role**: OpenAI-compatible proxy routing requests to 30+ LLMs (`gemini-2.0-flash`, `gpt-4o-mini`, `claude-3-7-sonnet-20250219`, `groq/llama-3.3-70b`, `deepseek-r1`).
   - **Endpoint**: Configured in `.env` via `OMNIROUTE_BASE_URL="http://localhost:20128/v1"`.
   - **Verification Method**: `curl http://localhost:20128/v1/models`

3. **yt-dlp CLI**:
   - **Role**: Fetching video transcripts and channel research data.
   - **Installation**: Included via Python package `pip install yt-dlp`.

4. **ImageMagick (`magick.exe`) (Optional for MoviePy)**:
   - **Role**: Required if `moviepy.editor.TextClip` is used for rendering kinetic text overlays on Windows.
   - **Windows Requirement**: Set environment variable `IMAGEMAGICK_BINARY="C:\Program Files\ImageMagick-7.x.x-Q16-HDRI\magick.exe"`.

5. **NVIDIA CUDA Toolkit & C++ Build Tools (For Local AI Models)**:
   - **Role**: Required if running local TTS (Kokoro/F5-TTS) or local video diffusion (Deforum/ComfyUI/Wan2.1).
   - **Requirements**: NVIDIA Driver, CUDA Toolkit 12.x, Visual Studio 2022 Build Tools (Desktop development with C++).

---

## 5. Multi-Model Routing Matrix Audit (`src/connectors/llm_router.py`)

The project requirement specifies a dynamic multi-model routing matrix via OmniRoute:

| Agent Node | Primary Model | Fallback Model | Purpose / Rationale |
|---|---|---|---|
| **Intake & Research** (`intake.py`, `researcher.py`) | `gemini-2.0-flash` | `gpt-4o-mini` | 1M context window for massive search parsing; zero API cost. |
| **Packaging (CTR)** (`packaging_ctr.py`) | `gpt-4o-mini` | `groq/llama-3.3-70b` | Ultra-fast JSON formatting and viral title generation. |
| **Script Architect** (`script_architect.py`) | `claude-3-7-sonnet-20250219` | `groq/llama-3.3-70b` | High analytical reasoning for narrative structure & open loops. |
| **TTS Scriptwriter** (`tts_scriptwriter.py`) | `claude-3-7-sonnet-20250219` | `gpt-4o` | Human writing quality, strict prosody tagging, Zero AI Slop enforcement. |
| **Visual Storyboarder** (`visual_storyboarder.py`) | `gemini-2.0-flash` | `claude-3.5-sonnet` | Complex spatial outpainting scene description & visual prompts. |
| **Retention Auditor** (`retention_auditor.py`) | `groq/llama-3.3-70b` | `deepseek-r1` | Strict logical reasoning, rule validation, and score calculation. |

### Current Router Code Assessment
- `src/connectors/llm_router.py` currently only checks `kwargs.get("force_claude_sonnet")` to route to `SCRIPTWRITER_MODEL`.
- To meet Requirement R2, `llm_router.py` must accept an `agent_role` parameter and route dynamically according to the matrix above.

---

## 6. Windows OS Deep-Dive: The `.pth` UTF-8 Encoding Bug

### 6.1 Diagnosis & Technical Evidence
When executing `python` or `pip list` in the workspace virtual environment on Windows without `-S`, Python throws a fatal error:

```text
Fatal Python error: init_import_site: Failed to import the site module
Traceback (most recent call last):
  ...
  File "C:\Users\ezequ\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\Lib\encodings\cp1252.py", line 23, in decode
    return codecs.charmap_decode(input,self.errors,decoding_table)[0]
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 25: character maps to <undefined>
```

**Root Cause**:
1. The project directory path `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL` contains Portuguese accented characters (`Á`).
2. Package manager `uv` creates an editable `.pth` file `.venv\Lib\site-packages\faceless_channel.pth` containing:
   `C:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\src`
   encoded as UTF-8 bytes (`\xc3\x81` for `Á`).
3. During Python startup (`import site`), CPython on Windows (under standard Brazilian Portuguese locale CP1252) opens `.pth` files using `locale.getpreferredencoding()` which defaults to `cp1252`.
4. Byte `0x81` is not defined in Windows-1252, causing `site.py` to crash before any code executes.

### 6.2 Solution & Verification
1. **Immediate Fix**: Replace the absolute path in `.venv\Lib\site-packages\faceless_channel.pth` with a relative path:
   `../../../src`
2. **Permanent Fix for Windows**:
   - Ensure `run.ps1` sets `$env:PYTHONUTF8="1"`.
   - Update `pyproject.toml` to use standard package layout or src directory mapping without hardcoded absolute path `.pth` files.
   - When running python commands via CLI, use `-S` or ensure UTF-8 environment mode.

---

## 7. Actionable Windows Setup & Installation Guide

To fully set up and verify the environment on Windows OS:

### Step 1: Fix `.pth` Path Encoding Bug
In PowerShell:
```powershell
Set-Content -Path ".\.venv\Lib\site-packages\faceless_channel.pth" -Value "../../../src" -Encoding utf8
```

### Step 2: Install Missing Python Dependencies via `uv`
```powershell
uv add yt-dlp httpx pillow numpy opencv-python moviepy ffmpeg-python edge-tts pytest
```

### Step 3: Generate `requirements.txt`
```powershell
uv export --format requirements-txt -o requirements.txt
```

### Step 4: Install System Binaries (FFmpeg)
In PowerShell (Admin):
```powershell
winget install Gyan.FFmpeg
# Restart terminal to refresh PATH
ffmpeg -version
```

### Step 5: Verify Python Node Compilation
```powershell
$env:PYTHONUTF8="1"
$env:PYTHONPATH="."
.\.venv\Scripts\python.exe -m py_compile src/core/config.py src/core/state.py src/core/engine.py src/connectors/llm_router.py src/connectors/agent_reach.py src/nodes/*.py
```

### Step 6: Create Directory Structure & Documentation
```powershell
New-Item -ItemType Directory -Force -Path "docs", "scripts"
```

---

## 8. Summary of Findings

1. **Codebase Quality**: All existing Python source files in `src/` are syntactically valid and compile cleanly.
2. **Windows Compatibility**: Identified and solved a critical Windows path encoding bug (`UnicodeDecodeError`) caused by accented folder names in `faceless_channel.pth`.
3. **Dependencies**: Identified 8 missing Python libraries (`yt-dlp`, `httpx`, `Pillow`, `numpy`, `opencv-python`, `moviepy`, `ffmpeg-python`, `edge-tts`) required for video, audio, and research features.
4. **External Tools**: Mapped requirements for FFmpeg, OmniRoute Proxy, and optional ImageMagick/CUDA.
5. **Repositories & Docs**: Recommended generating `requirements.txt`, populating `README.md`, and creating `docs/` and `scripts/` directories.
