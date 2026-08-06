import json
import os
import sys

def run_empirical_validation():
    workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
    json_path = os.path.join(workspace_root, "memory", "viral_knowledge_bank", "knowledge_base.json")
    md_path = os.path.join(workspace_root, "memory", "viral_knowledge_bank", "patterns.md")

    results = {
        "json_exists": False,
        "json_valid_syntax": False,
        "root_keys_present": False,
        "patterns_keys_present": False,
        "categories_non_empty": False,
        "category_counts": {},
        "md_exists": False,
        "md_all_ids_present": False,
        "errors": []
    }

    # 1. Check file existence
    if not os.path.isfile(json_path):
        results["errors"].append(f"JSON file missing: {json_path}")
        return results
    results["json_exists"] = True

    # 2. Check JSON parse
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        results["json_valid_syntax"] = True
    except Exception as e:
        results["errors"].append(f"JSON parse error: {str(e)}")
        return results

    # 3. Check root keys
    required_root_keys = ["version", "last_updated", "analyzed_videos_count", "patterns"]
    missing_root = [k for k in required_root_keys if k not in data]
    if missing_root:
        results["errors"].append(f"Missing root keys in JSON: {missing_root}")
    else:
        results["root_keys_present"] = True

    # 4. Check patterns sub-keys
    required_pattern_keys = ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]
    patterns = data.get("patterns", {})
    if not isinstance(patterns, dict):
        results["errors"].append("'patterns' key is not a JSON object")
        return results

    missing_pattern_keys = [k for k in required_pattern_keys if k not in patterns]
    if missing_pattern_keys:
        results["errors"].append(f"Missing pattern category keys: {missing_pattern_keys}")
    else:
        results["patterns_keys_present"] = True

    # 5. Check each category is a non-empty list
    all_non_empty = True
    for cat in required_pattern_keys:
        val = patterns.get(cat)
        if not isinstance(val, list):
            results["errors"].append(f"Category '{cat}' is not a list")
            all_non_empty = False
        elif len(val) == 0:
            results["errors"].append(f"Category '{cat}' is an empty list")
            all_non_empty = False
        else:
            results["category_counts"][cat] = len(val)

    if all_non_empty and len(missing_pattern_keys) == 0:
        results["categories_non_empty"] = True

    # 6. Check patterns.md
    if os.path.isfile(md_path):
        results["md_exists"] = True
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # Check for all IDs in Markdown
        all_ids = []
        for cat, items in patterns.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and "id" in item:
                        all_ids.append(item["id"])
        
        missing_ids = [item_id for item_id in all_ids if item_id not in md_content]
        if missing_ids:
            results["errors"].append(f"Missing pattern IDs in Markdown: {missing_ids}")
        else:
            results["md_all_ids_present"] = True
    else:
        results["errors"].append(f"Markdown file missing: {md_path}")

    return results

if __name__ == "__main__":
    res = run_empirical_validation()
    print("=== EMPIRICAL TEST RESULTS ===")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    
    if res["root_keys_present"] and res["patterns_keys_present"] and res["categories_non_empty"] and res["md_all_ids_present"]:
        print("\nVERDICT: APPROVE")
        sys.exit(0)
    else:
        print("\nVERDICT: REJECT")
        sys.exit(1)
