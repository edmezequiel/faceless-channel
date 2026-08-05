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

