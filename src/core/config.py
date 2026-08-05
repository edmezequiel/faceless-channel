import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env, caso exista
load_dotenv()

class SystemConfig(BaseModel):
    """
    Configurações globais do sistema Faceless, integradas à arquitetura OmniRoute + LiteLLM.
    """
    # Configurações do Roteador OmniRoute (Proxy Central de LLMs)
    OMNIROUTE_BASE_URL: str = Field(
        default=os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1"),
        description="Endpoint base da API OpenAI-compatible do OmniRoute"
    )
    OMNIROUTE_API_KEY: str = Field(
        default=os.getenv("OMNIROUTE_API_KEY", "sk-omniroute-master"),
        description="Chave de autenticação mestre do OmniRoute"
    )
    
    # Modelo padrão e Modelo Roteirista (Anti-AI Slop)
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
    SCRIPTWRITER_MODEL: str = Field(default=os.getenv("SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219"))
    
    # Restrições de Concorrência
    MAX_CONCURRENT_AGENTS: int = 1
    
    # Caminhos
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")
    
config = SystemConfig()
