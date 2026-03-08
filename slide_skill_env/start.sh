#!/bin/sh
# Startup script with diagnostic logging.
# Runs a quick import test before handing off to uvicorn, so any Python
# import errors are visible in the HF Spaces container logs.

set -e

echo "=== Slide Forge startup ==="
echo "Python: $(python --version)"
echo "Node:   $(node --version)"
echo "Working dir: $(pwd)"

echo "Testing imports..."
python -c "
import sys, os
print('sys.path:', sys.path[:4])
try:
    from slide_skill_env.app import app
    print('Import OK')
except Exception as e:
    import traceback
    print('IMPORT FAILED:', e)
    traceback.print_exc()
    sys.exit(1)
"

echo "Starting uvicorn on port 7860..."
exec uvicorn slide_skill_env.app:app --host 0.0.0.0 --port 7860 --workers 1
