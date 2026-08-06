# Original User Request

## 2026-08-05T14:36:53Z

# Teamwork Project Prompt — Draft

> Status: Ready for launch — awaiting user approval
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

O projeto consiste em auditar a base de código atual do canal Faceless para garantir que os 6 subagentes da "Esteira Autônoma" estejam corretamente criados e integrados. Além disso, analisar e definir qual é o melhor modelo de IA do mercado atual para garantir 100% de qualidade no roteiro (zero "AI slop" ou texto genérico), e aplicar as correções necessárias no roteador de LLM do código.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL
Integrity mode: development

## Requirements

### R1. Auditoria da Esteira (LangGraph)
Verificar os arquivos em `src/nodes/` e `src/core/engine.py` para confirmar que a topologia de 6 agentes está perfeitamente amarrada e os nós existem. Nenhuma integração com a interface visual (UI) do Antigravity é necessária, o foco é 100% no código Python.

### R2. Seleção do Modelo Definitivo (Anti AI Slop)
Executar uma análise sobre os modelos de fronteira atuais (você tem acesso à skill `llm_version_checker` no workspace). Determinar qual modelo entrega a melhor prosa humana, sem jargões genéricos, custe o que custar.

### R3. Refatoração do Roteador
Atualizar `src/connectors/llm_router.py` para substituir o modelo atual pelo modelo vencedor da análise (se diferente), garantindo que o `node_tts_scriptwriter` use-o compulsoriamente.

## Acceptance Criteria

### Verificação do Grafo Python
- [ ] O script `engine.py` passa por uma verificação de sintaxe (`python -m py_compile`) sem falhas, confirmando que os 6 agentes estão implementados.

### Atualização do Roteador
- [ ] O arquivo `llm_router.py` contém explicitamente o nome exato do modelo (ex: `claude-3-5-sonnet-latest` ou superior) na regra de roteamento forçado do scriptwriter.
- [ ] As alterações no roteador não quebram o fallback local do Ollama para o resto do sistema.

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*

## 2026-08-05T15:24:12Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Analisar a fundo o projeto de filme de IA "Hell Grind" da Higgsfield AI, extraindo seus métodos de roteiro, prompts, workflows e direção visual. Com base nesses insights, auditar nosso projeto atual (Faceless Channel) e criar um Plano de Implementação sugerindo melhorias profissonais, sem conectar APIs externas no momento.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL
Integrity mode: development

## Requirements

### R1. Extração de Conhecimento
Leia o conteúdo do site `https://higgsfield.ai/@higgsfield.studio/projects/hell-grind` usando o subagente `browser` ou navegação web. Extraia insights profundos sobre os processos, técnicas, prompts, direção visual e roteiro utilizados no filme.

### R2. Análise Comparativa
Compare as técnicas profissionais encontradas no case do "Hell Grind" com a arquitetura atual do nosso Faceless Channel (`src/nodes/` e o pipeline LangGraph). Identifique lacunas na nossa direção visual, estruturação do roteiro e orquestração de agentes.

### R3. Plano de Implementação
Crie o artefato `implementation_plan.md` detalhando as melhorias que devemos absorver do "Hell Grind". As melhorias não devem ser regras absolutas, mas adaptações para enriquecer nosso projeto. Não implemente integrações de conexão com hubs de IA neste momento. Aguarde revisão (não edite código fonte ainda).

## Acceptance Criteria

### Qualidade da Extração
- [ ] O plano lista metodologias reais citadas na página do projeto (estilos de prompt, lógicas de transição, estruturação de roteiro).

### Verificação do Plano
- [ ] O artefato `implementation_plan.md` existe, contém uma seção de "Alterações Propostas" para arquivos específicos em `src/nodes/` baseados na análise do filme.
- [ ] Nenhum arquivo `.py` de código-fonte foi alterado durante esta fase (apenas planejamento).

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*

## 2026-08-05T16:00:05Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Definir o posicionamento estratégico do nicho do canal unindo Psicologia Científica/Acadêmica e Pop Psychology/Dark Psychology, e criar a Identidade de Marca (Branding, Personagem Recorrente / SOUL ID e Âncoras Visuais Proprietárias) anti-cópia para o Faceless Channel.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL
Integrity mode: development

## Requirements

