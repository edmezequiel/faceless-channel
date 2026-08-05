import sys
import os

# Add root directory to path
root_dir = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.connectors import llm_router
from src.core import config as cfg_module
from src.core.engine import build_graph

def test_router_logic():
    print("--- Testing LLM Router Logic ---")
    
    # Check winning model constant
    print(f"SCRIPTWRITER_WINNING_MODEL: {llm_router.SCRIPTWRITER_WINNING_MODEL}")
    assert llm_router.SCRIPTWRITER_WINNING_MODEL == "claude-3-7-sonnet-20250219", "Winning model mismatch!"
    
    # We monkeypatch completion to intercept target_model without making external API calls
    captured_models = []
    
    def mock_completion(**kwargs):
        captured_models.append(kwargs.get("model"))
        class MockChoice:
            class MockMessage:
                content = "Mock response"
            message = MockMessage()
        class MockResponse:
            choices = [MockChoice()]
        return MockResponse()
    
    llm_router.completion = mock_completion
    
    # 1. Test forced scriptwriter route (force_claude_sonnet=True)
    captured_models.clear()
    llm_router.generate_response("prompt", force_claude_sonnet=True)
    assert captured_models[0] == "claude-3-7-sonnet-20250219", f"Expected claude-3-7-sonnet-20250219, got {captured_models[0]}"
    print("PASS: force_claude_sonnet routes to claude-3-7-sonnet-20250219")
    
    # 2. Test forced scriptwriter route (force_scriptwriter=True)
    captured_models.clear()
    llm_router.generate_response("prompt", force_scriptwriter=True)
    assert captured_models[0] == "claude-3-7-sonnet-20250219", f"Expected claude-3-7-sonnet-20250219, got {captured_models[0]}"
    print("PASS: force_scriptwriter routes to claude-3-7-sonnet-20250219")
    
    # 3. Test local LLM fallback (USE_LOCAL_LLM = True)
    cfg_module.config.USE_LOCAL_LLM = True
    captured_models.clear()
    llm_router.generate_response("prompt")
    assert captured_models[0] == "ollama/llama3", f"Expected ollama/llama3, got {captured_models[0]}"
    print("PASS: USE_LOCAL_LLM=True defaults to ollama/llama3")
    
    # 4. Test cloud LLM default (USE_LOCAL_LLM = False)
    cfg_module.config.USE_LOCAL_LLM = False
    captured_models.clear()
    llm_router.generate_response("prompt")
    assert captured_models[0] == cfg_module.config.LITELLM_DEFAULT_MODEL, f"Expected {cfg_module.config.LITELLM_DEFAULT_MODEL}, got {captured_models[0]}"
    print(f"PASS: USE_LOCAL_LLM=False defaults to {cfg_module.config.LITELLM_DEFAULT_MODEL}")

def test_engine_graph():
    print("--- Testing Engine Graph Compilation ---")
    graph = build_graph()
    nodes = list(graph.nodes.keys())
    print(f"Graph nodes: {nodes}")
    expected_nodes = ["intake", "orchestrator", "researcher", "packaging", "architect", "scriptwriter", "storyboarder", "auditor"]
    for expected in expected_nodes:
        assert expected in nodes, f"Missing node: {expected}"
    print("PASS: All 8 nodes present in StateGraph (including 6 conveyor belt agents)")

if __name__ == "__main__":
    test_router_logic()
    test_engine_graph()
    print("ALL INDEPENDENT VERIFICATION TESTS PASSED SUCCESSFULLY!")
