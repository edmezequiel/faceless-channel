import sys
import os
import tempfile
import json
import py_compile

workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from src.connectors.learning_engine import ViralLearningEngine

def test_stress():
    results = {}
    
    # 1. py_compile check
    target_file = os.path.join(workspace_root, "src", "connectors", "learning_engine.py")
    try:
        py_compile.compile(target_file, doraise=True)
        results["py_compile"] = "PASS"
    except Exception as e:
        results["py_compile"] = f"FAIL: {e}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_db = os.path.join(tmpdir, "nested", "db.json")
        tmp_md = os.path.join(tmpdir, "nested", "patterns.md")

        # 2. Instantiation with missing directories
        try:
            engine = ViralLearningEngine(db_path=tmp_db, patterns_md_path=tmp_md)
            results["instantiation_missing_dir"] = "PASS"
        except Exception as e:
            results["instantiation_missing_dir"] = f"FAIL: {e}"

        # 3. format_patterns_for_prompt output check for category tags
        out = engine.format_patterns_for_prompt()
        required_tags = [
            "[RETENTION HOOKS]",
            "[DOMESTIC ANALOGIES]",
            "[MICRO-TWISTS]",
            "[SENSORY BEATS]",
            "[SOFT CTAS]",
            "[RETENTION TACTICS]"
        ]
        missing_tags = [tag for tag in required_tags if tag not in out]
        if missing_tags:
            results["format_patterns_category_tags"] = f"FAIL: Missing tags {missing_tags}"
        else:
            results["format_patterns_category_tags"] = "PASS"

        # 4. Save database creates directory and file atomically
        try:
            engine.save_database()
            if os.path.exists(tmp_db) and os.path.exists(tmp_md):
                results["save_database_creation"] = "PASS"
            else:
                results["save_database_creation"] = "FAIL: Files not created"
        except Exception as e:
            results["save_database_creation"] = f"FAIL: {e}"

        # 5. Load corrupted JSON
        corrupt_db = os.path.join(tmpdir, "corrupt.json")
        with open(corrupt_db, "w", encoding="utf-8") as f:
            f.write("{ invalid json")
        try:
            engine_corrupt = ViralLearningEngine(db_path=corrupt_db, patterns_md_path=tmp_md)
            # Should fall back to default KB without crashing
            if engine_corrupt.data.get("version") == "1.0.0":
                results["corrupt_json_fallback"] = "PASS"
            else:
                results["corrupt_json_fallback"] = "FAIL: Did not return default KB"
        except Exception as e:
            results["corrupt_json_fallback"] = f"FAIL: Crashed on corrupt JSON: {e}"

    print("--- STRESS TEST RESULTS ---")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_stress()
