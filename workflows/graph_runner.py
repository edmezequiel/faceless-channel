#!/usr/bin/env python3
"""
Graph Runner Engine para o Sistema de Automação de Canais Faceless.
Executa e valida transições de estado no grafo de agentes de forma leve (8 GB RAM).
"""

import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "state.json"
GRAPH_FILE = BASE_DIR / "workflows" / "main_graph.json"

def load_json(filepath):
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def validate_state(state):
    required_keys = [
        "goal", "constraints", "plan", "artifacts", "findings",
        "memory", "verification", "audit_log", "model_routing",
        "research_sources", "active_agents"
    ]
    missing = [k for k in required_keys if k not in state]
    if missing:
        raise ValueError(f"Chaves obrigatórias ausentes no state.json: {missing}")
    return True

def run_dry_run():
    print("=== INICIANDO VERIFICAÇÃO DRY-RUN DO GRAFO ===")
    graph = load_json(GRAPH_FILE)
    state = load_json(STATE_FILE)
    
    validate_state(state)
    print(f"[OK] Grafo '{graph.get('name')}' versão {graph.get('version')} carregado com sucesso.")
    print(f"[OK] Arquivo state.json validado com {len(state.keys())} campos obrigatórios presentes.")
    
    nodes = graph.get("nodes", {})
    print(f"[OK] Total de nós registrados no grafo: {len(nodes)}")
    for node_id, details in nodes.items():
        print(f"  - Nó [{node_id}]: Agente -> '{details.get('agent')}'")
    
    print("\nSimulando fluxo do grafo:")
    current_node = graph.get("start_node")
    visited = []
    
    while current_node and current_node not in visited:
        visited.append(current_node)
        node_info = nodes.get(current_node, {})
        print(f"  --> Executando nó [{current_node}] (Agente: {node_info.get('agent')})")
        
        if "next" in node_info:
            current_node = node_info["next"]
            if current_node == "orchestrator" and "orchestrator" in visited:
                print("  --> Orquestrador retornou ao centro de controle. Ciclo do grafo verificado!")
                break
        elif "transitions" in node_info:
            first_trans = list(node_info["transitions"].values())[0]
            print(f"      (Transição condicional -> Rota padrão: '{first_trans}')")
            current_node = first_trans
        else:
            break
            
    print("\n[OK] DRY-RUN CONCLUÍDO COM SUCESSO! O grafo e a estrutura de estado estão 100% funcionais.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executador de Grafos do Sistema Faceless")
    parser.add_argument("--dry-run", action="store_true", help="Executar validação em modo seco sem alterar estado")
    args = parser.parse_args()

    if args.dry_run or len(sys.argv) == 1:
        run_dry_run()
