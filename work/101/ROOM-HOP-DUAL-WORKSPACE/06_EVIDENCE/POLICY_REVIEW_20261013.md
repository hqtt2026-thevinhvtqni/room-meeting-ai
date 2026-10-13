# Work 101 — Policy Review

Date: 2026-10-13
Review type: static source review plus observed GitHub Actions unit-test execution.

## Issues found and corrected
1. The evidence-tree denylist was too broad; ordinary evidence documents are now allowed while generated logs/runtime artifacts remain excluded.
2. Path validation rejects non-canonical relative paths, traversal, absolute/drive paths, ADS, Windows reserved names and case-insensitive collisions within snapshots.
3. Source/destination snapshots must explicitly identify the selected common base revision when constructing a plan; mismatches fail closed.
4. The deterministic DRY_RUN planner binds policy version, operation/work IDs, destination branch, base/source/destination revisions, allowlist, per-path content digests, directions and conflict paths into the diff digest.
5. `main` and `master` are rejected as destination branches; conflicts, stale baselines and deletion-pending plans emit no transfer paths.
6. Any baseline-file deletion on either side, including matching deletion on both sides, enters `DELETION_PENDING` and requires review.
7. The PowerShell runner was repaired after static inspection found a malformed origin guard and duplicated trailing script content. Windows-invalid path characters, OS metadata, temporary/backup files and private-key material are also excluded and covered by tests.

## Test evidence
- GitHub Actions run [38341525183](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/38341347877) completed SUCCESS.
- CPython 3.12.15 ran 23 tests; job log confirms `Ran 23 tests` and `OK`.
- This verifies the pure policy unit suite only; it does not establish adapter or runtime correctness.

## Residual risks / blockers
- Runtime adapter is not implemented. Realpath/symlink containment, atomic writes, target revision semantics, Core authorization, durable audit ledger and restart/recovery remain unverified.
- No PowerShell execution on the Windows PC, Sandbox/GitHub round-trip, browser runtime, live Dashboard source, or ROOM-HOP E2E has been performed.
- Work 24/27/28 live contracts must be verified and Work 14 lifecycle records reconciled before integration design.
- CI logs contain a non-fatal checkout cleanup warning caused by `.gitmodules` lacking a URL for `room-meeting-ai`, and a Node.js 20 deprecation warning; these are tracked separately from the passing unit suite.
- No merge, release or live write is authorized. Keep sync `DRY_RUN`.
