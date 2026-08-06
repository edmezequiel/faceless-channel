# -*- coding: utf-8 -*-
import os
import json
import sys

def run_deep_test():
    root_dir = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
    sys.path.insert(0, root_dir)
    from src.connectors.learning_engine import ViralLearningEngine

    kb_path = os.path.join(root_dir, "memory", "viral_knowledge_bank", "knowledge_base.json")
    md_path = os.path.join(root_dir, "memory", "viral_knowledge_bank", "patterns.md")

    print("=== DEEP SCHEMA & SYNCHRONIZATION TEST ===")
    
    engine = ViralLearningEngine(db_path=kb_path, patterns_md_path=md_path)
    
    # Check 1: Top-level properties
    print(f"[1] Version: {engine.data.get('version')}")
    print(f"[1] Last Updated: {engine.data.get('last_updated')}")
    print(f"[1] Analyzed Videos Count: {engine.data.get('analyzed_videos_count')}")
    assert engine.data.get("version") == "1.0.0", "Version mismatch"
    assert engine.data.get("analyzed_videos_count") == 5, "Analyzed videos count mismatch"
    
    # Check 2: 6 Categories in patterns dict
    patterns = engine.get_top_patterns()
    expected_cats = ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]
    for cat in expected_cats:
        assert cat in patterns, f"Category {cat} missing from patterns"
        items = patterns[cat]
        assert isinstance(items, list), f"Category {cat} is not a list"
        assert len(items) > 0, f"Category {cat} is empty"
        print(f"[2] Category '{cat}': {len(items)} entries (PASS)")

    # Check 3: Format patterns for prompt
    prompt_str = engine.format_patterns_for_prompt()
    for idx, label in enumerate(["[RETENTION HOOKS]", "[DOMESTIC ANALOGIES]", "[MICRO-TWISTS]", "[SENSORY BEATS]", "[SOFT CTAS]", "[RETENTION TACTICS]"], start=1):
        assert label in prompt_str, f"Prompt string missing section label {label}"
    print("[3] format_patterns_for_prompt() verified with all 6 categories (PASS)")

    # Check 4: Markdown File Sync Check
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    for cat in expected_cats:
        assert f"(`{cat}`)" in md_text, f"Markdown missing header tag (`{cat}`)"
    
    print("[4] Markdown header tags verified for all 6 categories (PASS)")

    print("\nALL DEEP VERIFICATION CHECKS PASSED PERFECTLY!")
    return True

if __name__ == "__main__":
    run_deep_test()
