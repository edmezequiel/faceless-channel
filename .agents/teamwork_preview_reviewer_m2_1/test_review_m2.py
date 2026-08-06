# -*- coding: utf-8 -*-
import os
import json
import tempfile
import sys

# Ensure root path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.connectors.learning_engine import ViralLearningEngine

def run_tests():
    print("=== STARTING REVIEWER VERIFICATION FOR LEARNING ENGINE ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_kb.json")
        md_path = os.path.join(tmpdir, "test_patterns.md")
        
        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)
        
        # 1. Verify 6 categories in data
        patterns = engine.data.get("patterns", {})
        expected_cats = {"hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"}
        assert set(patterns.keys()) == expected_cats, f"Missing categories: {expected_cats - set(patterns.keys())}"
        print("[PASS] 1. Category completeness check passed.")
        
        # 2. Verify format_patterns_for_prompt output
        formatted = engine.format_patterns_for_prompt()
        assert "1. HOOKS E PARADOXOS DE RETENÇÃO:" in formatted
        assert "2. ANALOGIAS DOMÉSTICAS DO DIA A DIA:" in formatted
        assert "3. MICRO-TWISTS & INVERSÃO DE EXPECTATIVAS:" in formatted
        assert "4. IMERSÃO SENSORIAL E SIMULAÇÕES:" in formatted
        assert "5. SOFT CTAs ORGÂNICOS DE MEIO DE VÍDEO:" in formatted
        assert "6. TÁTICAS DE RETENÇÃO E OPEN LOOPS:" in formatted
        print("[PASS] 2. Prompt formatting check passed.")
        
        # 3. Add sample data to all 6 categories and test save + patterns.md sync
        sample_data = {
            "hooks": [{"id": "HOOK_01", "type": "paradox", "template": "Hook template", "adapted_for_channel": "Hook adapted"}],
            "analogies": [{"id": "ANA_01", "concept": "Concept", "domestic_comparison": "Domestic", "example": "Ex", "adapted_for_channel": "Ana adapted"}],
            "micro_twists": [{"id": "TWIST_01", "trigger": "Trigger", "phrase": "Phrase", "adapted_for_channel": "Twist adapted"}],
            "sensory_beats": [{"id": "SENS_01", "type": "first_person", "template": "Sensory template", "adapted_for_channel": "Sensory adapted"}],
            "ctas": [{"id": "CTA_01", "type": "mid_video", "template": "CTA template", "adapted_for_channel": "CTA adapted"}],
            "retention_tactics": [{"id": "TAC_01", "tactic": "Open Loop", "mechanism": "Mechanism", "pacing_interval": "Pacing", "adapted_for_channel": "Tac adapted"}]
        }
        
        for cat, items in sample_data.items():
            patterns[cat].extend(items)
        
        engine.save_database()
        assert os.path.exists(db_path)
        assert os.path.exists(md_path)
        
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        assert "Retention Hooks & Scale Contrast (`hooks`)" in md_content
        assert "Everyday Domestic Analogies (`analogies`)" in md_content
        assert "Micro-Twists & Expectation Inversion (`micro_twists`)" in md_content
        assert "Sensory Immersion Beats (`sensory_beats`)" in md_content
        assert "Organic Soft CTAs (`ctas`)" in md_content
        assert "Retention Tactics & Open Loops (`retention_tactics`)" in md_content
        
        # Verify rendered items in tables
        assert "Hook adapted" in md_content
        assert "Ana adapted" in md_content
        assert "Twist adapted" in md_content
        assert "Sensory adapted" in md_content
        assert "CTA adapted" in md_content
        assert "Tac adapted" in md_content
        print("[PASS] 3. Atomic save & Markdown sync check passed.")
        
        # 4. Verify formatted output with loaded patterns
        formatted_populated = engine.format_patterns_for_prompt()
        assert "Hook adapted" in formatted_populated
        assert "Ana adapted" in formatted_populated
        assert "Twist adapted" in formatted_populated
        assert "Sensory adapted" in formatted_populated
        assert "CTA adapted" in formatted_populated
        assert "Tac adapted" in formatted_populated
        print("[PASS] 4. Populated prompt formatting check passed.")

    print("\n=== ALL REVIEWER TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
