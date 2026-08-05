# Audit Completo da Arquitetura do Faceless Channel

**Data de Auditoria:** 2026-08-05  
**Ambiente de Trabalho:** `c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL`  
**Escopo do Audit:** `src/nodes/`, `src/core/engine.py`, `src/core/state.py`, `src/connectors/llm_router.py`, `src/connectors/agent_reach.py`, `workflows/`  
**Status de Modificação de Código:** Estritamente Read-Only (nenhum arquivo `.py` de código-fonte foi alterado).

---

## Executive Summary

A auditoria arquitetural do **Faceless Channel** confirmou que o sistema opera com uma esteira principal de 6 agentes especializados encadeados via **LangGraph** (`src/core/engine.py`), precedidos por 2 nós de entrada/orquestração (`intake` e `orchestrator`). A arquitetura do grafo implementa um mecanismo de **Closed-Loop** de realimentação condicional em que o nó `auditor` (Retention Auditor) valida a nota de qualidade/retenção do roteiro e, caso a nota seja inferior a 85, o fluxo retrata e devolve o estado diretamente ao nó `scriptwriter` (TTS Scriptwriter) com o feedback detalhado do auditor.

Abaixo apresenta-se o inventário técnico exato, a análise detalhada da engenharia de prompts, a estruturação de roteiro/direção visual e a orquestração do LangGraph.

---

## 1. Node Inventory (Inventário dos Nós)

A pasta `src/nodes/` contém **8 arquivos de nós Python**. A tabela abaixo detalha cada nó, sua responsabilidade, entradas consumidas do `AgentState`, saídas produzidas e status de implementação.

| Arquivo (`src/nodes/`) | Função / Classe | Responsabilidade Principal | Entradas (`AgentState`) | Saídas (`AgentState`) | Tipo de Chamada / LLM |
|---|---|---|---|---|---|
| `intake.py` | `node_intake_router` | Valida a meta/objetivo de entrada (`goal`) e inicializa o log de auditoria. | `goal`, `audit_log` | `audit_log`, `current_status`: `"intake_ok"` | Lógica Python pura (Mock/Validação) |
| `orchestrator.py` | `node_orchestrator` | Atua como cérebro do Grafo. Avalia o status e despacha o fluxo para a esteira. | `current_status`, `audit_log` | `current_status`: `"route_researcher"`, `audit_log` | Lógica de decisão Python |
| `researcher_fact_checker.py` | `node_researcher_fact_checker` | **Agente 1 da Esteira**: Coleta dados via YouTube/Web (`AgentReachConnector`) e isola fatos comprovados. | `goal` | `factual_context`, `current_status`: `"research_done"` | LLM Router (`generate_response`) com system prompt de Fact-Checker |
| `packaging_ctr.py` | `node_packaging_ctr` | **Agente 2 da Esteira**: Gera 5 títulos baseados em Curiosity Gap e 1 conceito de thumbnail. | `goal`, `factual_context` | `packaging` (dict: `titles`, `thumbnail_concept`), `current_status`: `"packaging_done"` | LLM Router + `PydanticOutputParser(Packaging)` |
| `script_architect.py` | `node_script_architect` | **Agente 3 da Esteira**: Desenha a escaleta narrativa de 10 min com ganchos e *Open Loops*. | `goal`, `factual_context` | `script_skeleton` (dict: `beats`, `open_loops`), `current_status`: `"architect_done"` | LLM Router + `PydanticOutputParser(ScriptSkeleton)` |
| `tts_scriptwriter.py` | `node_tts_scriptwriter` | **Agente 4 da Esteira**: Escreve o roteiro em prosa falada com tags de prosódia e banimento de AI Slop. | `script_skeleton`, `factual_context`, `auditor_feedback` | `tts_prose`, `word_count`, `current_status`: `"scriptwriter_done"` | LLM Router (`force_claude_sonnet=True`) + `PydanticOutputParser(TTSResponse)` |
| `visual_storyboarder.py` | `node_visual_storyboarder` | **Agente 5 da Esteira**: Decompõe a prosa em blocos visuais sincronizados (B-Roll e técnicas de iluminação/câmera). | `tts_prose` | `visual_blocks` (list of dicts: `VisualBlock`), `current_status`: `"storyboarder_done"` | LLM Router + `PydanticOutputParser(StoryboardResponse)` |
| `retention_auditor.py` | `node_retention_auditor` | **Agente 6 da Esteira**: Audita o roteiro (palavras por frase, volume total, tags de prosódia). Define nota e feedback. | `tts_prose`, `word_count` | `retention_score`, `auditor_feedback`, `current_status`: `"auditor_approved"` ou `"auditor_failed"` | Análise algorítmica por Regex em Python puro |

