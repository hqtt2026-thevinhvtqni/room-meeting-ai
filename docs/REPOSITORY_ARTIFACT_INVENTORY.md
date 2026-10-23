# Repository Artifact Inventory — Initial Pass

Date: 2026-10-23 (UTC+07:00)
Status: INITIAL INVENTORY — no files deleted. Classifications below are provisional until owners/references are checked.

| Path / pattern | Initial classification | Action |
|---|---|---|
| `desktop.ini` | OS-generated candidate; tracked despite ignore rule | Confirm whether any project-specific reason exists, then remove from Git in a dedicated reviewed change |
| `agent_write_test.txt` | Likely write-probe artifact | Trace commit/history and confirm no test consumes it |
| `pytest_output.txt` | Generated test output candidate | Confirm no documentation or test fixture relies on it |
| `log.jsonl` | Runtime/audit log candidate | Preserve until provenance, owner, and retention requirements are established |
| `tmp/`, `trash/` | Temporary/archive candidates | Inventory contents recursively before any disposition |
| `agent_test/` | Unknown test/support directory | Inspect contents and references before moving/deleting |
| `30/` | Work-numbered directory, owner not established | Identify canonical Work and confirm naming policy; do not delete |
| `test google import genai.py` | Ad-hoc test script candidate | Inspect import/use and determine whether it belongs under tests/ |
| `test_secretary_*.py`, `test_closed_paste.py` | Test candidates | Preserve; establish whether collected by pytest and document intended test command |
| `*_v1_backup.py` (if present) | Backup/source-history candidate | Inspect references and commit history; prefer Git history only after recovery/reproducibility is verified |
| `docs/NewFolder/NewFile.txt`, `hello.txt` (if present) | Placeholder candidates from reported review | Verify exact branch/path before any change |

## Rules

- Do not delete by filename alone.
- Record the path, last meaningful commit, references, owner/Work, disposition, and verification evidence for each change.
- Remove generated/runtime artifacts only in a dedicated cleanup PR, after confirming they are not required evidence or fixtures.
- The existing `.gitignore` on `main` already lists `desktop.ini`; the remaining issue is that an already tracked file is not automatically untracked by adding an ignore rule.
