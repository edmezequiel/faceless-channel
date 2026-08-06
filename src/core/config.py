import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Dict

# Carrega variáveis de ambiente do .env, caso exista
load_dotenv()

class SystemConfig(BaseModel):
    """
    Configurações globais do sistema Faceless, integradas à arquitetura OmniRoute + LiteLLM.
    Suporta roteamento multi-modelo por especialidade de agente.
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
    
    # Modelo padrão para tarefas genéricas
    LITELLM_DEFAULT_MODEL: str = Field(default=os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini"))
    
    # Modelo Roteirista Principal (Anti-AI Slop — Claude Sonnet)
    SCRIPTWRITER_MODEL: str = Field(default=os.getenv("SCRIPTWRITER_MODEL", "antigravity/claude-sonnet-4-6"))
    
    # ═══════════════════════════════════════════════════════════════
    # MATRIZ DE ESPECIALIZAÇÃO MULTI-MODELO (por função de agente)
    # ═══════════════════════════════════════════════════════════════
    # Cada agente da esteira pode ter um modelo ideal diferente,
    # roteado automaticamente via OmniRoute.
    
    RESEARCHER_MODEL: str = Field(
        default=os.getenv("RESEARCHER_MODEL", "groq/llama-3.3-70b-versatile"),
        description="Modelo para pesquisa e fact-checking (Groq 70b)"
    )
    PACKAGING_MODEL: str = Field(
        default=os.getenv("PACKAGING_MODEL", "groq/llama-3.3-70b-versatile"),
        description="Modelo para embalagem CTR"
    )
    ARCHITECT_MODEL: str = Field(
        default=os.getenv("ARCHITECT_MODEL", "antigravity/claude-sonnet-4-6"),
        description="Modelo para arquitetura de roteiro"
    )
    STORYBOARDER_MODEL: str = Field(
        default=os.getenv("STORYBOARDER_MODEL", "groq/llama-3.3-70b-versatile"),
        description="Modelo para storyboard visual"
    )
    AUDITOR_MODEL: str = Field(
        default=os.getenv("AUDITOR_MODEL", "groq/llama-3.3-70b-versatile"),
        description="Modelo para auditoria de retenção"
    )
    
    # Restrições de Concorrência
    MAX_CONCURRENT_AGENTS: int = 1
    
    # Caminhos
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")

config = SystemConfig()
