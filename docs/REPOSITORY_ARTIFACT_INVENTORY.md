# Repository Artifact Inventory — Verified First Pass

Date: 2026-10-23 (UTC+07:00)
Status: PARTIAL — three confirmed machine/generated artifacts removed from this PR branch only. `main` is untouched. Remaining candidates are deliberately retained pending provenance review.

| Path / pattern | Evidence / classification | Disposition |
|---|---|---|
| `desktop.ini` | Read content: Windows Explorer metadata referencing a local Google Drive File Stream install. Existing `.gitignore` rule was not enough because the file was already tracked. | **Removed from this PR branch** in commit `7d9126a`; not deleted from `main`. |
| `pytest_output.txt` | Read content: saved pytest console output from a local Windows checkout/path; not a test fixture. Repository search found an old cleanup script referencing it for untracking, not runtime use. | **Removed from this PR branch** in commit `0759fc4`. |
| `agent_write_test.txt` | Content is a single write-probe token; repository code search found no consumer. | **Removed from this PR branch** in commit `04b4507`. |
| `log.jsonl` | Runtime/audit log. `build_prompt.py` appends to this path and meeting code also uses `log.jsonl` for persisted meeting records. | **Preserved**; do not treat this name as disposable. Separate root log from per-meeting logs before changing retention. |
| `tmp/`, `trash/` | Temporary/archive candidates; contents and owners not yet audited recursively. | Preserve until per-file inventory and recovery path exist. |
| `agent_test/` | Unknown test/support directory. | Preserve; inspect contents and references before disposition. |
| `30/` | Work-numbered directory with Work 30 mirror/build records and operating instructions. | Preserve as Work data; do not remove as clutter. |
| `test google import genai.py` | Ad-hoc test script candidate. | Not yet dispositioned; inspect imports, execution side effects, and references. |
| `test_secretary_*.py`, `test_closed_paste.py` | Test candidates. | Preserve; verify collection and owning Work before moving. |
| `*_v1_backup.py` (if present) | Potential backup/source history. | Preserve until Git history and reproducibility are checked. |
| `docs/NewFolder/NewFile.txt`, `hello.txt` | Reported placeholder candidates. | Exact paths not found on the maintenance branch; no deletion made. |
| Invalid gitlink/submodule path `room-meeting-ai` | CI checkout cleanup logs `No url found for submodule path 'room-meeting-ai' in .gitmodules`. | **BLOCKED** pending inspection of tracked tree/history; no gitlink removal attempted. |

## Rules

- Do not delete by filename alone.
- Record path, meaningful commit/history, references, owner/Work, disposition, and verification evidence for each change.
- All deletions above are branch-local and reviewable in PR #22; they are not on `main`.
- Keep CI failures visible. Do not remove or skip failing tests to obtain a green check.
