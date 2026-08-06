import sys
import os
import tempfile
import py_compile

# Ensure workspace root is in sys.path
workspace_root = r"c:\Users\ezequ\OneDrive\Área de Trabalho\FACELESS CHANNEL"
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

# 1. Test py_compile
target_file = os.path.join(workspace_root, "src", "connectors", "learning_engine.py")
print(f"Compiling {target_file}...")
try:
    py_compile.compile(target_file, doraise=True)
    print("py_compile PASSED (exit code 0 equivalent)")
except Exception as e:
    print(f"py_compile FAILED: {e}")
    sys.exit(1)

# 2. Instantiate ViralLearningEngine with temporary paths to avoid modifying real data
from src.connectors.learning_engine import ViralLearningEngine

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_db = os.path.join(tmpdir, "db.json")
    tmp_md = os.path.join(tmpdir, "patterns.md")
    
    engine = ViralLearningEngine(db_path=tmp_db, patterns_md_path=tmp_md)
    output = engine.format_patterns_for_prompt()
    
    print("\n--- OUTPUT OF format_patterns_for_prompt() ---")
    print(output)
    print("-----------------------------------------------\n")
    
    required_blocks = [
        "[RETENTION HOOKS]",
        "[DOMESTIC ANALOGIES]",
        "[MICRO-TWISTS]",
        "[SENSORY BEATS]",
        "[SOFT CTAS]",
        "[RETENTION TACTICS]"
    ]
    
    missing = []
    for block in required_blocks:
        if block not in output:
            missing.append(block)
            
    if missing:
        print(f"FAIL: The following required category titles/blocks were NOT found in output:\n  {missing}")
        sys.exit(1)
    else:
        print("SUCCESS: All 6 required category titles/blocks were found in output.")
