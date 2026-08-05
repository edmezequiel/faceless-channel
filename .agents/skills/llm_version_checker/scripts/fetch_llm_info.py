import json
import urllib.request
import sys

def fetch_model_market_data(query_term=""):
    """
    Busca modelos, preços por 1M de tokens e dados de contexto no OpenRouter.
    """
    url = "https://openrouter.ai/api/v1/models"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            models = data.get('data', [])
            
            if query_term:
                models = [
                    m for m in models 
                    if query_term.lower() in m.get('id', '').lower() 
                    or query_term.lower() in m.get('name', '').lower()
                ]
            
            # Ordena por modelos mais recentes ou atualizados
            models.sort(key=lambda x: x.get('created', 0), reverse=True)
            
            formatted_models = []
            for m in models[:15]:
                pricing = m.get('pricing', {})
                
                # Preços no OpenRouter são por token, converte para 1 Milhão de tokens (USD)
                prompt_price_per_1m = float(pricing.get('prompt', 0) or 0) * 1_000_000
                completion_price_per_1m = float(pricing.get('completion', 0) or 0) * 1_000_000
                
                formatted_models.append({
                    "id": m.get("id"),
                    "name": m.get("name"),
                    "context_length": m.get("context_length"),
                    "pricing_usd_per_1m_tokens": {
                        "input": f"${prompt_price_per_1m:.4f}",
                        "output": f"${completion_price_per_1m:.4f}"
                    },
                    "description": m.get("description", "")[:250]
                })
                
            return formatted_models
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"=== INTELIGÊNCIA DE MODELOS, CUSTOS E PREÇOS (Termo: '{query}') ===")
    results = fetch_model_market_data(query)
    print(json.dumps(results, indent=2, ensure_ascii=False))
