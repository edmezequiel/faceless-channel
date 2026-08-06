# -*- coding: utf-8 -*-
import os
import json
import re
import sys

JSON_PATH = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\memory\viral_knowledge_bank\knowledge_base.json"
MD_PATH = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL\memory\viral_knowledge_bank\patterns.md"

def run_audit():
    print("=== STARTING FORENSIC INTEGRITY AUDIT FOR MILESTONE 1 ===")
    violations = []
    
    # Check 1: File Existence
    if not os.path.exists(JSON_PATH):
        violations.append(f"File missing: {JSON_PATH}")
    if not os.path.exists(MD_PATH):
        violations.append(f"File missing: {MD_PATH}")
        
    if violations:
        return False, violations
        
    # Check 2: JSON Validity & Schema
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            kb_data = json.load(f)
    except Exception as e:
        violations.append(f"JSON syntax error in knowledge_base.json: {e}")
        return False, violations

    required_top_keys = ["version", "last_updated", "analyzed_videos_count", "patterns"]
    for k in required_top_keys:
        if k not in kb_data:
            violations.append(f"Missing top-level JSON key: '{k}'")
            
    patterns = kb_data.get("patterns", {})
    required_categories = ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]
    
    for cat in required_categories:
        if cat not in patterns:
            violations.append(f"Missing required pattern category: '{cat}'")
        elif not isinstance(patterns[cat], list):
            violations.append(f"Category '{cat}' is not a list.")
        elif len(patterns[cat]) == 0:
            violations.append(f"Category '{cat}' is empty (no items).")

    # Check 3: Search for Dummy / Facade Data / Placeholders
    prohibited_words = ["lorem", "ipsum", "dummy", "placeholder", "foo", "bar", "test_item", "sample", "todo", "xxx"]
    kb_str = json.dumps(kb_data).lower()
    for pw in prohibited_words:
        if pw in kb_str:
            violations.append(f"Prohibited/dummy keyword found in JSON: '{pw}'")

    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()
    md_str_lower = md_content.lower()
    for pw in prohibited_words:
        if pw in md_str_lower:
            violations.append(f"Prohibited/dummy keyword found in Markdown: '{pw}'")

    # Check 4: Check Genuine Seed Data Content
    total_json_items = 0
    all_json_ids = set()
    category_counts = {}
    sources = set()
    
    for cat, items in patterns.items():
        category_counts[cat] = len(items)
        total_json_items += len(items)
        for idx, item in enumerate(items):
            item_id = item.get("id")
            if not item_id:
                violations.append(f"Item #{idx} in category '{cat}' missing 'id'")
            else:
                all_json_ids.add(item_id)
            
            src = item.get("example_source", "")
            if src:
                sources.add(src)
            
            # Check fields are populated genuinely
            for k, v in item.items():
                if isinstance(v, str) and len(v.strip()) < 3:
                    violations.append(f"Item '{item_id}' has suspicious short field '{k}': '{v}'")

    print(f"Total JSON Pattern Items: {total_json_items}")
    print(f"Categories Present: {category_counts}")
    print(f"Sources Found: {sources}")

    # Check 5: Cross-Verification JSON vs Markdown
    md_ids = set(re.findall(r'`(HOOK_\d+|ANA_\d+|TWIST_\d+|SENS_\d+|CTA_\d+|TAC_\d+)`', md_content))
    print(f"IDs found in patterns.md: {len(md_ids)}")
    
    missing_in_md = all_json_ids - md_ids
    missing_in_json = md_ids - all_json_ids
    
    if missing_in_md:
        violations.append(f"IDs in JSON but missing in patterns.md: {missing_in_md}")
    if missing_in_json:
        violations.append(f"IDs in patterns.md but missing in JSON: {missing_in_json}")

    # Check 6: Real YouTube Case Studies Verification
    voyager_items = [i for cat in patterns.values() for i in cat if "Voyager" in i.get("example_source", "")]
    pluto_items = [i for cat in patterns.values() for i in cat if "Pluto" in i.get("example_source", "") or "James Webb" in i.get("example_source", "")]
    
    print(f"Voyager 1 case study items: {len(voyager_items)}")
    print(f"Pluto / James Webb case study items: {len(pluto_items)}")
    
    if len(voyager_items) == 0:
        violations.append("No seed data items found for Voyager 1 case study.")
    if len(pluto_items) == 0:
        violations.append("No seed data items found for Pluto / James Webb case study.")

    return len(violations) == 0, violations

if __name__ == "__main__":
    success, violations = run_audit()
    if success:
        print("\nFORENSIC VERDICT: CLEAN")
    else:
        print("\nFORENSIC VERDICT: INTEGRITY VIOLATION")
        print("Violations:")
        for v in violations:
            print(f" - {v}")
    sys.exit(0 if success else 1)
