# KA TO NU — CONSOLIDATED FOLLOW-UP AFTER KAST-01..04 STATIC REVIEW
Date: 2026-10-15
Authority: Ka coordinates; Nu owns implementation. This file is durable Work guidance, not proof of inbox dispatch or acknowledgement.

## Review outcome
The updated files were read back. Source versions: contract 0.1.1, collector 0.3.0, verifier 0.2.0. No tests executed.

## Required in the next single coherent package
1. KAST-04 incremental metadata bounds: in enumerate_files(), bound excluded item count and each item length as they are appended; fail closed immediately rather than accumulating the whole list and checking afterward. Ensure the policy also bounds path/status collection work where feasible.
2. KAST-02 ZIP external attributes: document accepted ZIP create_system and attribute combinations; add regression cases for Unix symlink, FIFO/device/socket/special modes, mode=0/ambiguous type, DOS attributes/reparse-like flags, directory attribute/name inconsistency, and normal DOS/Unix regular files. Reject ambiguous or non-regular members unless compatibility requirements justify an explicit safe exception.
3. KAST-03 cap drift: import and use HARD_MAX_MANIFEST_BYTES from source_snapshot_contract.py in the collector rather than duplicating 2 * 1024 * 1024. Add a test or static contract assertion that collector and verifier share the same constant.
4. KAST-04 cleanup: add failure-injection test plan for archive write failure, manifest oversize, manifest write failure, and cleanup failure. Do not run collector on PC; test only in an approved isolated runner.
5. Refresh report's leading summary/version matrix so the current versions are clear at first read. Keep historical version statements only under a clearly labelled superseded-history section; do not delete audit history.

## Required evidence per item
- exact source/test paths and changed functions;
- readback result;
- tests mapped to finding IDs;
- runner ID/revision, command, stdout/stderr, exit code, counts, artifact hash if available; otherwise explicit NOT RUN;
- residual risks and gate state.

## Hard boundaries
- No PC access, collector execution, source transfer/import, live service change, or release.
- No fabricated test results or hashes.
- Do not represent receipt shape validation as authentication. F3 remains BLOCKED until a trusted issuer/verifier and replay protection exist.
- F1 remains BLOCKED until Windows-specific race safety is implemented and evidenced.

## Current disposition
KAST-01: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.
KAST-02: IMPLEMENTED PARTIALLY / NOT EXECUTED.
KAST-03: STATIC REVIEW POSITIVE / NOT EXECUTED; remove duplicated cap.
KAST-04: IMPLEMENTED PARTIALLY / NOT EXECUTED; incremental bounds required.
F1 BLOCKED; F3 BLOCKED; approved runner BLOCKED; source transfer/import BLOCKED; E2E BLOCKED; release NO-GO.
