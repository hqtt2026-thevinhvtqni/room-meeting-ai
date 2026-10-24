# 07_ENVIRONMENT — Authorized Python Execution Environment — Work 102

**Status:** PROPOSED — becomes ACTIVE only after Vinh (Final Authority) authorizes this environment as the Work 102 execution host.  
**Purpose:** Resolve the ENV_BLOCKED test gate by providing a reproducible, evidence-producing Python environment bound to the exact seven-file candidate hashes recorded in [STATUS_SNAPSHOT_20261024.md](../06_EVIDENCE/STATUS_SNAPSHOT_20261024.md).

## 1. Authorization rule

- The engineering journal requires an "authorized execution host". This environment is a candidate until Vinh records authorization (a single journal line naming this setup, the machine class, and the date is sufficient).
- The environment is a test runner only. It does NOT modify Sandbox source, does not create Core/dispatcher/Host, does not merge/release. Repair budget remains max 2 repair rounds / 3 test runs per cycle.

## 2. Prerequisites

- Windows PC with PowerShell 5.1+ (or pwsh), Python **3.12.14** (exact version used for the reference bundle), internet access for one pip install.
- A read/write copy of the Work 102 Sandbox workspace (folder containing 04_CODE/ and 05_TEST/). Copy it out of the Sandbox first; do not run against the canonical Sandbox in place unless Vinh explicitly authorizes that.

## 3. Setup (one time)

```powershell
cd <workspace-copy>
pwsh -File AI-AGENT-LOOP-PRODUCTION-READINESS/07_ENVIRONMENT/setup_env.ps1
```

Creates `.venv-work102` with pinned pytest 8.3.5 and records versions.

## 4. Evidence run

```powershell
pwsh -File AI-AGENT-LOOP-PRODUCTION-READINESS/07_ENVIRONMENT/run_full_suite.ps1 -Workspace <workspace-copy>
```

The script, in order:
1. Computes SHA-256 of the 7 candidate files and reports MATCH / DRIFT / NOT_VERIFIED against the pinned expected hashes (drift ⇒ abort with exit 2; do not test drifted source).
2. Runs pytest collection + full suite + deterministic demo where available, emitting JUnit XML.
3. Preserves raw stdout/stderr, exit codes, interpreter + package versions, per-file hashes.
4. Writes `06_EVIDENCE/AUTHORIZED_RUN_<timestamp>/RUN_MANIFEST.json` ready to be copied back into Sandbox evidence and appended to the journal.

Exit 0 = suite passed on hash-matched source; Exit 1 = tests ran and failed (evidence still valid); Exit 2 = hash drift or environment failure (not a valid run).

## 5. After a run

- Append the run result to the journal as an evidence entry (command, cwd, versions, hashes, counts, exit code).
- Ka reviews the same RUN_MANIFEST and hashes; record Ka verdict only after actual read-back.
- A passing local run still does NOT close Gate A (Core authority, dispatch/ACK, leases/fencing, W14 Host binding). Keep gates separate.

## 6. Scope

- No new dispatcher/queue/Core/Host. No canonical main source changes. This folder is runner tooling + documentation only.
- Expected hashes live in `expected_candidate_hashes.json` here; update it ONLY with a journal-recorded candidate change (new RUN_BUNDLE from Co), never ad hoc.