### Análise Detalhada da Implementação dos Nós:

1. **`intake.py` (`node_intake_router`)**:
   - Extrai `goal` de `state` (default `"Sem objetivo definido"`).
   - Adiciona entrada em `audit_log`: `{"agent": "intake_router", "action": "Validação de entrada concluída com sucesso."}`.
   - Retorna `current_status = "intake_ok"`.

2. **`orchestrator.py` (`node_orchestrator`)**:
   - Verifica `state.get("current_status")`. Se for `"intake_ok"`, define rota para `"researcher"`.
   - Adiciona log em `audit_log`.
   - Retorna `current_status = "route_researcher"`.

3. **`researcher_fact_checker.py` (`node_researcher_fact_checker`)**:
   - Executa `AgentReachConnector.search_youtube(goal)` e `AgentReachConnector.read_webpage(...)` (atualmente wrappers simulados).
   - Monta `raw_data` e invoca `generate_response(prompt, system_prompt="Você é um Fact-Checker rigoroso.")`.
   - Atualiza `factual_context` no estado.

4. **`packaging_ctr.py` (`node_packaging_ctr`)**:
   - Utiliza `PydanticOutputParser(pydantic_object=Packaging)` para forçar saída estrita em JSON.
   - Trata exceções de parse via `OutputParserException`, fornecendo um fallback com 5 títulos genéricos e conceito de capa simples.

5. **`script_architect.py` (`node_script_architect`)**:
   - Otimizado com `PydanticOutputParser(pydantic_object=ScriptSkeleton)`.
   - Instrui o LLM a criar um vídeo de 10 minutos estilo MrBeast, quebrando padrão no Beat 1, alternando ângulo a cada 45s e inserindo 1-2 open loops massivos.
   - Fallback de segurança com 3 beats simples e 1 open loop caso o parse falhe.

6. **`tts_scriptwriter.py` (`node_tts_scriptwriter`)**:
   - O nó crítico da esteira. Invoca `generate_response` passando obrigatoriamente `force_claude_sonnet=True`.
   - Em `llm_router.py`, a flag `force_claude_sonnet` força a constante `SCRIPTWRITER_WINNING_MODEL = "claude-3-7-sonnet-20250219"`.
   - Incorpora o `auditor_feedback` no prompt quando o auditor reprova uma versão anterior.
   - Calcula `word_count = len(prose_text.split())`.

7. **`visual_storyboarder.py` (`node_visual_storyboarder`)**:
   - Se `tts_prose` estiver vazia, falha imediatamente (`current_status = "storyboarder_failed"`).
   - Utiliza `PydanticOutputParser(pydantic_object=StoryboardResponse)`.
   - Fatia o roteiro em blocos com `b_roll_description` e `grokfilm_technique`.

8. **`retention_auditor.py` (`node_retention_auditor`)**:
   - Realiza cálculo determinístico sem chamada a LLM:
     - Word Count < 200: penalização de -40 pontos.
     - Média de Palavras por Frase (MPF) > 15: penalização de -20 pontos (usando `re.split(r'[.!?]', prose)`).
     - Contagem de tags de prosódia (`re.findall(r'\[.*?\]', prose)`) < (frases / 4): penalização de -20 pontos.
   - Se `score < 85`, `current_status = "auditor_failed"`; caso contrário, `current_status = "auditor_approved"`.

---

## 2. Prompt Engineering Audit (Engenharia de Prompts)

### 2.1 Análise dos Prompts por Nó

- **`node_researcher_fact_checker`**:
  - *System Prompt*: `"Você é um Fact-Checker rigoroso."`
  - *User Prompt*: `"Analise estes dados sobre '{goal}'. Extraia APENAS fatos comprovados, nomes, datas e eventos, removendo qualquer viés ou desinformação.\n\nDados brutos:\n{raw_data}"`
  - *Avaliação*: Prompt funcional, porém direto e simplista. Não fornece regras de estruturação para o output factual (ex: bullet points por ordem de relevância cronológica).

