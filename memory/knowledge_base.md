# Base de Conhecimento Curada

## Diretrizes Fundamentais do Sistema Faceless

### 1. Filosofia Open-Source e Baixo Consumo (Otimizado para 8GB RAM)
- Toda a infraestrutura do projeto utiliza conectores e gateways abertos (**LiteLLM**, **Ollama/llama.cpp** no lugar de vLLM, **SurfSense+gpt-researcher**, **Graphify**).
- A orquestração usa conceitos do **LangGraph** para controle de estado rigoroso.
- A execução de subagentes no grafo é projetada para ser mantida em sequência controlada, prevenindo estouro de memória RAM.

### 2. Regra de Ouro de Verificação Independente
- O agente `implementation_agent` é estritamente proibido de validar ou aprovar os seus próprios artefatos.
- A aprovação é dividida em dois checkpoints obrigatórios: `verifier` (validação funcional) e `security_auditor` (validação de segurança/segredos).

### 3. Trilha de Auditoria e Memória Curada
- Contextos brutos e HTML/logs volumosos nunca são persistidos em memória permanente.
- O agente `memory_curator` extrai e condensa apenas fatos curados para o `memory/curated_memory.json` e `state.json`.
