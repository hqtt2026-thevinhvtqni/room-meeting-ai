# Work 05 — Google Drive OAuth adapter sync status

**Date:** 2026-11-29  
**Status:** DRAFT SYNCED TO FEATURE BRANCH — NOT TESTED / NOT MERGED

## Scope
This branch mirrors the Work 05 Sandbox G1 OAuth-user Drive API v3 factory and its focused unit tests into the ROOM-HOP Git repository. It does not claim the complete Work 05 project has been mirrored.

## Files
- `10_TEST/MANUS_E2E_RUNS/W05_REAL_WORK_001/LOCAL_SOURCE_HANDOFF/src/work05_drive_factory.py`
- `10_TEST/MANUS_E2E_RUNS/W05_REAL_WORK_001/LOCAL_SOURCE_HANDOFF/tests/test_work05_drive_factory.py`

## Design constraints
- Uses OAuth user credentials, not a Google Service Account.
- Requires the least-privilege `https://www.googleapis.com/auth/drive.file` scope.
- Resolves credentials through `ConnectionManager.credential_for_operation(room_id, user_id, connection_id)` before adapter construction.
- Client secret is supplied by trusted runtime configuration; it must not be accepted from browser input or stored in public metadata.
- This factory does not implement the missing Core authorization authority; the caller must enforce authorization before supplying credentials.
- Work 33 remains the storage adapter owner. This Work 05 factory only constructs and injects the authenticated Google Drive API v3 service.

## Verification and limits
- Source was read back from the Work 05 Sandbox before mirroring.
- Four focused tests are present but **NOT RUN**.
- No live Google OAuth consent, Google API request, Core identity integration, deployment, or Windows Google Drive Desktop installation was performed.
- The Work 33 Core Authorizer integration remains a gate; its fail-closed behavior must not be bypassed.
- This is a feature branch only. Do not merge to `main` until source integration, tests, security review, and Work 33/Core authorization gates pass.

## Next gates
1. Integrate against the real Work 05 ConnectionManager interface and dependency layout.
2. Wire to Work 33's Google Drive adapter without bypassing Core authorization.
3. Run focused tests plus combined Work 05/33 regression tests.
4. Review OAuth redirect, secret storage, refresh/revoke behavior and exact granted scope.
5. Open/complete independent review before merge.