- **`node_packaging_ctr`**:
  - *System Prompt*: `"Você é um gênio de CTR e Psicologia Humana."`
  - *User Prompt*: Define regras de Curiosity Gap, limite de 50 caracteres para títulos e conceito de thumbnail com no máximo 3 elementos visuais. Incorpora `format_instructions` do `PydanticOutputParser`.
  - *Avaliação*: Boa aplicação de instrução estruturada.

- **`node_script_architect`**:
  - *System Prompt*: `"Você é um roteirista analítico especializado em gráficos de retenção (AVD)."`
  - *User Prompt*: Exige estrutura estilo MrBeast, quebra de padrão no Beat 1, mudança de ângulo narrativo a cada 45 segundos e 1 a 2 Open Loops massivos.
  - *Avaliação*: Prompt robusto para esqueleto estrutural.

- **`node_tts_scriptwriter` (O Prompt Supremo)**:
  - *System Prompt*: `"Você é um gênio da escrita persuasiva focado em ritmo dinâmico. Você odeia jargões genéricos de Inteligência Artificial."`
  - *User Prompt*:
    - **Lista Negra de AI Slop**: Banimento explícito de 18 termos e clichês de IA: `"mergulhar"`, `"desvendar"`, `"paisagem"`, `"em um mundo onde"`, `"jornada"`, `"descubra"`, `"vamos explorar"`, `"hoje vamos falar sobre"`, `"fascinante"`, `"cativante"`, `"teia"`, `"intrincado"`, `"testamento"`, `"sinfonia"`, `"dança"`, `"imaginem"`.
    - **Fôlego Curto**: Exigência de frases curtas de no máximo 15 palavras.
    - **Prosódia Mecânica**: Exigência de tags no formato `[PAUSA_0.5s]`, `[PAUSA_1s]`, `[TOM_MISTERIOSO]`, `[TOM_AGRESSIVO]`, `[ACELERAR]`.
    - **Realimentação de Feedback**: Injeta `{auditor_feedback if auditor_feedback else "Primeira tentativa. Faça perfeito."}`.
    - **Volume de Conteúdo**: Instrução explícita para não limitar tempo nem espremer a história, mantendo densidade.
  - *Avaliação*: O prompt mais trabalhado do sistema. Apresenta excelente clareza de regras e restrições inquebráveis.

- **`node_visual_storyboarder`**:
  - *System Prompt*: `"Você é um Cinematógrafo Especialista em AI Video."`
  - *User Prompt*: Solicita a fatiagem do roteiro em `b_roll_description` e `grokfilm_technique`.
  - *Avaliação*: O prompt é genérico e vago. Não define padrões de composição cinematográfica, estilos de lente, movimento de câmera, iluminação ou paleta de cores.

### 2.2 Estilo de Invocação de LLM e Roteamento

As chamadas são centralizadas em `src/connectors/llm_router.py`:
- O roteador verifica a flag `USE_LOCAL_LLM` (do `src/core/config.py`).
- Se `force_claude_sonnet=True` ou `force_scriptwriter=True` for passado nos `kwargs`, o roteador **força obrigatoriamente** a utilização do modelo em nuvem `SCRIPTWRITER_WINNING_MODEL` (atualmente configurado como `"claude-3-7-sonnet-20250219"`).
- Para outros nós:
  - Se `USE_LOCAL_LLM` for verdadeiro e `model` for `None`, utiliza `"ollama/llama3"`.
  - Se `USE_LOCAL_LLM` for falso, utiliza `LITELLM_DEFAULT_MODEL` (`"gpt-4o-mini"`).
- Todas as chamadas de nuvem e local são abstraídas pela biblioteca `litellm.completion`.

### 2.3 Gestão de Prompts e Tratamento de Erros

- **Prompts Hardcoded**: Todos os prompts estão gravados como strings dentro das próprias funções dos nós (ex: em `tts_scriptwriter.py`). Não há um repositório centralizado ou sistema de templates `.jinja2` / `.txt` para gestão e versionamento de prompts.
- **Tratamento de Erros e Parsers**:
  - Todos os nós estruturados utilizam `langchain_core.output_parsers.PydanticOutputParser`.
  - Em caso de falha de parsing (`OutputParserException`), os nós capturam o erro no bloco `try...except` e retornam um **dicionário de fallback seguro** (prevenindo quebra catastrófica do grafo).

