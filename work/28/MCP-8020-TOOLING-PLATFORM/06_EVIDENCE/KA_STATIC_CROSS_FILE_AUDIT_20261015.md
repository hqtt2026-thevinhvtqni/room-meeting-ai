# KA STATIC CROSS-FILE AUDIT — WORK 28
Date: 2026-10-15
Scope: read-only inspection of source_snapshot_contract.py, source_snapshot_import_verifier.py, pc_readonly_source_collector.py.
Status: STATIC ONLY; NOT EXECUTED.

## Findings
1. PATH COLLISION — The manifest contract and ZIP verifier track exact path strings. They do not reject case-fold collisions such as room_hop_mcp/A.py and room_hop_mcp/a.py. Windows destinations may treat these as the same path. Required: one documented target-platform collision key and negative tests. F1/F7 NOT PASS.
2. ZIP MEMBER TYPE — The verifier checks directory/encryption/compression/path/size/hash, but does not validate ZIP external attributes as regular files. It does not extract anything today; this blocks relying on it for a future importer. Required: reject non-regular and link-like entries, with tests. F7 BLOCKED for import use.
3. MANIFEST SIZE — Archive bytes are bounded, but manifest_bytes are decoded and parsed before a separate byte cap is checked. Required: hard manifest-byte limit before decoding/parsing and boundary tests.
4. METADATA BOUNDS — Collector builds status_short and excluded_paths without enforcing the manifest contract's item caps. Large trees may create a manifest the verifier rejects. On failure, the output directory may remain after its files are removed. Required: enforce caps before output creation and safely clean only the directory owned by this run.
5. RECEIPT TRUST — validate_transfer_receipt validates fields and hash strings only. It does not authenticate issuer_signature or prevent nonce replay. The function's own docstring says trusted transport must verify integrity. F3 remains BLOCKED until a real trusted issuer/verifier and replay policy exist.
6. WINDOWS RACE SAFETY — Collector uses path checks, identity/size/mtime comparisons, and O_NOFOLLOW when available. These checks alone do not prove Windows handle/reparse-point race resistance. F1 remains BLOCKED until platform-specific implementation and tests.
7. RUNNER — No approved Work-28 runner or immutable run receipt is exposed by the current connector. All runtime tests remain NOT RUN; E2E remains BLOCKED.

## Required next actions
- Nu: address findings 1-4 in one coherent Work-28 package; do not represent receipt-shape validation as authentication.
- Cla: independently review findings 1-6, especially Windows safety and actual trust issuance.
- Go: ensure each finding has regression tests and review discoverability; run only with an approved runner bound to exact artifacts.
- Ka: reconcile the artifacts, update journal, and specify the platform capability contract for source transfer and approved execution.
- Vinh: final release authority after evidence.

## Restrictions and evidence
No PC access, collector run, source transfer/import, PC modification, live service change, or release occurred. No SHA-256 is claimed because this connector exposes no hashing operation. This is a static review, not a security certification.
