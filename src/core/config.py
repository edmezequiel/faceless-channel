import os
from pydantic import BaseModel, Field

class SystemConfig(BaseModel):
    """
    Configurações globais do sistema Faceless, focadas em otimização
    de RAM (8GB max) e fallback de modelos.
    """
    # Roteamento de Modelos (Ollama Local vs API Nuvem)
    USE_LOCAL_LLM: bool = Field(
        default=os.getenv("USE_LOCAL_LLM", "true").lower() == "true",
        description="Força o roteamento primário para Ollama local (Economia de recursos)."
    )
    OLLAMA_BASE_URL: str = Field(default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
    
    # Restrições de Concorrência (evita estouro de RAM)
    MAX_CONCURRENT_AGENTS: int = 1
    
    # Caminhos
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")
    
config = SystemConfig()
