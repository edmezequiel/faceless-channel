# Original User Request

## 2026-08-06T17:28:22Z

Desenvolver um Sistema Autônomo de Aprendizado e Aprimoramento Contínuo de Roteiros Virais (`Viral Learning Engine`). O sistema ingerirá transcrições e dados de vídeos virais do YouTube de qualquer nicho, extrairá os padrões narrativos de alta retenção (ganchos, paradoxos, imersão sensorial, micro-twists, analogias) e atualizará dinamicamente a base de conhecimento e os prompts da esteira `EDM ARCHETYPE LAB`.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL

Integrity mode: development

## Requirements

### R1. Base de Conhecimento Estruturada de Roteiros Virais (`Viral Knowledge Bank`)
Criar uma estrutura de dados persistente em `memory/viral_knowledge_bank/knowledge_base.json` e `memory/viral_knowledge_bank/patterns.md` para catalogar e categorizar padrões de sucesso de qualquer vídeo viral (hooks, ganchos de retenção, analogias, pacing, viradas e CTAs).

### R2. Módulo de Ingestão e Aprendizado Autônomo (`src/connectors/learning_engine.py`)
Implementar um módulo Python capaz de analisar transcrições brutas ou estudos de caso de vídeos virais, extrair a anatomia narrativa, calcular os fatores de sucesso e atualizar atomicamente a `knowledge_base.json`.

### R3. Injeção Dinâmica na Esteira LangGraph (`src/nodes/script_architect.py` e `src/nodes/tts_scriptwriter.py`)
Conectar os nós da esteira de produção para lerem automaticamente os melhores padrões acumulados no `Viral Knowledge Bank` e injetá-los no prompt do Claude 3.7 Sonnet a cada novo roteiro gerado.

### R4. Interface CLI / Script de Aprendizado (`ingest_viral_script.py`)
Criar um script executável simples `ingest_viral_script.py [caminho_ou_texto]` que permita ao usuário enviar novos roteiros virais para o sistema aprender instantaneamente.

## Acceptance Criteria

### Integridade do Banco de Dados
- [ ] O arquivo `memory/viral_knowledge_bank/knowledge_base.json` existe e possui schema válido com categorias: `hooks`, `analogies`, `micro_twists`, `sensory_beats`, `ctas` e `retention_tactics`.
- [ ] O script de ingestão `ingest_viral_script.py` processa as transcrições da Voyager 1 e de Plutão/JWST e popula a base de conhecimento com os casos analisados.

### Integração com o Pipeline Python
- [ ] O módulo `src/connectors/learning_engine.py` passa por compilação de sintaxe (`python -m py_compile`) sem erros.
- [ ] Os nós `script_architect.py` e `tts_scriptwriter.py` importam e consomem os padrões do `Viral Knowledge Bank` em tempo de execução.
- [ ] O teste completo do pipeline (`run_test.py`) executa com sucesso usando os aprendizados injetados.
