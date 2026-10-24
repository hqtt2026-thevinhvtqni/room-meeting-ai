# 07_ENVIRONMENT — Work 102 candidate Python execution environment

**Status:** AUTHORIZED FOR CANDIDATE TESTING ONLY — authorization recorded in the engineering journal. This does not declare the candidate PASS or production-ready.

## 1. Scope and authority

- Final authority: Vinh. This runner is authorized only for Work 102 candidate testing on a separate read/write workspace copy.
- It does not modify canonical Sandbox source, create Core/dispatcher/Host, merge to `main`, or authorize release.
- Repair budget remains at most 2 repair rounds and 3 test runs per related defect cycle.

## 2. Prerequisites

- Windows with PowerShell 5.1+ or PowerShell 7.
- Python **3.12.14 exactly** and network access to install pinned `pytest==8.3.5`.
- A copy of the Work 102 candidate workspace whose root contains `04_CODE/`, `05_TEST/`, and `06_EVIDENCE/`. Do not run against the canonical Sandbox in place.
- The environment scripts and `expected_candidate_hashes.json` from this GitHub branch.

## 3. Setup

From a PowerShell terminal, point `$workspace` to the candidate workspace root and `$tools` to this branch's `07_ENVIRONMENT` directory:

```powershell
$workspace = 'C:\path\to\work102-candidate'
$tools = 'C:\path\to\repo\AI-AGENT-LOOP-PRODUCTION-READINESS\07_ENVIRONMENT'
pwsh -File "$tools\setup_env.ps1" -Workspace $workspace
```

The setup script refuses any base Python version other than 3.12.14 and does not overwrite an existing `.venv-work102`.

## 4. Hash-gated test run

```powershell
pwsh -File "$tools\run_full_suite.ps1" -Workspace $workspace
$LASTEXITCODE
```

Before executing pytest, the runner checks all seven candidate SHA-256 hashes against `expected_candidate_hashes.json`. Missing or mismatched files abort the run with exit code 2. A successful hash check is not itself a test result.

The runner executes `python -m pytest 05_TEST -v` with JUnit XML output and records:
- `HASH_CHECK.json`: expected and actual SHA-256 per file.
- `pytest_stdout.txt` and `pytest_stderr.txt`: separate raw process streams.
- `junit.xml`: test report when produced.
- `RUN_MANIFEST.json`: candidate ID, exact command, working directory, interpreter/package versions, per-file hashes, artifacts, and exit code.

Exit 0 means pytest exited successfully on the hash-matched candidate; exit 1 means tests ran and failed; exit 2 means hash/environment/pre-run failure. Preserve all evidence even for a failing test run.

## 5. After the run

Copy the complete `AUTHORIZED_RUN_<timestamp>` evidence directory back to Work 102 Sandbox through the approved workflow, read it back, and append a journal entry with the actual command, workspace, versions, seven hashes, test counts, exit code, and evidence paths. Ka must independently inspect the exact manifest and files before recording a review verdict.

A local test PASS does **not** close Gate A (Core authority, task dispatch/ACK, leases/fencing, persistence/recovery, or Work 14 Host binding). Keep the gates separate.

## 6. Candidate hash policy

The seven expected hashes are pinned in `expected_candidate_hashes.json` from the journal-recorded Patch V2 candidate. Update them only after a new candidate is formally recorded in the engineering journal; never update hashes just to make a drifted run pass.
