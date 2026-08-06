# -*- coding: utf-8 -*-
import os
import json
import re
import sys

def run_empirical_verification():
    root_dir = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
    kb_path = os.path.join(root_dir, "memory", "viral_knowledge_bank", "knowledge_base.json")
    md_path = os.path.join(root_dir, "memory", "viral_knowledge_bank", "patterns.md")
    
    results = {
        "kb_file_exists": False,
        "md_file_exists": False,
        "json_valid": False,
        "top_level_keys": False,
        "all_6_categories_present": False,
        "categories_non_empty": {},
        "entries_valid": {},
        "md_headers_present": False,
        "md_sync_exact": False,
        "errors": []
    }
    
    # 1. Check existence
    if os.path.exists(kb_path):
        results["kb_file_exists"] = True
    else:
        results["errors"].append(f"knowledge_base.json not found at {kb_path}")
        
    if os.path.exists(md_path):
        results["md_file_exists"] = True
    else:
        results["errors"].append(f"patterns.md not found at {md_path}")
        
    if not results["kb_file_exists"]:
        return results

    # 2. Parse JSON
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            kb_data = json.load(f)
        results["json_valid"] = True
    except Exception as e:
        results["errors"].append(f"Failed to parse knowledge_base.json: {e}")
        return results

    # 3. Top level keys
    required_top_keys = ["version", "last_updated", "analyzed_videos_count", "patterns"]
    missing_top_keys = [k for k in required_top_keys if k not in kb_data]
    if not missing_top_keys:
        results["top_level_keys"] = True
    else:
        results["errors"].append(f"Missing top-level keys in knowledge_base.json: {missing_top_keys}")

    # 4. Check 6 categories
    expected_categories = ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]
    patterns = kb_data.get("patterns", {})
    
    missing_cats = [c for c in expected_categories if c not in patterns]
    if not missing_cats:
        results["all_6_categories_present"] = True
    else:
        results["errors"].append(f"Missing categories in patterns dict: {missing_cats}")

    # 5. Check category contents and valid entries
    for cat in expected_categories:
        items = patterns.get(cat, [])
        is_list = isinstance(items, list)
        count = len(items) if is_list else 0
        results["categories_non_empty"][cat] = (is_list and count > 0, count)
        
        if not is_list or count == 0:
            results["errors"].append(f"Category '{cat}' is empty or not a list")
        else:
            # Validate individual entries
            invalid_entries = 0
            for idx, item in enumerate(items):
                if not isinstance(item, dict) or len(item) == 0:
                    invalid_entries += 1
            results["entries_valid"][cat] = (invalid_entries == 0, count - invalid_entries, count)
            if invalid_entries > 0:
                results["errors"].append(f"Category '{cat}' has {invalid_entries} invalid/empty entries out of {count}")

    # 6. Check patterns.md
    if results["md_file_exists"]:
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        # Check section headers in markdown
        cat_headers = {
            "hooks": "1. Retention Hooks & Scale Contrast (`hooks`)",
            "analogies": "2. Everyday Domestic Analogies (`analogies`)",
            "micro_twists": "3. Micro-Twists & Expectation Inversion (`micro_twists`)",
            "sensory_beats": "4. Sensory Immersion Beats (`sensory_beats`)",
            "ctas": "5. Organic Soft CTAs (`ctas`)",
            "retention_tactics": "6. Retention Tactics & Open Loops (`retention_tactics`)"
        }
        
        missing_md_headers = [cat for cat, header in cat_headers.items() if header not in md_content]
        if not missing_md_headers:
            results["md_headers_present"] = True
        else:
            results["errors"].append(f"Missing headers in patterns.md for categories: {missing_md_headers}")

        # Test sync with ViralLearningEngine code
        try:
            sys.path.insert(0, root_dir)
            from src.connectors.learning_engine import ViralLearningEngine
            engine = ViralLearningEngine(db_path=kb_path, patterns_md_path=md_path)
            
            # Generate expected md string using engine logic
            # Let's inspect what engine._update_patterns_md() generates vs actual md_content
            # We can capture generated markdown by writing to a temporary file
            temp_md_test = md_path + ".verify_tmp"
            engine_test = ViralLearningEngine(db_path=kb_path, patterns_md_path=temp_md_test)
            engine_test._update_patterns_md()
            
            with open(temp_md_test, "r", encoding="utf-8") as f:
                generated_md = f.read()
                
            if os.path.exists(temp_md_test):
                os.remove(temp_md_test)
                
            if md_content.strip() == generated_md.strip():
                results["md_sync_exact"] = True
            else:
                results["errors"].append("patterns.md is not 100% byte-for-byte in sync with ViralLearningEngine generator")
                # Measure differences
                results["md_diff_details"] = f"Actual len: {len(md_content)}, Generated len: {len(generated_md)}"
        except Exception as e:
            results["errors"].append(f"Failed during sync generation test: {e}")

    return results

if __name__ == "__main__":
    res = run_empirical_verification()
    print(json.dumps(res, indent=2, ensure_ascii=False))
