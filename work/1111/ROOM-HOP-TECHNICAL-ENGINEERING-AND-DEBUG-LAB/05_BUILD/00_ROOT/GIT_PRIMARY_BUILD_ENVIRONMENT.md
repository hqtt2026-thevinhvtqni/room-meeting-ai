# Work 1111 — Git-primary build environment

**Status:** ACTIVE / adopted for Work 1111  
**Work ID:** 1111  
**Active branch:** `work/w1111-core-execution-authority-v1-2`  
**PR:** #48 (draft; do not merge without explicit approval)

## 1. Source of truth

- GitHub repository `hqtt2026-thevinhvtqni/room-meeting-ai` is the primary versioned build and test environment for Work 1111.
- While PR #48 remains open, the active source-of-truth ref is `work/w1111-core-execution-authority-v1-2`, not `main`.
- `main` remains unchanged by this work until review and explicit merge authorization.
- The canonical Work record path is `work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/`.
- ROOM-HOP Sandbox Work 1111 is the collaboration mirror. It is updated from a verified Git ref; it is not an independent competing source of truth.

## 2. Build/test environment

- CI runner: GitHub Actions, Ubuntu, Python 3.12.
- Install: `python -m pip install -r requirements.txt fastapi httpx`.
- Workflow: `.github/workflows/core-execution-authority.yml`.
- Core test command:
  `python -m pytest -q tests/test_execution_authority.py tests/test_execution_host_authority.py tests/test_core_http_main.py`
- W12 canonical host tests run from `12/WORK-EXECUTION-ENVIRONMENT/04_CODE` against `../05_TEST/test_real_execution_host.py`.
- W13 bridge/integration tests run from `13/EXECUTION-HOST-INFRASTRUCTURE/04_CODE` against `../05_TEST/test_wee_8031_bridge.py`, `test_core_grant_host_integration.py`, and `test_core_wee_w13_w12_e2e.py`.

## 3. Required change cycle

1. Read the active branch and confirm its HEAD before editing.
2. Make scoped changes on the active Work branch; never edit `main` directly.
3. Commit each coherent change with a descriptive message.
4. Wait for GitHub Actions to finish on the exact final HEAD SHA.
5. Inspect job steps and logs. A green run on an earlier SHA does not validate a later SHA.
6. Record the run URL, commit SHA, test groups, counts, failures, and limitations in the Work journal.
7. Only after exact-HEAD CI is verified, synchronize the corresponding Work files to ROOM-HOP Sandbox.
8. Read back Sandbox files and compare content/hash where available. A successful write without readback is not a verified sync.

## 4. Evidence and acceptance boundaries

- CI PASS means only the test groups actually executed on the recorded commit passed.
- CI does not prove the user's PC runtime, cloud runtime, live network, credentials, process lifecycle, or deployment are correct.
- Live E2E requires separate positive/negative runtime probes and independently verifiable artifacts.
- Sandbox sync, GitHub commit, CI, and live runtime are four separate evidence layers.
- Never label the whole Work E2E PASS based only on pytest or documentation synchronization.

## 5. Sandbox mirror policy

- Direction for code/build truth: Git branch -> Sandbox.
- New changes originate in Git. Sandbox-only edits must be reconciled into Git before being treated as canonical.
- Sync only Work 1111 paths; do not overwrite adjacent Works or runtime configuration.
- Preserve Sandbox readback evidence and report missing/unreadable files as BLOCKED, not PASS.

## 6. Initial adoption evidence

- Initial active branch: `work/w1111-core-execution-authority-v1-2`.
- PR #48 remains OPEN/DRAFT/UNMERGED.
- Exact-head GitHub Actions run `43072888315` on commit `a6efdeb2a8e517d949905ea8896279c49a50bb7a` completed successfully after the nested-test blocker fix. The run covered Core authority, W12 canonical host, and W13 bridge/integration tests.
- Subsequent commits require a new exact-HEAD CI result; this initial result must not be reused as proof for later commits.
