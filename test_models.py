from src.connectors.llm_router import generate_response
import logging

logging.basicConfig(level=logging.INFO)

test_models = [
    "antigravity/claude-sonnet-4-6",
    "agy/claude-sonnet-4-6",
    "google/gemini-2.0-flash",
    "groq/llama-3.3-70b-versatile",
    "gpt-4o-mini"
]

print("=== TESTANDO CONEXÃO DE MODELOS NO OMNIROUTE ===")
for model in test_models:
    print(f"\n--- Testando modelo: {model} ---")
    res = generate_response(prompt="Responda apenas 'OK' se você está funcionando.", model=model)
    print(f"Resposta ({model}): {res[:100]}")
