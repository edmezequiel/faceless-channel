# Plano de Implementação — Absorção de Técnicas do "Hell Grind" (Higgsfield AI) no Faceless Channel

> **Status:** Planejamento Finalizado — Aguardando Aprovação para Execução  
> **Data:** 05 de Agosto de 2026  
> **Autor:** Project Orchestrator (`teamwork_preview_orchestrator`)  
> **Escopo:** Análise comparativa e plano de evolução da arquitetura do Faceless Channel sem alteração direta de código-fonte (`.py`) nesta fase.

---

## 1. Resumo Executivo e Contexto

O projeto **"Hell Grind"** (Higgsfield AI Studio) representa o estado da arte na produção cinematográfica com Inteligência Artificial generativa. Produzido por uma equipe de 15 profissionais com orçamento inferior a US$ 500.000, o filme de 90 minutos estabeleceu novos padrões técnicos:
- **Ratio de Curadoria de 64:1** (16.000+ gerações para 253 takes selecionados na primeira fase).
- **Proporção Compute-to-Labor de 80/20** (80% do orçamento em processamento GPU / modelos e 20% em direção criativa humana).
- **Arquitetura de Prompts em 3 Camadas** (Identidade SOUL ID, Keyframe Hero Frame T2I e Motion/Cinegrafia I2V).
- **Controle Fisiológico de Ritmo e Câmera** (Hook de 2 segundos, headers de metadados por shot, taxonomia de câmera física e transições por "Scene Logic").

Em contrapartida, a auditoria da esteira autônoma do **Faceless Channel** (`src/nodes/` e `src/core/engine.py`) revelou uma estrutura LangGraph sólida de 8 nós (`intake`, `orchestrator`, `researcher`, `packaging`, `architect`, `scriptwriter`, `storyboarder`, `auditor`) com roteamento forçado para Claude 3.7 Sonnet, lista negra de 18 palavras de AI Slop e validação estrita de MPF (máximo 15 palavras/frase).

No entanto, o Faceless Channel atualmente possui **lacunas operacionais importantes em direção visual, estruturação de câmera, separação de áudio/lip-sync e filtragem de continuidade de movimento**. Este plano mapeia a absorção dessas técnicas.

---

## 2. Análise Comparativa e Lacunas Identificadas

| Domínio Técnico | Case "Hell Grind" (Higgsfield AI) | Faceless Channel (Atual) | Lacuna Identificada / Oportunidade |
| :--- | :--- | :--- | :--- |
| **Estrutura de Roteiro** | Hook de 2s, shots curtos (2.0s–4.5s), headers de metadados por shot (`[SHOT_ID]`, `[CAMERA_MOVE]`, `[DURATION]`). | Roteiro continuo em blocos de narração com MPF <= 15 palavras e tags de prosódia. | Falta de metadados ópticos/câmera estruturados por shot e divisão temporal rígida. |
| **Estratégia de Áudio** | 80% Voiceover (VO) para condução narrativa / 20% Lip-sync restrito a close-ups dramáticos. | Roteiro focado primariamente em áudio TTS sequencial sem diferenciação entre VO e Lip-Sync. | Risco de aberração labial ("lip-sync warping") se aplicar animação facial em tomadas abertas. |
| **Engenharia de Prompts** | Prompts em 3 Camadas: (1) Identity Token, (2) Keyframe T2I estático, (3) Motion I2V com verbos imperativos. | Prompts visuais gerados como texto único descritivo no `visual_storyboarder`. | Mistura de estilo, iluminação e movimento no mesmo prompt causa "AI drift" e deformação. |
| **Taxonomia de Câmera** | Comandos físicos rígidos (`Dolly In`, `Whip Pan`, `Orbit 360°`, `Truck Left`) e tags de restrição espacial. | Termos genéricos de câmera ou ausência de direcionamento óptico padronizado. | Movimentos de câmera imprevisíveis ou zoom digital com perda de resolução. |
| **Direção Visual & Cor** | Paletas de cores por reino/tema, regra de cadência de enquadramento (`CU -> Medium -> Wide`). | Prompt visual focado apenas no assunto da cena sem paleta de cores ou regra de transição de plano. | Fadiga visual por planos muito semelhantes e falta de coesão cromática no canal. |
| **Lógica de Transição** | "Scene Logic" (cortes por ação/velocidade, ponte de interpolação entre Keyframe A e B). | Transição entre cenas baseada em sequência linear de narração. | Efeitos de metamorfose indesejados ("AI morphing") ao trocar de cenário. |
| **Qualidade & Curadoria** | Filtro de qualidade com ratio 64:1; descarte automático de oscilações e aberrações de movimento. | `retention_auditor` valida estritamente texto (MPF e prosódia), sem auditoria visual de continuidade. | Falta de gate keeper para métricas visuais e consistência de movimento. |

