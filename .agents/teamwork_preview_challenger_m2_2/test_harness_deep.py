import os
import sys
import shutil
import tempfile
import json
import traceback

workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from src.connectors.learning_engine import ViralLearningEngine

def run_deep_tests():
    temp_dir = tempfile.mkdtemp(prefix="learning_engine_deep_")
    print(f"=== Running DEEP tests in temporary directory: {temp_dir} ===")
    results = []

    # -------------------------------------------------------------
    # TEST 5: Special characters in pattern entries (\n, |, nulls)
    # -------------------------------------------------------------
    try:
        db_path = os.path.join(temp_dir, "special_kb.json")
        md_path = os.path.join(temp_dir, "special_patterns.md")

        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)
        engine.data["patterns"]["hooks"].append({
            "id": "HOOK|001\nLine2",
            "type": "scale | contrast",
            "example_source": "Source | Video",
            "pattern": "Pattern with | pipe and \n newline",
            "adapted_for_channel": None # null value
        })
        engine.save_database()

        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Ensure no line in the markdown table contains unescaped raw newlines breaking table syntax
        hook_table_lines = [l for l in lines if "HOOK\\|001" in l or "HOOK|001" in l]
        assert len(hook_table_lines) == 1, f"Expected 1 line for HOOK, got {len(hook_table_lines)}: {hook_table_lines}"
        assert "\\|" in hook_table_lines[0], "Pipes should be escaped with \\|"
        assert "\n" not in hook_table_lines[0][:-1], "Newlines inside cells should be replaced by spaces"
        assert "N/A" in hook_table_lines[0], "None value should be replaced with N/A"

        results.append(("TEST 5: Special character sanitization in markdown", "PASS", "Pipes, newlines, and Nones handled safely"))
    except Exception as e:
        results.append(("TEST 5: Special character sanitization in markdown", "FAIL", f"Exception: {e}\n{traceback.format_exc()}"))

    # -------------------------------------------------------------
    # TEST 6: format_patterns_for_prompt() correctness
    # -------------------------------------------------------------
    try:
        db_path = os.path.join(temp_dir, "prompt_kb.json")
        md_path = os.path.join(temp_dir, "prompt_patterns.md")
        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)

        prompt_str = engine.format_patterns_for_prompt()
        assert "APRENDIZADOS ACUMULADOS DOS MAIORES VÍDEOS VIRAIS" in prompt_str
        assert "1. HOOKS E PARADOXOS DE RETENÇÃO:" in prompt_str
        assert "2. ANALOGIAS DOMÉSTICAS DO DIA A DIA:" in prompt_str
        assert "3. MICRO-TWISTS & INVERSÃO DE EXPECTATIVAS:" in prompt_str
        assert "4. IMERSÃO SENSORIAL E SIMULAÇÕES:" in prompt_str
        assert "5. SOFT CTAs ORGÂNICOS DE MEIO DE VÍDEO:" in prompt_str
        assert "6. TÁTICAS DE RETENÇÃO E OPEN LOOPS:" in prompt_str

        results.append(("TEST 6: format_patterns_for_prompt() format", "PASS", "Returns formatted prompt containing all 6 categories"))
    except Exception as e:
        results.append(("TEST 6: format_patterns_for_prompt() format", "FAIL", f"Exception: {e}\n{traceback.format_exc()}"))

    # -------------------------------------------------------------
    # TEST 7: Invalid item types inside category lists (e.g. non-dict elements)
    # -------------------------------------------------------------
    try:
        db_path = os.path.join(temp_dir, "invalid_item_kb.json")
        md_path = os.path.join(temp_dir, "invalid_item_patterns.md")
        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)
        engine.data["patterns"]["hooks"].append("Not a dict!") # string inside list
        try:
            engine._update_patterns_md()
            results.append(("TEST 7: Non-dict in pattern list", "FAIL", "Did not raise exception when category list contained a string instead of dict"))
        except AttributeError as ae:
            results.append(("TEST 7: Non-dict in pattern list", "FAIL (Known Limit)", f"AttributeError raised when item in list is non-dict: {ae}"))
    except Exception as e:
        results.append(("TEST 7: Non-dict in pattern list", "FAIL", f"Unexpected exception: {e}"))

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n=================== DEEP TEST RESULTS ===================")
    for name, status, detail in results:
        print(f"[{status}] {name} -> {detail}")

if __name__ == "__main__":
    run_deep_tests()
