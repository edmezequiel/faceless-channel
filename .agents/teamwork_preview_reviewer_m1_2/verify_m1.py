import json
import re

def verify():
    kb_path = 'memory/viral_knowledge_bank/knowledge_base.json'
    md_path = 'memory/viral_knowledge_bank/patterns.md'
    
    with open(kb_path, encoding='utf-8') as f:
        kb = json.load(f)

    print("=== TOP LEVEL SCHEMA CHECK ===")
    required_top_keys = {"version", "last_updated", "analyzed_videos_count", "patterns"}
    actual_top_keys = set(kb.keys())
    print("Top keys match exact required set:", actual_top_keys == required_top_keys)
    print("Top keys:", list(kb.keys()))
    
    print("\n=== PATTERNS CATEGORIES CHECK ===")
    required_categories = {"hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"}
    actual_categories = set(kb["patterns"].keys())
    print("Categories match exact required 6:", actual_categories == required_categories)
    
    cat_counts = {cat: len(kb["patterns"][cat]) for cat in required_categories}
    print("Category counts:", cat_counts)
    
    print("\n=== CASE STUDY SOURCE COVERAGE ===")
    voyager_count = 0
    pluto_count = 0
    
    for cat, items in kb["patterns"].items():
        print(f"\nCategory [{cat}]: {len(items)} items")
        for item in items:
            item_id = item.get("id")
            source = item.get("example_source", "")
            if "Voyager" in source:
                voyager_count += 1
            if "Pluto" in source or "James Webb" in source:
                pluto_count += 1
            print(f"  - {item_id}: source='{source}', fields={list(item.keys())}")
            
    print(f"\nTotal Voyager 1 entries: {voyager_count}")
    print(f"Total Pluto/JWST entries: {pluto_count}")
    
    print("\n=== MARKDOWN CONSISTENCY CHECK ===")
    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()
        
    all_json_ids = []
    missing_ids_in_md = []
    for cat, items in kb["patterns"].items():
        for item in items:
            item_id = item.get("id")
            all_json_ids.append(item_id)
            if item_id not in md_text:
                missing_ids_in_md.append(item_id)
                
    print("All JSON IDs found in patterns.md:", len(missing_ids_in_md) == 0)
    if missing_ids_in_md:
        print("Missing IDs in MD:", missing_ids_in_md)
    else:
        print("Verified all IDs present in patterns.md:", all_json_ids)
        
    print("\n=== CHECKING DETAILED FIELD INTEGRITY ===")
    # Check field consistency in hooks
    for item in kb["patterns"]["hooks"]:
        assert {"id", "type", "pattern", "example_source", "template", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in hook {item['id']}"
    # Check field consistency in analogies
    for item in kb["patterns"]["analogies"]:
        assert {"id", "concept", "domestic_comparison", "example_source", "example", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in analogy {item['id']}"
    # Check field consistency in micro_twists
    for item in kb["patterns"]["micro_twists"]:
        assert {"id", "trigger", "example_source", "phrase", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in micro_twist {item['id']}"
    # Check field consistency in sensory_beats
    for item in kb["patterns"]["sensory_beats"]:
        assert {"id", "type", "example_source", "template", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in sensory_beat {item['id']}"
    # Check field consistency in ctas
    for item in kb["patterns"]["ctas"]:
        assert {"id", "type", "example_source", "template", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in cta {item['id']}"
    # Check field consistency in retention_tactics
    for item in kb["patterns"]["retention_tactics"]:
        assert {"id", "tactic", "mechanism", "pacing_interval", "example_source", "template", "adapted_for_channel"}.issubset(item.keys()), f"Missing fields in retention_tactic {item['id']}"
        
    print("All item field checks PASSED successfully.")

if __name__ == "__main__":
    verify()