### R1. Pesquisa e Posicionamento do Nicho (Via Browser)
O agente DEVE usar o subagente `browser` para pesquisar no YouTube e na web os canais de maior sucesso em Psicologia/Dark Psychology/Neurociência (ex: formatos estilo *Academy of Ideas*, *Einzelgänger*, *Psych2Go*, canais de Dark Psychology estilo Netflix). Identifique a fusão ideal entre rigor científico e ganchos populares de alta retenção.

### R2. Criação da Identidade de Marca e Personagem (SOUL ID Anti-Cópia)
Desenvolver a bíblia do personagem/apresentador virtual proprietário do canal (design conceitual, arquétipo, paleta de cores, simbologia recorrente, bordão/assinatura narrativa). Este personagem será a propriedade intelectual que impede que o canal seja copiado por concorrentes.

### R3. Mapeamento de Integração no Sistema LangGraph
Documentar como integrar este personagem e diretrizes de nicho no pipeline do LangGraph (especificamente `layer1_identity_token` no `visual_storyboarder.py`, `SOUL_ID` no `state.py`, e tom de voz no `tts_scriptwriter.py`). Crie o artefato `implementation_plan.md` com a proposta de branding. Não modifique o código-fonte ainda.

## Acceptance Criteria

### [Qualidade do Nicho & Posicionamento]
- [ ] O plano estabelece um posicionamento claro que une termos científicos (Tríade Sombria, TCC, Neuropsicologia) com gatilhos populares (Psicologia Sombria, Manipulação, Impostor).

### [Propriedade Intelectual & Personagem]
- [ ] O plano define a especificação completa do personagem/âncora visual (aparência, prompt estático do SOUL_ID, elementos visuais únicos e estilo narrativo).

### [Verificação do Plano de Arquitetura]
- [ ] O artefato `implementation_plan.md` é entregue com as diretrizes de integração sem alterar arquivos `.py` nesta fase.

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*

## 2026-08-06T00:11:03Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Auditar o projeto Faceless Channel (`EDM ARCHETYPE LAB`), identificar todos os repositórios, ferramentas ou dependências faltantes lendo os READMEs para instalação correta, e atualizar o sistema de roteamento dos 6 agentes no LangGraph para aproveitar os 30+ modelos e provedores gerenciados pelo OmniRoute.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL
Integrity mode: development

## Requirements

### R1. Auditoria Geral de Dependências e Repositórios Pendentes
Analisar a base de código do projeto (`requirements.txt`, `src/`, documentações e scripts) para identificar bibliotecas, ferramentas externas ou repositórios faltantes. Ler os READMEs de qualquer dependência para garantir a instalação e compilação correta no ambiente Windows.

### R2. Matriz de Mapeamento Multi-Modelo via OmniRoute
Mapear a atribuição ideal de modelos de IA para cada uma das 6 etapas da esteira do `EDM ARCHETYPE LAB`, aproveitando o gateway do OmniRoute:
- **Intake & Pesquisa**: `gemini-2.0-flash` (1M context / gratuito).
- **Packaging (CTR)**: `gpt-4o-mini` ou `groq/llama-3.3-70b` (Velocidade e precisão de formato).
- **Script Architect & TTS Scriptwriter**: `claude-3-7-sonnet-20250219` (Qualidade humana / Anti-AI Slop).
- **Visual Storyboarder**: `gemini-2.0-flash` ou `claude-3.5-sonnet` (Detalhamento visual de outpainting).
- **Retention Auditor**: `groq/llama-3.3-70b` ou `deepseek-r1` (Raciocínio lógico estrito).

### R3. Atualização e Validação do Roteador LangGraph
Refatorar `src/connectors/llm_router.py` e os nós em `src/nodes/` para aceitar seleção dinâmica de modelos roteados através do OmniRoute, garantindo fallbacks em caso de indisponibilidade e compilação limpa do grafo (`python -m py_compile`).

## Acceptance Criteria

### [Auditoria & Instalação]
- [ ] Todas as dependências Python (`requirements.txt`) e ferramentas externas necessárias estão devidamente instaladas e verificadas no sistema.

### [Matriz de Roteamento Multi-Modelo]
- [ ] O `llm_router.py` implementa a matriz de roteamento por função de agente utilizando o proxy do OmniRoute (`http://localhost:20128/v1`).

### [Validação do Grafo]
- [ ] Todos os arquivos em `src/nodes/` e `src/core/engine.py` compilam com sucesso via `py_compile` sem falhas.

---
*Next: when approved → delegate via invoke_subagent (see Delegation Protocol)*

