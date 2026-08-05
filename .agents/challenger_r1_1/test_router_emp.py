from unittest.mock import patch, MagicMock
from src.connectors.llm_router import generate_response
from src.core.config import config
from src.nodes.tts_scriptwriter import node_tts_scriptwriter

def test_router():
    mock_res = MagicMock()
    mock_res.choices = [MagicMock()]
    mock_res.choices[0].message.content = 'Generated text response'

    with patch('src.connectors.llm_router.completion', return_value=mock_res) as mock_comp:
        # Subtest A: force_claude_sonnet=True
        res_a = generate_response(prompt='Test prompt A', force_claude_sonnet=True)
        model_a = mock_comp.call_args[1].get('model')
        print(f'[TEST A PASS] force_claude_sonnet=True -> target_model = {model_a}')
        assert model_a in ['claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-latest'], f'FAIL: Expected Claude model, got {model_a}'

        # Subtest B: force_scriptwriter=True
        mock_comp.reset_mock()
        res_b = generate_response(prompt='Test prompt B', force_scriptwriter=True)
        model_b = mock_comp.call_args[1].get('model')
        print(f'[TEST B PASS] force_scriptwriter=True -> target_model = {model_b}')
        assert model_b in ['claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-latest'], f'FAIL: Expected Claude model, got {model_b}'

        # Subtest C: Standard call without kwargs when USE_LOCAL_LLM=True
        mock_comp.reset_mock()
        config.USE_LOCAL_LLM = True
        res_c = generate_response(prompt='Test prompt C')
        model_c = mock_comp.call_args[1].get('model')
        print(f'[TEST C PASS] USE_LOCAL_LLM=True without kwargs -> target_model = {model_c}')
        assert model_c == 'ollama/llama3', f'FAIL: Expected ollama/llama3, got {model_c}'

        # Subtest D: Call from node_tts_scriptwriter directly
        mock_comp.reset_mock()
        mock_res.choices[0].message.content = '{"tts_prose": "Roteiro sem AI slop."}'
        state = {'script_skeleton': {'hook': 'Hook test'}, 'factual_context': 'Fact context', 'auditor_feedback': ''}
        out = node_tts_scriptwriter(state)
        model_d = mock_comp.call_args[1].get('model')
        print(f'[TEST D PASS] node_tts_scriptwriter call -> target_model = {model_d}')
        assert model_d in ['claude-3-7-sonnet-20250219', 'claude-3-5-sonnet-latest'], f'FAIL: Expected Claude model in tts_scriptwriter, got {model_d}'

    print('=== ALL EMPIRICAL ROUTER TESTS PASSED SUCCESSFULLY! ===')

if __name__ == '__main__':
    test_router()
