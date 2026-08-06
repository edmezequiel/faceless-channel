import json
import os
import sys

def deep_schema_stress_test():
    workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
    json_path = os.path.join(workspace_root, "memory", "viral_knowledge_bank", "knowledge_base.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    
    # Root check
    if not isinstance(data.get("version"), str) or not data.get("version"):
        errors.append("Invalid 'version'")
    if not isinstance(data.get("last_updated"), str) or not data.get("last_updated"):
        errors.append("Invalid 'last_updated'")
    if not isinstance(data.get("analyzed_videos_count"), int) or data.get("analyzed_videos_count") <= 0:
        errors.append("Invalid 'analyzed_videos_count'")
        
    patterns = data.get("patterns", {})
    categories = ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]
    
    for cat in categories:
        items = patterns.get(cat, [])
        if not items:
            errors.append(f"Empty category: {cat}")
            continue
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{cat}[{idx}] is not a dict")
                continue
            if "id" not in item or not item["id"]:
                errors.append(f"{cat}[{idx}] missing 'id'")
            if "adapted_for_channel" not in item or not item["adapted_for_channel"]:
                errors.append(f"{cat}[{idx}] missing 'adapted_for_channel'")
            if "example_source" not in item or not item["example_source"]:
                errors.append(f"{cat}[{idx}] missing 'example_source'")

    print(f"Deep Schema Check Errors Count: {len(errors)}")
    if errors:
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("Deep Schema Check PASSED with 0 errors!")
        sys.exit(0)

if __name__ == "__main__":
    deep_schema_stress_test()
