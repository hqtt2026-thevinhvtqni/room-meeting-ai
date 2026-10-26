# Work 33 — ROOM Shared File & Evidence Hub (RSFEH)

Self-contained file + evidence store for ROOM-HOP.

## Quick start (clean environment)

```bash
export PYTHONPATH=04_CODE/src
export RSFEH_ROOT=./rsfeh_data   # optional

python -m rsfeh init
python -m rsfeh put /path/to/file.bin --agent xu --work-id 33 --notes "evidence"
python -m rsfeh list --work-id 33
python -m rsfeh get <file_id> --out /tmp/out.bin
python -m rsfeh verify <file_id>
python -m rsfeh search evidence
python -m rsfeh audit
```

Requires Python 3.10+ (stdlib only: sqlite3, hashlib, argparse, pathlib).

## Acceptance status (local)

| ID | Result | Evidence |
|----|--------|----------|
| A1–A9 | PASS | `06_EVIDENCE/test-results/pytest_full.log` — 17 passed |
| A10 | BLOCKED | No live Core/MCP write contract + credentials in this session |
| A11 | PASS | This tree + BUILD_REPORT / HANDOFF |

## Structure

See `03_ARCHITECTURE/` and product tree under this WORK_33_ROOM.