---

## 3. Script Structuring & Visual Direction Audit

### 3.1 Schemas e Modelos de Dados Pydantic (`src/core/state.py`)

A estruturação dos dados entre os nós é suportada pelos modelos Pydantic v2 declarados em `src/core/state.py`:

```python
class Packaging(BaseModel):
    titles: List[str] = Field(default_factory=list, description="5 títulos com Curiosity Gap")
    thumbnail_concept: str = Field(default="", description="Conceito primário da capa")

class ScriptSkeleton(BaseModel):
    beats: List[str] = Field(default_factory=list, description="Estrutura temporal")
    open_loops: List[str] = Field(default_factory=list, description="Ganchos retidos até o final")

class VisualBlock(BaseModel):
    timestamp_start: str
    timestamp_end: str
    b_roll_description: str
    grokfilm_technique: str
```

### 3.2 Fluxo Sequencial de Dados

1. `goal` (String) -> `intake` -> `orchestrator`
2. `researcher`: Consome `goal` -> Gera `factual_context` (String de texto livre factual)
3. `packaging`: Consome `goal` + `factual_context` -> Gera `packaging` (Dict no schema `Packaging`)
4. `architect`: Consome `goal` + `factual_context` -> Gera `script_skeleton` (Dict no schema `ScriptSkeleton`: `beats` e `open_loops`)
5. `scriptwriter`: Consome `script_skeleton` + `factual_context` + `auditor_feedback` -> Gera `tts_prose` (String com prosódia) + `word_count` (int)
6. `storyboarder`: Consome `tts_prose` -> Gera `visual_blocks` (Lista de Dicts no schema `VisualBlock`)
7. `auditor`: Consome `tts_prose` + `word_count` -> Gera `retention_score` (int) + `auditor_feedback` (String)

### 3.3 Lacunas na Direção Visual e Prompts de Vídeo

A auditoria identificou limitações significativas na geração visual em `node_visual_storyboarder`:
1. **Ausência de Timestamps Reais**: O modelo `VisualBlock` exige `timestamp_start` e `timestamp_end`, porém no prompt do storyboarder o LLM não recebe a duração do áudio nem o cálculo de tempo por palavra para preencher esses campos adequadamente.
2. **Prompts Visuais Simplistas**: A `b_roll_description` é gerada como um resumo textual simples e a `grokfilm_technique` é uma string genérica. Não há separação em parâmetros essenciais de geração de vídeo AI (Subject, Movement, Framing, Aspect Ratio, Lighting, Camera Lens).

---

## 4. Multi-Agent & LangGraph Orchestration Audit (`src/core/engine.py`)

### 4.1 Topologia do Grafo LangGraph

O arquivo `src/core/engine.py` constrói o `StateGraph` utilizando a classe `AgentState` declarada em `src/core/state.py`.

```
[ENTRY: intake]
       │
       ▼
 [orchestrator]
       │ (conditional edge: return "researcher")
       ▼
  [researcher]
       │ (edge)
       ▼
  [packaging]
       │ (edge)
       ▼
  [architect]
       │ (edge)
       ▼
 [scriptwriter] ◄────────────────────────────────┐ (Closed Loop:
       │ (edge)                                  │  se retention_score < 85)
       ▼                                         │
[storyboarder]                                   │
       │ (edge)                                  │
       ▼                                         │
   [auditor] ─── (status == "auditor_failed") ───┘
       │
       └─── (status != "auditor_failed") ───► [END]
```

### 4.2 Definição dos Nós e Arestas em `engine.py`

1. **Adição dos Nós**:
   ```python
   builder.add_node("intake", node_intake_router)
   builder.add_node("orchestrator", node_orchestrator)
   builder.add_node("researcher", node_researcher_fact_checker)
   builder.add_node("packaging", node_packaging_ctr)
   builder.add_node("architect", node_script_architect)
   builder.add_node("scriptwriter", node_tts_scriptwriter)
   builder.add_node("storyboarder", node_visual_storyboarder)
   builder.add_node("auditor", node_retention_auditor)
   ```

