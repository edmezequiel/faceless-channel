import sys
import os
import tempfile
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath("."))

from src.connectors.learning_engine import ViralLearningEngine

REQUIRED_TAGS = [
    "[RETENTION HOOKS]",
    "[DOMESTIC ANALOGIES]",
    "[MICRO-TWISTS]",
    "[SENSORY BEATS]",
    "[SOFT CTAS]",
    "[RETENTION TACTICS]"
]

def test_default_format():
    print("--- Test 1: Default DB format_patterns_for_prompt() ---")
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_file = os.path.join(tmp_dir, "kb.json")
        md_file = os.path.join(tmp_dir, "patterns.md")
        engine = ViralLearningEngine(db_path=db_file, patterns_md_path=md_file)
        formatted = engine.format_patterns_for_prompt()
        print("Formatted output:")
        print(formatted)
        
        for tag in REQUIRED_TAGS:
            assert tag in formatted, f"FAILED: Tag '{tag}' missing from output!"
            print(f"  [PASS] Found '{tag}'")

def test_populated_format():
    print("--- Test 2: Populated DB format_patterns_for_prompt() ---")
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_file = os.path.join(tmp_dir, "kb.json")
        md_file = os.path.join(tmp_dir, "patterns.md")
        data = {
            "version": "1.0.0",
            "last_updated": "2026-08-06T12:00:00Z",
            "analyzed_videos_count": 5,
            "patterns": {
                "hooks": [{"type": "paradox", "pattern": "O segredo oculto", "adapted_for_channel": "Hook adaptado"}],
                "analogies": [{"concept": "Dopamina", "domestic_comparison": "Café", "example": "Como tomar café"}],
                "micro_twists": [{"trigger": "porém", "phrase": "Mas a verdade é outra"}],
                "sensory_beats": [{"type": "auditivo", "template": "Ouça o sussurro..."}],
                "ctas": [{"type": "soft", "template": "Comente abaixo..."}],
                "retention_tactics": [{"tactic": "loop", "mechanism": "Pergunta aberta", "pacing_interval": "30s"}]
            }
        }
        with open(db_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
            
        engine = ViralLearningEngine(db_path=db_file, patterns_md_path=md_file)
        formatted = engine.format_patterns_for_prompt()
        print("Populated Formatted output:")
        print(formatted)
        
        for tag in REQUIRED_TAGS:
            assert tag in formatted, f"FAILED: Tag '{tag}' missing from populated output!"
            print(f"  [PASS] Found '{tag}'")

def main():
    try:
        test_default_format()
        test_populated_format()
        print("\nALL EMPIRICAL TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
