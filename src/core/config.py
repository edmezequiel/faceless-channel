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
    SCRIPTWRITER_MODEL: str = Field(default=os.getenv("SCRIPTWRITER_MODEL", "claude-3-7-sonnet-20250219"))
    
    # ═══════════════════════════════════════════════════════════════
    # MATRIZ DE ESPECIALIZAÇÃO MULTI-MODELO (por função de agente)
    # ═══════════════════════════════════════════════════════════════
    # Cada agente da esteira pode ter um modelo ideal diferente,
    # roteado automaticamente via OmniRoute.
    
    RESEARCHER_MODEL: str = Field(
        default=os.getenv("RESEARCHER_MODEL", "gemini-2.0-flash"),
        description="Modelo para pesquisa e fact-checking (janela de contexto grande, gratuito)"
    )
    PACKAGING_MODEL: str = Field(
        default=os.getenv("PACKAGING_MODEL", "gpt-4o-mini"),
        description="Modelo para embalagem CTR (rápido e preciso em formatação)"
    )
    ARCHITECT_MODEL: str = Field(
        default=os.getenv("ARCHITECT_MODEL", "claude-3-7-sonnet-20250219"),
        description="Modelo para arquitetura de roteiro (qualidade narrativa)"
    )
    STORYBOARDER_MODEL: str = Field(
        default=os.getenv("STORYBOARDER_MODEL", "gemini-2.0-flash"),
        description="Modelo para storyboard visual (detalhamento visual e spatial prompting)"
    )
    AUDITOR_MODEL: str = Field(
        default=os.getenv("AUDITOR_MODEL", "gpt-4o-mini"),
        description="Modelo para auditoria de retenção (raciocínio lógico estrito)"
    )
    
    # Restrições de Concorrência
    MAX_CONCURRENT_AGENTS: int = 1
    
    # Caminhos
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", ".")

config = SystemConfig()