2. **Fluxo Inicial e Arestas Sequenciais**:
   - Entry Point: `builder.set_entry_point("intake")`
   - Direct Edge: `builder.add_edge("intake", "orchestrator")`
   - Conditional Edge: `orchestrator` -> `orchestrator_router` (que retorna `"researcher"`)
   - Direct Sequential Chain:
     - `researcher` -> `packaging`
     - `packaging` -> `architect`
     - `architect` -> `scriptwriter`
     - `scriptwriter` -> `storyboarder`
     - `storyboarder` -> `auditor`

3. **Mecanismo de Closed-Loop (Feedback Loop)**:
   - Conditional Edge em `auditor`:
     ```python
     def auditor_router(state: AgentState):
         status = state.get("current_status", "")
         if status == "auditor_failed":
             logger.warning(">>> CLOSED LOOP ATIVADO: Roteiro reprovado (< 85). Voltando para o Scriptwriter.")
             return "scriptwriter"
         else:
             logger.info(">>> Roteiro APROVADO! Finalizando esteira.")
             return END
     ```
   - Mapeamento de rotas do auditor: `{"scriptwriter": "scriptwriter", END: END}`.

### 4.3 Análise de Estado Global (`AgentState`)

O `AgentState` em `src/core/state.py` utiliza `TypedDict` e operadores de redução (`Annotated[..., operator.add]`):
- `goal`: String (meta do vídeo)
- `current_status`: String (status da etapa atual)
- `factual_context`: String (fatos extraídos pelo pesquisador)
- `packaging`: Dict (títulos e thumbnail)
- `script_skeleton`: Dict (beats e open loops)
- `tts_prose`: String (prosa falada)
- `word_count`: Integer (contagem de palavras)
- `visual_blocks`: List[Dict] (blocos visuais do storyboarder)
- `retention_score`: Integer (nota do auditor, 0 a 100)
- `auditor_feedback`: String (motivo de reprovação/orientação)
- `audit_log`: `Annotated[List[Dict[str, Any]], operator.add]` (log acumulativo)
- `research_sources`: `Annotated[List[Dict[str, str]], operator.add]` (fontes acumulativas)
- `active_agents`: `Annotated[List[str], operator.add]` (histórico de agentes)

### 4.4 Discrepância Encontrada: Dualidade de Grafo

Durante a investigação da arquitetura, identificou-se uma discrepância relevante entre dois executores no repositório:
- **`src/core/engine.py`**: É o grafo oficial em Python construído com **LangGraph** (`StateGraph`), operando com **6 agentes da esteira principal** (`researcher`, `packaging`, `architect`, `scriptwriter`, `storyboarder`, `auditor`) + 2 nós de entrada (`intake`, `orchestrator`).
- **`workflows/graph_runner.py` / `workflows/main_graph.json`**: É um validador/executor em JSON que define um grafo diferente de **10 agentes** (`intake_router`, `orchestrator`, `research_agent`, `cultural_graph_engineer`, `generative_cinematographer`, `codebase_analyst`, `memory_curator`, `model_router_agent`, `implementation_agent`, `verifier`, `security_auditor`, `audit_reporter`).

O código em `src/core/engine.py` é o pipeline de produção real para geração de conteúdo Faceless via LangGraph.

---

## 5. Resumo das Descobertas e Recomendações

1. **Integridade da Esteira de 6 Agentes**: Todos os 6 agentes da esteira de conteúdo e o ecossistema do `engine.py` existem e estão 100% integrados em Python no `src/core/engine.py`.
2. **Roteamento de LLM**: O `llm_router.py` contém a regra forçada `SCRIPTWRITER_WINNING_MODEL = "claude-3-7-sonnet-20250219"` ativada pela flag `force_claude_sonnet=True` no `tts_scriptwriter.py`.
3. **Prompt do Scriptwriter**: Extremamente completo com banimento de 18 termos de AI Slop, regra de fôlego curto (<= 15 palavras por frase), inserção obrigatória de prosódia e ciclo de feedback.
4. **Oportunidades de Otimização**:
   - Centralizar prompts hardcoded em arquivos de template externos ou módulo de prompts.
   - Enriquecer os prompts de direção visual do `visual_storyboarder.py` com termos cinemáticos avançados (camera movement, lighting, shot scale, prompt structuring).
   - Ajustar a métrica de tamanho mínimo de palavras no `retention_auditor.py` (atualmente o auditor exige 200 palavras, enquanto o spec previa 1.800 palavras para vídeos de 10-12 min).

---

*Relatório de Auditoria concluído com sucesso por Codebase Architecture Explorer.*
