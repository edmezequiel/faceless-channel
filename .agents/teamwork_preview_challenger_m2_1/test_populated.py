import sys
import os
import tempfile
import json

workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from src.connectors.learning_engine import ViralLearningEngine

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_db = os.path.join(tmpdir, "db.json")
    tmp_md = os.path.join(tmpdir, "patterns.md")
    
    # Populate db with sample items across all 6 categories
    data = {
        "version": "1.0.0",
        "last_updated": "2026-08-06T12:00:00Z",
        "analyzed_videos_count": 1,
        "patterns": {
            "hooks": [{"type": "question", "pattern": "Why do we sleep?", "adapted_for_channel": "Why do we fail?"}],
            "analogies": [{"concept": "RAM memory", "domestic_comparison": "Desk space", "example": "Your brain desk"}],
            "micro_twists": [{"trigger": "but wait", "phrase": "However, that is wrong", "adapted_for_channel": "Or is it?"}],
            "sensory_beats": [{"type": "tactile", "template": "Feel the cold sweat", "adapted_for_channel": "Cold sweat"}],
            "ctas": [{"type": "subscribe", "template": "Join the lab", "adapted_for_channel": "Subscribe"}],
            "retention_tactics": [{"tactic": "open_loop", "mechanism": "Curiosity gap", "adapted_for_channel": "Stay tuned"}]
        }
    }
    with open(tmp_db, "w", encoding="utf-8") as f:
        json.dump(data, f)
        
    engine = ViralLearningEngine(db_path=tmp_db, patterns_md_path=tmp_md)
    output = engine.format_patterns_for_prompt()
    
    print("\n--- OUTPUT WITH POPULATED DATA ---")
    print(output)
    print("----------------------------------\n")
    
    required_blocks = [
        "[RETENTION HOOKS]",
        "[DOMESTIC ANALOGIES]",
        "[MICRO-TWISTS]",
        "[SENSORY BEATS]",
        "[SOFT CTAS]",
        "[RETENTION TACTICS]"
    ]
    
    for b in required_blocks:
        print(f"Contains '{b}'? -> {b in output}")
