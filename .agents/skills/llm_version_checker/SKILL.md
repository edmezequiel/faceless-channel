---
name: llm-version-checker
description: Consulta as últimas versões de LLMs, rankings de benchmarks em tempo real (LMSYS Arena, LiveBench, etc.), recomendação de modelos por tipo de tarefa e análise detalhada de custos de API (preço por 1M de tokens e custo-benefício).
---

# LLM Version, Benchmark & Cost Intelligence Skill

## Quando Utilizar
Utilize esta skill sempre que o usuário perguntar sobre:
- Versões recentes, novidades ou lançamentos de modelos (ex.: Kimi k3, Qwen 3.8, Claude, DeepSeek).
- **Rankings de Benchmarks**: Qual o melhor modelo em rankings atuais (LMSYS Chatbot Arena, LiveBench, SWE-bench, Artificial Analysis).
- **Recomendação por Tarefa**: Qual o modelo ideal para programação, matemática/raciocínio, visão computacional, RAG com arquivos grandes ou agentes autônomos.
- **Custos de API**: Comparação de preços por 1 milhão de tokens (input e output), custos com prompt caching, latência e melhor relação custo-benefício.

---

## Fluxo de Execução

### Passo 1: Consulta de Metadados e Preços em Tempo Real
1. Execute o script `scripts/fetch_llm_info.py` ou faça uma requisição à API do OpenRouter (`https://openrouter.ai/api/v1/models`).
2. Para cada modelo relevante, extraia:
   - **ID e Nome do Modelo**.
   - **Preço de Entrada (Input)**: Convertido para valor por **1 Milhão de Tokens (USD)**.
   - **Preço de Saída (Output)**: Convertido para valor por **1 Milhão de Tokens (USD)**.
   - **Tamanho da Janela de Contexto** (ex.: 128k, 200k, 1M, 2M tokens).

### Passo 2: Verificação de Rankings de Benchmarks
Consulte as tabelas e dados atualizados nos benchmarks de referência:
- **LMSYS Chatbot Arena (Elo Rating)**: Para desempenho geral em conversação e preferência humana.
- **SWE-bench / LiveBench Code / HumanEval**: Para capacidade de programação e resolução de bugs de código em repositórios reais.
- **GPQA / MATH-500 / AIME**: Para raciocínio matemático e científico avançado.
- **Artificial Analysis**: Para medir latência (tokens por segundo), tempo até o primeiro token (TTFT) e custo-eficiência.

### Passo 3: Análise de Ajuste à Tarefa do Usuário
Combine Desempenho (Elo/Benchmark) vs. Custo para indicar a escolha certa conforme o cenário:

| Tipo de Tarefa | Benchmarks Chave | Modelos de Elite (Topo de Linha) | Opções de Custo-Benefício (Avançadas e Baratas) |
| :--- | :--- | :--- | :--- |
| **Programação e Agentes de Código** | SWE-bench, LiveBench Code | Claude 3.5 Sonnet / OpenAI o1 / GPT-4o | DeepSeek-Coder / Qwen-2.5-Coder / DeepSeek-V3 |
| **Raciocínio Complexo / Matemática** | GPQA, MATH-500, AIME | OpenAI o1 / o3-mini / DeepSeek-R1 | DeepSeek-R1 / Qwen-2.5-Math |
| **RAG / Longo Contexto (Documentos Grandes)** | Needle in a Haystack, RAG-bench | Gemini 1.5 Pro / Claude 3.5 Sonnet | Gemini 1.5 Flash / Qwen 2.5 72B |
| **Multimodalidade (Visão e Imagem)** | MMMU, Vision Arena | GPT-4o / Gemini 1.5 Pro / Claude 3.5 Sonnet | Qwen2-VL / MiniCPM-V |
| **Alta Frequência / Baixa Latência** | Tokens/segundo (Artificial Analysis) | Claude 3.5 Haiku / GPT-4o-mini | DeepSeek-V3 / Gemini 1.5 Flash |

### Passo 4: Formatação do Relatório para o Usuário
Estruture a resposta com clareza nos seguintes blocos:

1. **Modelos Relevantes / Lançamentos**:
   - Nome, desenvolvedor e versão/data de lançamento.
2. **Posição em Benchmarks**:
   - Pontuação Elo no Chatbot Arena ou desempenho nos benchmarks específicos da tarefa.
3. **Análise de Custos de API**:
   - Custo estimado por **1M Tokens de Entrada** e **1M Tokens de Saída**.
   - Indicação se suporta *Prompt Caching* (redução de até 75-90% no custo de entrada).
4. **Veredito / Recomendação de Uso**:
   - **Escolha Premium / Sem restrição de orçamento**: O modelo com maior pontuação absoluta no benchmark.
   - **Escolha Custo-Benefício**: O modelo que entrega 90-95% do desempenho por uma fração pequena do preço.