---

## 3. Alterações Propostas (Mapeamento em `src/nodes/` e `src/core/`)

Para elevar o Faceless Channel ao nível profissional do "Hell Grind", propõe-se as seguintes modificações estruturais nos arquivos Python de `src/nodes/` e `src/core/`:

```
c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\
├── src/
│   ├── core/
│   │   └── state.py                 <-- Atualizar Pydantic Schemas (ShotMetadata, VisualBlock 3-Layer)
│   └── nodes/
│       ├── script_architect.py      <-- Injetar 2-Second Hook Rule & Shot Metadata Headers
│       ├── tts_scriptwriter.py      <-- Implementar Separação 80/20 VO vs. Lip-Sync & Prosódia
│       ├── visual_storyboarder.py   <-- Reestruturar Prompts em 3 Camadas & Taxonomia de Câmera
│       ├── retention_auditor.py     <-- Ampliar regras de auditoria para cadência de planos e ritmo
│       └── packaging_ctr.py         <-- Adicionar Paleta de Cores e Guia Estético do Canal
```

---

### 3.1 `src/core/state.py` (Modelagem de Dados)
- **Objetivo**: Expandir as estruturas Pydantic para suportar a arquitetura em 3 camadas e metadados por shot.
- **Modificações Específicas**:
  1. Criar a classe `ShotMetadata(BaseModel)`:
     - `shot_id: str` (ex: `"SC01_SH002"`)
     - `duration_seconds: float` (ex: `3.0`)
     - `camera_movement: str` (ex: `"Dolly In with Orbit Right"`)
     - `audio_type: Literal["voiceover", "lip_sync"]`
     - `spatial_constraints: List[str]` (ex: `["keep subject centered"]`)
  2. Atualizar a classe `VisualBlock(BaseModel)`:
     - `layer1_identity_token: str` (ex: `"[SOUL_ID_HERO]"` sem descritores textuais faciais)
     - `layer2_keyframe_prompt: str` (descrição estática de ambiente, iluminação e lente 35mm)
     - `layer3_motion_prompt: str` (verbos imperativos de cinegrafia e intensidade de movimento)
     - `color_palette: str` (ex: `"Cyber-Slums Cyan & Neon Magenta"`)

---

### 3.2 `src/nodes/script_architect.py` (Arquitetura de Roteiro)
- **Objetivo**: Forçar a estrutura narrativa baseada no **Hook de 2 segundos** e na geração de headers de metadados por shot.
- **Modificações Específicas**:
  1. Atualizar o `SYSTEM_PROMPT` para instruir o LLM a:
     - Exigir um jolt visual/narrativo nos primeiros 2 segundos do roteiro (evento de impacto imediato).
     - Dividir o roteiro em shots curtos de **2.0 a 4.5 segundos** cada, prevenindo a oscilação do modelo de vídeo.
     - Gerar o header `[SHOT_ID]` e `[DURATION]` para cada beat da história.

---

### 3.3 `src/nodes/tts_scriptwriter.py` (Escrita de Roteiro e Áudio)
- **Objetivo**: Integrar a regra 80/20 de Voiceover vs. Lip-Sync e refinar as tags de prosódia.
- **Modificações Específicas**:
  1. Adicionar lógica de classificação no prompt:
     - **80% do texto**: Marcado como `[VOICEOVER]` (narração contínua que guia o vídeo sem necessidade de animação labial).
     - **20% do texto**: Marcado como `[LIP_SYNC]` estritamente para close-ups de momentos dramáticos de clímax.
  2. Expandir a lista negra de palavras proibições (AI Slop) com os termos proibidos do Hell Grind (`hyperrealistic`, `masterpiece`, `trending on artstation`, `4K/8K oversaturated`).

---

