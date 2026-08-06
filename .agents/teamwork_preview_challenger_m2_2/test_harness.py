import os
import sys
import shutil
import tempfile
import json
import traceback

# Ensure src directory is in sys.path
workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from src.connectors.learning_engine import ViralLearningEngine

def run_tests():
    temp_dir = tempfile.mkdtemp(prefix="learning_engine_test_")
    print(f"=== Running tests in temporary directory: {temp_dir} ===")

    results = []

    # -------------------------------------------------------------
    # TEST 1: Default initialization and initial patterns.md sync
    # -------------------------------------------------------------
    try:
        db_path = os.path.join(temp_dir, "test_kb.json")
        md_path = os.path.join(temp_dir, "test_patterns.md")

        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)

        assert os.path.exists(md_path), "patterns.md should be created on initialization if missing"
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        categories = [
            "## 🪝 1. Retention Hooks & Scale Contrast (`hooks`)",
            "## 💡 2. Everyday Domestic Analogies (`analogies`)",
            "## 🌀 3. Micro-Twists & Expectation Inversion (`micro_twists`)",
            "## 👁️ 4. Sensory Immersion Beats (`sensory_beats`)",
            "## 📣 5. Organic Soft CTAs (`ctas`)",
            "## ⏱️ 6. Retention Tactics & Open Loops (`retention_tactics`)"
        ]

        missing_cats = [cat for cat in categories if cat not in content]
        if missing_cats:
            results.append(("TEST 1: Initial patterns.md sync", "FAIL", f"Missing categories: {missing_cats}"))
        else:
            results.append(("TEST 1: Initial patterns.md sync", "PASS", "All 6 category tables present in initial patterns.md"))

    except Exception as e:
        results.append(("TEST 1: Initial patterns.md sync", "FAIL", f"Exception: {e}\n{traceback.format_exc()}"))

    # -------------------------------------------------------------
    # TEST 2: Populate all 6 categories and test atomic save
    # -------------------------------------------------------------
    try:
        engine.data["patterns"]["hooks"].append({
            "id": "HOOK_001",
            "type": "scale_contrast",
            "example_source": "Source Video 1",
            "pattern": "Big vs Small",
            "adapted_for_channel": "Adapted Hook 1"
        })
        engine.data["patterns"]["analogies"].append({
            "id": "ANA_001",
            "concept": "Dopamine spike",
            "domestic_comparison": "Sugar rush",
            "example": "Original phrase",
            "adapted_for_channel": "Adapted analogy 1"
        })
        engine.data["patterns"]["micro_twists"].append({
            "id": "TWIST_001",
            "trigger": "Contrarian truth",
            "phrase": "Original twist",
            "adapted_for_channel": "Adapted twist 1"
        })
        engine.data["patterns"]["sensory_beats"].append({
            "id": "SENS_001",
            "type": "auditory",
            "template": "Sound of click",
            "adapted_for_channel": "Adapted sensory 1"
        })
        engine.data["patterns"]["ctas"].append({
            "id": "CTA_001",
            "type": "soft_mid",
            "template": "Subscribe if like",
            "adapted_for_channel": "Adapted CTA 1"
        })
        engine.data["patterns"]["retention_tactics"].append({
            "id": "TAC_001",
            "tactic": "Open loop",
            "mechanism": "Curiosity gap",
            "pacing_interval": "60s",
            "adapted_for_channel": "Adapted tactic 1"
        })

        engine.save_database()

        # Check atomic save files
        assert os.path.exists(db_path), "JSON db file should exist"
        assert not os.path.exists(f"{db_path}.tmp"), "JSON tmp file should be cleaned up"
        assert not os.path.exists(f"{md_path}.tmp"), "MD tmp file should be cleaned up"

        with open(md_path, "r", encoding="utf-8") as f:
            updated_md = f.read()

        check_elements = [
            "HOOK_001", "ANA_001", "TWIST_001", "SENS_001", "CTA_001", "TAC_001",
            "Adapted Hook 1", "Adapted analogy 1", "Adapted twist 1",
            "Adapted sensory 1", "Adapted CTA 1", "Adapted tactic 1"
        ]

        missing_elements = [elem for elem in check_elements if elem not in updated_md]
        if missing_elements:
            results.append(("TEST 2: Atomic save & content sync", "FAIL", f"Missing elements in markdown: {missing_elements}"))
        else:
            results.append(("TEST 2: Atomic save & content sync", "PASS", "All populated items saved atomically and synced to patterns.md"))

    except Exception as e:
        results.append(("TEST 2: Atomic save & content sync", "FAIL", f"Exception: {e}\n{traceback.format_exc()}"))

    # -------------------------------------------------------------
    # TEST 3: Edge cases with empty dicts / None values
    # -------------------------------------------------------------
    # 3a: Empty dict in self.data
    try:
        sub_dir = os.path.join(temp_dir, "empty_dict_test")
        os.makedirs(sub_dir, exist_ok=True)
        e3 = ViralLearningEngine(
            db_path=os.path.join(sub_dir, "kb.json"),
            patterns_md_path=os.path.join(sub_dir, "patterns.md")
        )
        e3.data = {}
        e3._update_patterns_md()
        with open(os.path.join(sub_dir, "patterns.md"), "r", encoding="utf-8") as f:
            content = f.read()
        assert "(Nenhum padrão registrado)" in content
        results.append(("TEST 3a: empty dict e3.data={}", "PASS", "Handled self.data={} gracefully"))
    except Exception as e:
        results.append(("TEST 3a: empty dict e3.data={}", "FAIL", f"Exception on self.data={{}}: {e}"))

    # 3b: engine.data = {"patterns": {}}
    try:
        sub_dir = os.path.join(temp_dir, "empty_patterns_test")
        os.makedirs(sub_dir, exist_ok=True)
        e3b = ViralLearningEngine(
            db_path=os.path.join(sub_dir, "kb.json"),
            patterns_md_path=os.path.join(sub_dir, "patterns.md")
        )
        e3b.data = {"patterns": {}}
        e3b._update_patterns_md()
        results.append(("TEST 3b: empty patterns dict", "PASS", "Handled patterns={} gracefully"))
    except Exception as e:
        results.append(("TEST 3b: empty patterns dict", "FAIL", f"Exception on patterns={{}}: {e}"))

    # 3c: engine.data = {"patterns": None}
    try:
        sub_dir = os.path.join(temp_dir, "none_patterns_test")
        os.makedirs(sub_dir, exist_ok=True)
        e3c = ViralLearningEngine(
            db_path=os.path.join(sub_dir, "kb.json"),
            patterns_md_path=os.path.join(sub_dir, "patterns.md")
        )
        e3c.data = {"patterns": None}
        e3c._update_patterns_md()
        results.append(("TEST 3c: patterns=None", "PASS", "Handled patterns=None gracefully"))
    except Exception as e:
        results.append(("TEST 3c: patterns=None", "FAIL", f"Exception on patterns=None: {e}"))

    # 3d: Existing JSON on disk with {"patterns": null}
    try:
        sub_dir = os.path.join(temp_dir, "null_json_test")
        os.makedirs(sub_dir, exist_ok=True)
        json_file = os.path.join(sub_dir, "null_patterns.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "patterns": None}, f)

        e3d = ViralLearningEngine(
            db_path=json_file,
            patterns_md_path=os.path.join(sub_dir, "patterns.md")
        )
        results.append(("TEST 3d: JSON with patterns: null", "PASS", "Loaded JSON with null patterns gracefully"))
    except Exception as e:
        results.append(("TEST 3d: JSON with patterns: null", "FAIL", f"Exception on loading null patterns JSON: {e}"))

    # -------------------------------------------------------------
    # TEST 4: Malformed paths / invalid path resilience
    # -------------------------------------------------------------
    # 4a: Directory passed as db_path
    try:
        sub_dir = os.path.join(temp_dir, "dir_as_db_test")
        os.makedirs(sub_dir, exist_ok=True)
        e4a = ViralLearningEngine(
            db_path=sub_dir, # directory!
            patterns_md_path=os.path.join(sub_dir, "patterns.md")
        )
        e4a.save_database()
        results.append(("TEST 4a: Directory as db_path", "PASS", "Handled directory as db_path"))
    except Exception as e:
        results.append(("TEST 4a: Directory as db_path", "FAIL", f"Exception: {type(e).__name__}: {e}"))

    # 4b: Directory passed as patterns_md_path
    try:
        sub_dir = os.path.join(temp_dir, "dir_as_md_test")
        os.makedirs(sub_dir, exist_ok=True)
        e4b = ViralLearningEngine(
            db_path=os.path.join(sub_dir, "kb.json"),
            patterns_md_path=sub_dir # directory!
        )
        e4b._update_patterns_md()
        results.append(("TEST 4b: Directory as patterns_md_path", "PASS", "Handled directory as patterns_md_path"))
    except Exception as e:
        results.append(("TEST 4b: Directory as patterns_md_path", "FAIL", f"Exception: {type(e).__name__}: {e}"))

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n=================== TEST RESULTS ===================")
    for name, status, detail in results:
        print(f"[{status}] {name} -> {detail}")

if __name__ == "__main__":
    run_tests()
