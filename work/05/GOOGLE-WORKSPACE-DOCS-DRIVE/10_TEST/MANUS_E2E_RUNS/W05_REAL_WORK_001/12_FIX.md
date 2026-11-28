# W05 REAL WORK 001 — FIX / RECOVERY

STATUS: PASS — 2 failures preserved and recovered; no failure hidden.
OWNER / AGENT: Recovery role
TIMESTAMP: 2026-10-05T02:30:46+07:00
INPUT: Initial test execution.
ACTION: Follow FAIL → CLASSIFY → PRESERVE → DIAGNOSE → MINIMAL FIX → RETEST.
FAILURE W05-F-001: ENVIRONMENT. Symptom: `pytest: command not found`. Expected test runner; actual command unavailable. Repair: install pytest only. Retest exposed the next logic result.
FAILURE W05-F-002: LOGIC. Symptom: section update produced `A\n[SECTION]newold`. Root cause: no terminator semantics in the mock section model. Repair: minimal end-of-document replacement for this vertical slice. Retest: `6 passed in 0.01s`.
EVIDENCE: evidence/W05-F-001.md, evidence/W05-F-002.md, pytest_retest.txt, pytest_final.txt.
NEXT: Preserve both historical failures in final report; do not rewrite them as if they never occurred.
