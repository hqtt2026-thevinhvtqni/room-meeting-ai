# KA INDEPENDENT STATIC REVIEW — KAST-01..04 PACKAGE
Date: 2026-10-15
Work: 28 / MCP-8020-TOOLING-PLATFORM
Review type: independent static readback only; no Python execution, no collector execution, no PC access.

## Files read back
- 04_CODE/source_snapshot_contract.py
- 04_CODE/source_snapshot_import_verifier.py
- 04_CODE/pc_readonly_source_collector.py
- 05_TEST/test_source_snapshot_contract.py
- 05_TEST/test_source_snapshot_import_verifier.py
- 06_EVIDENCE/NU_WORK28_COMPLETE_SOURCE_LIFECYCLE_REMEDIATION_REPORT_20261015.md

## Version consistency observed
- Contract: 0.1.1; defines HARD_MAX_MANIFEST_BYTES = 2 MiB and casefold_path_key().
- Collector: pc-readonly-collector/0.3.0; imports shared metadata caps.
- Verifier: source-snapshot-verifier/0.2.0; bounds manifest before decode/JSON parse, checks collision keys, checks ZIP external attributes.
- Test sources include KAST-01 case-fold collision, KAST-02 symlink-mode ZIP member, KAST-03 oversized manifest, and contract metadata bounds.
- Nu report's Sections 9 and 11 identify the updated version matrix and explicitly supersede the older versions in Sections 1–2. Treat the correction as authoritative, but the report still begins with stale pre-remediation versions. A future cleanup should make the first summary/version matrix canonical to reduce operator error.

## Static findings

### KA-KAST-REV-01 — Metadata is bounded after full accumulation, not during enumeration
Evidence: collector enumerate_files() appends every excluded path to an in-memory list and only calls check_metadata_bounds(status_short, excluded) after enumeration returns.
Impact: the final manifest is capped, but a repository with a very large number of excluded entries can still consume substantial memory/time before rejection. This is a residual resource-exhaustion gap, not a claim that the 20,000 cap is absent.
Required: enforce count/length caps incrementally while appending excluded entries, failing closed before unbounded accumulation. Add test for early failure once the count/length cap is exceeded.
Status: IMPLEMENTED PARTIALLY / NOT EXECUTED; KAST-04 is not fully closed by static review.

### KA-KAST-REV-02 — ZIP member type hardening needs additional compatibility/negative cases
Evidence: verifier derives Unix mode from external_attr >> 16 and rejects non-regular types when mode is nonzero. Existing test covers a Unix symlink-mode member.
Impact: the important Unix symlink case is covered in source, but static evidence does not show coverage for DOS-created ZIPs with absent Unix type bits, DOS reparse/link-like attributes, or malformed/ambiguous mode metadata. Because the verifier is not an importer today, this is a hardening/test-coverage gap rather than proof of an extraction exploit.
Required: explicitly define accepted ZIP create_system and external-attribute combinations; add tests for mode=0, DOS attribute/reparse bit, FIFO/device/socket modes, and inconsistent directory flags. Decide compatibility policy rather than silently accepting ambiguous types.
Status: IMPLEMENTED PARTIALLY / NOT EXECUTED; KAST-02 needs a policy/test decision before closure.

### KA-KAST-REV-03 — Collision checks appear consistent at the string-contract layer
Evidence: contract computes NFC/NFKC casefold key and rejects duplicate keys; verifier separately checks manifest collision keys and archive-member collision keys, then validates exact archive paths against manifest entries.
Residual: regression source explicitly shows case-only collision cases; no independent test execution occurred. Confirm Unicode compatibility and Windows path equivalence cases when runner is available.
Status: STATIC REVIEW POSITIVE / NOT EXECUTED.

### KA-KAST-REV-04 — Manifest cap ordering appears correct
Evidence: verifier checks manifest byte length against HARD_MAX_MANIFEST_BYTES before hashing/decode/JSON parse; collector checks serialized manifest length before writing it and enters owned-output cleanup on failure.
Residual: collector's cap is hardcoded as 2 MiB instead of importing HARD_MAX_MANIFEST_BYTES, so contract/collector could drift in a later change. Prefer one shared constant and a test that proves collector and verifier agree.
Status: STATIC REVIEW POSITIVE WITH DRIFT RISK / NOT EXECUTED.

### KA-KAST-REV-05 — Owned output cleanup is safer but still untested
Evidence: collector rejects pre-existing output directory, sets owned=True only after successful mkdir, deletes only two known outputs and calls rmdir() only when owned.
Residual: failure-injection tests are not present in the readback evidence; concurrent mutation and Windows behavior are not proven.
Status: STATIC REVIEW POSITIVE / NOT EXECUTED.

## Gate disposition
- KAST-01: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.
- KAST-02: IMPLEMENTED PARTIALLY / NOT EXECUTED; ZIP type policy/test cases remain.
- KAST-03: IMPLEMENTED / STATIC REVIEW POSITIVE / NOT EXECUTED.
- KAST-04: IMPLEMENTED PARTIALLY / NOT EXECUTED; metadata accumulation needs incremental cap enforcement.
- F1 Windows race safety: BLOCKED.
- F3 receipt authentication/replay prevention: BLOCKED; receipt validation is not signature verification.
- Approved runner and canonical execution receipt: BLOCKED.
- Source transfer/import: BLOCKED.
- E2E-Automatic: BLOCKED pending source/runtime/runner evidence.
- Release: NO-GO.

## Next actions
1. Nu: fix KA-KAST-REV-01 and decide/cover KA-KAST-REV-02; share the manifest hard cap constant with collector to remove drift.
2. Go: review the updated tests for discoverability and coverage; execute only if approved runner is made available and tied to this exact Work revision.
3. Cla: independently review the amended ZIP type policy, Windows F1 and receipt F3 trust boundary.
4. Ka: reconcile the next revision and journal; continue the capability-gap design for approved runner and authenticated source transfer.
5. Vinh: final authority for release decision.

No test was run. No stdout/stderr, exit code, test count, or SHA-256 is claimed. No PC source was read, collector executed, source transferred/imported, or live service changed.
