# KA WORK 28 — CONTINUOUS E2E-AUTOMATIC EXECUTION ORDER
Date: 2026-10-15 (Work 28 evidence timestamp; no claim about current Room Hop clock)
Authority: Vinh final authority; Ka CSA coordinator; Nu implementation owner; Go independent reproducibility reviewer; Cla independent security reviewer.

## Purpose
This is a continuation order, not a release approval. Work must continue across all safe lanes instead of stopping at the first missing capability. Keep EVIDENCE FIRST and never convert static review into runtime PASS.

## Current verified constraints
- Work 28 MCP Sandbox read/write is available.
- This connector has no approved Python/test runner, no trusted source-transfer receipt issuer, and no demonstrated canonical PC-source binding.
- Cla review signature identifies its author/conclusions only. `CLA_PROPOSED_RED_TESTS_20261015.py` remains PROPOSED / NOT RUN.
- Existing source collector is a draft, not approved to run. F1 and F3 are not passed.
- No PC write, source import, live service restart, live registry mutation, or release is authorized by this order.

## Parallel work lanes — execute in this order without waiting idle

### Lane A — Ka (now; static implementation review)
1. Continue direct readback of all Work 28 artifacts and perform a static cross-file consistency audit of collector, manifest contract, archive verifier, tests, and work plan.
2. Record every finding with file/path, exact function, impact, acceptance condition, and evidence status. Distinguish code-observed facts from inference.
3. Make safe Work-28-only changes to documentation/contracts/tests only when the change is clearly justified and does not impersonate the canonical runtime implementation.
4. Keep a running decision ledger and journal. Every action ends with one of: DONE WITH READBACK, BLOCKED WITH SPECIFIC MISSING CAPABILITY, or NOT RUN.

### Lane B — Nu (implementation owner; acknowledgement still required)
Deliver one coherent source-lifecycle package, not fragmented patches:
- F1: Windows parent components, symlink/junction/reparse points, descriptor/path identity, mutation during read, race tests, and platform-specific behavior. If no approved runner, label tests NOT RUN and supply deterministic test commands, not invented results.
- F3: receipt trust design must name the actual trusted issuer/verifier and approved channel; schema validation or a string called issuer_signature is not authentication. Do not fabricate a receipt or key.
- F7: bound excluded-path/status metadata; ensure failure cleanup removes or explicitly quarantines partial output; ZIP size/entry/path limits and deterministic output.
- F8: fixed Git argv, shell=False, timeout, bounded stdout/stderr, no optional locks/fsmonitor, isolated environment, no hooks/network side effects.
- Reconcile contract and verifier hard caps; add tests for case-insensitive path collisions on Windows, reserved names, ZIP external attributes/symlink-like entries, metadata cap overflow, failure cleanup, and repeated/nonces.
- Update the consolidated report and journal with exact file list and evidence states. Do not run the collector or access PC under this order.

### Lane C — Go (independent review; no task inbox dispatch capability confirmed)
1. Review Nu's consolidated package after it is present. Before that, continue static test-quality review of existing artifacts.
2. Confirm discoverability/import assumptions and whether each test has positive, negative, boundary, and failure-injection coverage.
3. Run tests only if an approved Work-28 runner becomes available and is explicitly bound to the exact artifact revision. Otherwise record NOT RUN, exact reason, and required runner contract.
4. Do not treat agent-local Python or copied files as canonical Work-28 evidence.

### Lane D — Cla (independent security review)
1. Review the signed trust-boundary/F1/F3 memo plus collector/verifier implementation and proposed red tests.
2. Specifically decide whether F1 can be passed on Windows and whether F3 has a real authenticated issuer/channel/replay defense. State evidence for each; do not infer runtime enforcement.
3. Review F7/F8 as secondary gates and identify any bypasses.
4. Current Cla inbox was checked and empty; this order is persisted guidance, not proof Cla has received or accepted it. No acknowledgement may be claimed until observed.

## Next dependency to solve — source and runner capabilities
Ka must not stop at "connector lacks feature". Produce a concrete capability-gap proposal for the ROOM-HOP platform:
1. Read-only source export operation: fixed allowlist, bounded streaming, manifest and per-file hashes, no secrets, no execution.
2. Authenticated transfer receipt: issuer identity, source commit/tree identity, archive and manifest digests, destination Work ID, channel/session, timestamp, nonce/replay storage, signed receipt verification.
3. Approved isolated Work runner: immutable artifact revision binding, no network by default, bounded CPU/memory/time/output, captured stdout/stderr/exit code, test discovery, signed/append-only run receipt.
4. Explicit policy gates and tests for denial, cancellation, timeout, resource cap, and tamper.
These are proposed platform requirements, not claims that the tools already exist.

## Acceptance gates
- G0 Source identity and complete allowlisted source snapshot: BLOCKED until real source bytes and authenticated provenance are available.
- G1 Manifest/archive structural verification: code-reviewable now; runtime test status remains NOT RUN without approved runner.
- G2 F1 filesystem race safety: NOT PASS until platform-specific evidence.
- G3 F3 provenance/authentication/replay: BLOCKED until trusted receipt issuer/verifier exists.
- G4 test reproducibility: BLOCKED until approved runner bound to exact revision.
- G5 live MCP→Core→authorized runtime→protected evidence→readback: BLOCKED until real source and runtime-binding evidence exist.
- G6 release: NO-GO until all required gates pass.

## Reporting contract
Every update must include: artifact path; exact scope; action performed; readback result; runner identity/revision if executed; command; stdout/stderr; exit code; test count; SHA-256 if an actual hash tool is available; status per gate; residual risks. Never invent unavailable fields.

## Immediate next step
Ka continues static audit and writes concrete findings to Work 28 now. Nu/Go/Cla are expected to act within their lanes when they access this order; no agent receipt is assumed. Vinh retains final authority.