### 3.4 `src/nodes/visual_storyboarder.py` (Geração de Prompts Visuais e Direção de Câmera)
- **Objetivo**: Substituir o prompt estático único pela **Arquitetura de Prompts em 3 Camadas** e padronizar a **Taxonomia de Câmera Física**.
- **Modificações Específicas**:
  1. Reestruturar a saída do nó para produzir explicitamente as 3 Camadas de Prompt:
     - **Camada 1 (Identidade)**: Isolar tokens de personagem (ex: `[SOUL_ID_MAIN]`) eliminando descrições como "cabelos castanhos, olhos azuis" que causam interferência na IA.
     - **Camada 2 (Keyframe T2I)**: Prompt estático focando em iluminação volumétrica, estética cinematográfica (35mm Anamorphic, f/2.8) e paleta cromática.
     - **Camada 3 (Motion I2V)**: Verbos imperativos curtos (`Dolly In`, `Whip Pan Left`, `Truck Right`, `Orbit 360°`).
  2. Aplicar a **Regra de Cadência de Enquadramento**:
     - Impedir sequências de `Close-Up -> Close-Up`. Forçar a transição `Close-Up -> Medium Shot -> Wide Establishing Shot`.
  3. Adicionar tags de **Restrição Espacial**:
     - Injetar automaticamente `"keep subject centered in frame"` e `"maintain physical aspect ratio"`.

---

### 3.5 `src/nodes/retention_auditor.py` (Auditoria e Controle de Qualidade)
- **Objetivo**: Expandir o auditor para validar a cadência de enquadramentos e o ritmo de câmera, além do MPF textual.
- **Modificações Específicas**:
  1. Adicionar verificação de cadência de enquadramento no storyboard gerado:
     - Reprovar (`retention_score < 70`) se houver 2 ou mais shots consecutivos com enquadramento idêntico (`Close-Up`).
  2. Validar a presença de verbos imperativos de câmera nos metadados de movimento.
  3. Manter o loop de realimentação fechado (`auditor_router` em `src/core/engine.py`), re-encaminhando para o `scriptwriter` ou `storyboarder` em caso de reprovação.

---

### 3.6 `src/nodes/packaging_ctr.py` (Embalagem e Direção Estética)
- **Objetivo**: Garantir que o título, a thumbnail e o tema visual compartilhem a mesma paleta de cores e gancho do roteiro.
- **Modificações Específicas**:
  1. Injetar a definição da paleta de cores dominante no modelo `Packaging` (ex: `neon_cyberpunk`, `desaturated_monochrome`, `golden_hour_mythic`).
  2. Garantir que a sugestão de Thumbnail use a regra do Keyframe Hero Frame (foco estático de alta resolução).

---

## 4. Cronograma de Implementação Recomendado (Próximas Fases)

Após a aprovação deste plano de implementação pelo usuário/time, o desenvolvimento deverá seguir em 3 fases estruturadas de código:

1. **Fase 1: Atualização dos Schemas de Dados (`src/core/state.py`)**
   - Atualizar Pydantic models e testar a instanciação dos novos tipos de dados.
2. **Fase 2: Refatoração dos Nós de Roteiro e Câmera (`src/nodes/`)**
   - Atualizar prompts e parsers em `script_architect.py`, `tts_scriptwriter.py` e `visual_storyboarder.py`.
3. **Fase 3: Validação do Grafo e Testes de Regressão (`src/core/engine.py` & Auditor)**
   - Atualizar `retention_auditor.py` e executar compilação de sintaxe e simulação de fluxo no LangGraph.

---

## 5. Critérios de Aceite Mapeados

- [x] **R1. Extração de Conhecimento**: Insights profundos do projeto *Hell Grind* catalogados em `.agents/spec_miner_hell_grind/hell_grind_insights.md`.
- [x] **R2. Análise Comparativa**: Auditoria estática do Faceless Channel documentada em `.agents/explorer_codebase/codebase_audit.md` e confrontada com o case.
- [x] **R3. Plano de Implementação**: Artefato `implementation_plan.md` gerado na raiz e no diretório do orquestrador com a seção "Alterações Propostas" mapeada para os arquivos em `src/nodes/` e `src/core/`.
- [x] **Integridade do Código**: Zero arquivos `.py` modificados durante esta fase de planejamento.
