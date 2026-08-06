# -*- coding: utf-8 -*-
import os
import json
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.connectors.learning_engine import ViralLearningEngine

def test_edge_cases():
    print("=== TESTING ADVERSARIAL EDGE CASES ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "partial_kb.json")
        md_path = os.path.join(tmpdir, "partial_patterns.md")
        
        # Scenario 1: Partial JSON on disk missing 3 categories
        partial_data = {
            "version": "1.0.0",
            "last_updated": "2026-01-01T00:00:00Z",
            "analyzed_videos_count": 1,
            "patterns": {
                "hooks": [{"id": "H1", "pattern": "test hook"}]
            }
        }
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(partial_data, f)
            
        engine = ViralLearningEngine(db_path=db_path, patterns_md_path=md_path)
        
        # Check that missing 5 categories were filled automatically
        cats = engine.data["patterns"]
        assert len(cats) == 6, f"Expected 6 categories, got {len(cats)}"
        assert len(cats["hooks"]) == 1
        assert cats["analogies"] == []
        assert cats["sensory_beats"] == []
        print("[PASS] Scenario 1: Missing categories auto-repaired on load.")
        
        # Scenario 2: Item with pipes and newlines in text fields (Markdown injection)
        engine.data["patterns"]["analogies"].append({
            "id": "ANA_BAD",
            "concept": "Concept | with | pipes",
            "domestic_comparison": "Line1\nLine2",
            "example": "Normal",
            "adapted_for_channel": "Adapted | Pipe"
        })
        engine.save_database()
        
        with open(md_path, "r", encoding="utf-8") as f:
            md = f.read()
            
        # Check that pipes are escaped as \| and newlines replaced with spaces
        assert r"Concept \| with \| pipes" in md or "Concept \\| with \\| pipes" in md
        assert "Line1 Line2" in md
        print("[PASS] Scenario 2: Markdown table injection prevented.")

    print("=== ALL ADVERSARIAL EDGE CASES PASSED ===")

if __name__ == "__main__":
    test_edge_cases()
