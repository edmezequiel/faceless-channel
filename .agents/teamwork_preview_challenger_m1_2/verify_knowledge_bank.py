import json
import os
import re
import sys

def run_tests():
    base_dir = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
    json_path = os.path.join(base_dir, "memory", "viral_knowledge_bank", "knowledge_base.json")
    md_path = os.path.join(base_dir, "memory", "viral_knowledge_bank", "patterns.md")
    
    results = []
    failed = False
    
    def log(test_name, success, detail=""):
        nonlocal failed
        status = "PASS" if success else "FAIL"
        if not success:
            failed = True
        results.append(f"[{status}] {test_name}: {detail}")
        print(f"[{status}] {test_name}: {detail}")

    # 1. Encoding check (UTF-8 strict)
    try:
        with open(json_path, "r", encoding="utf-8", errors="strict") as f:
            json_text = f.read()
        log("UTF-8 strict read: knowledge_base.json", True, f"Length: {len(json_text)} chars")
    except Exception as e:
        log("UTF-8 strict read: knowledge_base.json", False, str(e))
        return results, False

    try:
        with open(md_path, "r", encoding="utf-8", errors="strict") as f:
            md_text = f.read()
        log("UTF-8 strict read: patterns.md", True, f"Length: {len(md_text)} chars")
    except Exception as e:
        log("UTF-8 strict read: patterns.md", False, str(e))
        return results, False

    # Check for byte order mark (BOM) or corrupted mojibake
    mojibake_patterns = [r"Ã©", r"Ã¡", r"Ã£", r"Ã§", r"â€™", r"Ã³", r"Ãº"]
    found_mojibake_json = [p for p in mojibake_patterns if re.search(p, json_text)]
    found_mojibake_md = [p for p in mojibake_patterns if re.search(p, md_text)]
    
    log("Mojibake check: knowledge_base.json", len(found_mojibake_json) == 0, f"Found: {found_mojibake_json}")
    log("Mojibake check: patterns.md", len(found_mojibake_md) == 0, f"Found: {found_mojibake_md}")

    # 2. JSON Syntax & Quote Escaping
    try:
        data = json.loads(json_text)
        log("JSON syntax parsing: knowledge_base.json", True, "Successfully parsed valid JSON")
    except json.JSONDecodeError as e:
        log("JSON syntax parsing: knowledge_base.json", False, f"JSONDecodeError at line {e.lineno}, col {e.colno}: {e.msg}")
        return results, False

    # 3. Schema & Category completeness for knowledge_base.json
    expected_categories = [
        "hooks",
        "analogies",
        "micro_twists",
        "sensory_beats",
        "ctas",
        "retention_tactics"
    ]
    
    top_keys = list(data.keys())
    log("Top-level keys check", set(top_keys) >= {"version", "last_updated", "analyzed_videos_count", "patterns"}, f"Keys: {top_keys}")
    
    patterns = data.get("patterns", {})
    categories_found = list(patterns.keys())
    missing_cats = [cat for cat in expected_categories if cat not in categories_found]
    log("6 Categories presence check", len(missing_cats) == 0, f"Found {len(categories_found)}/6 categories. Missing: {missing_cats}")

    # Check all entry IDs uniqueness
    all_ids = []
    id_counts = {}
    cat_counts = {}

    for cat in expected_categories:
        items = patterns.get(cat, [])
        cat_counts[cat] = len(items)
        if len(items) == 0:
            log(f"Category '{cat}' populated in JSON", False, "Empty list of items")
            continue
        
        log(f"Category '{cat}' populated in JSON", True, f"Contains {len(items)} items")

        for idx, item in enumerate(items):
            item_id = item.get("id", f"UNKNOWN_{idx}")
            all_ids.append(item_id)
            id_counts[item_id] = id_counts.get(item_id, 0) + 1
            
            orig_example = item.get("template") or item.get("example") or item.get("phrase")
            adapted = item.get("adapted_for_channel")
            source = item.get("example_source")

            has_orig = isinstance(orig_example, str) and len(orig_example.strip()) > 0
            has_adapted = isinstance(adapted, str) and len(adapted.strip()) > 0
            has_source = isinstance(source, str) and len(source.strip()) > 0

            log(f"Item {item_id} in {cat} - original example", has_orig, f"Val: {orig_example[:40]}..." if has_orig else "Missing/Empty")
            log(f"Item {item_id} in {cat} - adapted_for_channel", has_adapted, f"Val: {adapted[:40]}..." if has_adapted else "Missing/Empty")
            log(f"Item {item_id} in {cat} - example_source", has_source, f"Val: {source}" if has_source else "Missing/Empty")

    duplicate_ids = [k for k, v in id_counts.items() if v > 1]
    log("Unique Entry IDs check", len(duplicate_ids) == 0, f"Duplicates: {duplicate_ids}")

    # 4. Markdown layout & Table completeness in patterns.md
    md_headers = re.findall(r"^##\s+.*", md_text, flags=re.MULTILINE)
    log("Markdown section headers count", len(md_headers) >= 6, f"Found {len(md_headers)} headers")

    # Split markdown by sections (## )
    sections = re.split(r"\n(?=##\s+)", md_text)
    
    for cat in expected_categories:
        matching_section = None
        for sec in sections:
            if f"`{cat}`" in sec or cat in sec:
                matching_section = sec
                break
        
        if not matching_section:
            log(f"Markdown section for `{cat}`", False, "Section missing")
            continue
            
        log(f"Markdown section for `{cat}`", True, "Section header found")
        
        # Extract table rows
        lines = matching_section.strip().split("\n")
        table_lines = [l.strip() for l in lines if l.strip().startswith("|")]
        data_rows = []
        for line in table_lines:
            # Skip header row and delimiter row
            if "Fonte / Referência" in line or "Conceito" in line or "Gatilho" in line or "ID" in line:
                continue
            if re.match(r"^\|[\s\-:\t|]+\|$", line):
                continue
            data_rows.append(line)

        log(f"Markdown table rows for `{cat}`", len(data_rows) == cat_counts.get(cat, 0), f"MD rows: {len(data_rows)}, JSON items: {cat_counts.get(cat, 0)}")

        # Verify that each data row has both original template/example and adapted_for_channel content
        for idx, row in enumerate(data_rows):
            columns = [c.strip() for c in row.split("|")[1:-1]]
            log(f"Markdown table row {idx+1} for `{cat}` column count", len(columns) >= 5, f"Columns found: {len(columns)}")
            
            # Last column is adapted example, second to last is original example/phrase/template
            if len(columns) >= 5:
                orig_col = columns[-2]
                adapted_col = columns[-1]
                log(f"Markdown row {idx+1} for `{cat}` - original content", len(orig_col) > 0 and orig_col != "-", f"Val: {orig_col[:30]}...")
                log(f"Markdown row {idx+1} for `{cat}` - adapted content", len(adapted_col) > 0 and adapted_col != "-", f"Val: {adapted_col[:30]}...")

    # 5. Stress test quote escaping in Markdown table pipes
    # If a quote or pipe inside table cell is unescaped, it breaks table parsing.
    pipe_in_cells_broken = False
    for line in md_text.split("\n"):
        if line.strip().startswith("|") and not re.match(r"^\|[\s\-:\t|]+\|$", line.strip()):
            # Count columns
            cols = line.strip().split("|")
            # If line starts and ends with |, cols should have len >= 3
            if len(cols) < 3:
                pipe_in_cells_broken = True
    log("Markdown table pipe escaping integrity", not pipe_in_cells_broken, "No broken table row formatting found")

    # 6. Roundtrip serialization stress test
    try:
        reserialized = json.dumps(data, indent=2, ensure_ascii=False)
        reloaded = json.loads(reserialized)
        log("JSON roundtrip re-serialization", reloaded == data, "Data identical after re-serialization")
    except Exception as e:
        log("JSON roundtrip re-serialization", False, str(e))

    return results, not failed

if __name__ == "__main__":
    results, success = run_tests()
    print("\n================ SUMMARY ================")
    print(f"Overall status: {'PASS' if success else 'FAIL'}")
    print(f"Total assertions: {len(results)}")
    print(f"Passed assertions: {sum(1 for r in results if r.startswith('[PASS]'))}")
    print(f"Failed assertions: {sum(1 for r in results if r.startswith('[FAIL]'))}")
