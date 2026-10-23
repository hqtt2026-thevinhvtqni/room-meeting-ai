"""pytest bootstrap: put 03_CODE on sys.path."""

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "03_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
