# WORK 101 — POLICY CORE STATIC REVIEW
Date: 2026-10-13 (+07)
State: SOURCE READ-BACK VERIFIED; TESTS NOT RUN

## Artifacts created
- `04_CODE/sync_policy.py` — pure offline policy primitives: path policy, SHA-256, snapshot validation, three-way change classification, exact approval binding and idempotency fingerprint.
- `05_TEST/test_sync_policy.py` — 10 unittest cases for path denial, secret/runtime/generated exclusions, source-only change, non-overlapping edits, same-path conflict, identical concurrent content, approval binding and idempotency replay.

## Read-back evidence
- MCP sandbox_read returned status=ok for both files.
- `sync_policy.py` read-back length: 6785 characters; `classify_sync` found.
- `test_sync_policy.py` read-back length: 3193 characters; 10 test methods found.
- These observations prove file persistence/read-back only. They do not prove Python syntax, importability, or test pass.

## Static review notes
- No network, GitHub, Core, filesystem write, shell, or credential operation is implemented in this module.
- Policy denies absolute/drive paths, traversal, non-canonical Unicode normalization, control/format characters, option-like components, Windows reserved names, alternate data streams, secret files, databases, logs, archives, generated output and evidence directories.
- Same-path concurrent edits with different digests become CONFLICT_PENDING; no last-write-wins behavior is implemented.
- Approval binding requires exact operation ID, diff digest, destination branch and base revision.
- Reusing an operation ID with a different payload is rejected by fingerprint mismatch.

## Known limits / required follow-up
- Tests were NOT RUN because this MCP Sandbox connector exposes file operations but no approved Python process runner.
- Pure path validation does not prove real filesystem containment, symlink/reparse-point safety, or race-free file access. Runtime adapter must enforce canonical realpath/root containment and reject symlinks/reparse points at the actual I/O boundary.
- Snapshot and sync functions are in-memory planning logic only. No GitHub/Sandbox transfer, revision discovery, retry persistence, conflict storage, or read-back digest verification is wired.
- Target repository URL, branch, root/path allowlist and credential/adapter authority remain unspecified/unverified; do not guess.
- Overall Work 101 remains ACTIVE / NOT VERIFIED. No PASS claimed.
