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
