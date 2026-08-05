# Original User Request

## 2026-08-05T15:35:47Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Analisar a fundo a estética de "Infinite Scroll" de sites de altíssimo nível (Shopify Winter 2026 e Pear.no) e arquitetar uma metodologia técnica para converter esse formato web interativo em um formato de vídeo contínuo gerado por IA para o Faceless Channel. O vídeo deve manter um fluxo visual ininterrupto, conectando imagens e textos de forma orgânica com a narração.

Working directory: c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL
Integrity mode: development

## Requirements

### R1. Análise de Referências (Via Browser)
O agente DEVE usar o subagente `browser` para acessar e destrinchar a estrutura visual, o ritmo e as lógicas de transição dos sites `https://www.shopify.com/editions/winter2026` e `https://pear.no/`. Identifique como os elementos textuais e visuais se mesclam durante a rolagem contínua.

### R2. Metodologia de Adaptação para Vídeo de IA
Proponha um workflow técnico explicando como mimetizar esse efeito usando nossas ferramentas de IA (ex: Outpainting contínuo, transições de pan/dolly fluidas unidas por interpoladores, uso de Deforum/SVD, ou sobreposição de texto em motion tracking). 

### R3. Plano de Arquitetura no LangGraph
Desenvolva um plano de implementação documentando como adaptar nosso `visual_storyboarder.py` e `script_architect.py` para suportar esse novo estilo narrativo (onde a câmera nunca corta, apenas "scrolla"). Crie o artefato `implementation_plan.md` listando as mudanças necessárias no código. Não modifique o código-fonte ainda.

## Acceptance Criteria

### [Qualidade da Análise]
- [ ] O plano descreve detalhadamente o comportamento de "scroll" dos sites de referência e como isso se traduz visualmente para vídeo (direção de arte).

### [Verificação do Workflow Técnico]
- [ ] O plano sugere uma técnica plausível de geração de vídeo contínuo com IA (ex: parâmetros específicos de I2V, Panning, Outpainting, ou After Effects script automation).
- [ ] O plano mapeia exatamente quais nós do LangGraph precisariam ser reescritos (ex: forçar a taxonomia de câmera para `Vertical Pan Down` constante).

### [Segurança do Código]
- [ ] Nenhum código `.py` é alterado nesta fase; apenas o artefato de planejamento é entregue.

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

