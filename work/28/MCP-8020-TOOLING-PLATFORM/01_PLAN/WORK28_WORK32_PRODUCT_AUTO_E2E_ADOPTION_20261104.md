# WORK 28 — Adoption of Work 32 Product Auto E2E Model

- Document ID: A2E-W28-W32-ADOPTION-20261104-001
- Recorded: 2026-11-04 06:37 UTC+07:00
- Source model: Work 32 / CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Work 32 Sandbox evidence inspected: W32-EVIDENCE-004, W32-EVIDENCE-005, W32-EVIDENCE-007, W32-EVIDENCE-008; W32-ADR-001 and W32-ADR-002; CI_GATE_MATRIX.md; product E2E source and result classifier.
- Work 32 product evidence source SHA: 4a931a351432a1ce6a06b84f05ed6fa3c788a1eb (W32-EVIDENCE-007). Work 32 branch: work/32-ci-cd-python-ci-v2.
- Work 28 branch baseline inspected: 1f440eb9f21c356423d3a0eb13cb8b717a8694f3.
- Owner: Xu (coordination); Vi (implementation); An (independent QA); Ka (independent architecture/security review).

## 1. Decision

Adopt the proven Work 32 **product-level Auto E2E delivery pattern**, not its product-specific meeting implementation. Work 28 remains a separate security-sensitive execution product. Preserve the Work 28 contracts, Work 28 Auto E2E evaluator, existing test suites and current fail-closed gate.

The key improvement over a CI-only green check is to prove a real user/product journey across the actual boundaries, verify persisted output, then build and retest an immutable artifact from the exact triggering commit. Every gate must be bound to the exact SHA and retain machine-readable evidence.

## 2. What was learned from Work 32

1. CI-first and CD-separated: hosted Python 3.12 runner, least-privilege repository permission, no automatic deployment or main merge.
2. Exact-SHA execution: checkout the triggering commit, install declared dependencies, run pip consistency checks and compile the application before tests.
3. Contract-first integration: reconcile the public MCP tool inventory with the authoritative HTTP/API contract; do not add duplicate lifecycle tools to MCP to satisfy stale tests.
4. Real boundary E2E: launch the actual MCP stdio subprocess and exercise the real HTTP adapter/service path; do not substitute a mocked transport or fake service for the claimed product journey.
5. Product lifecycle proof: exercise success and negative policy/quorum paths, then read persisted transcript/artifact back and compare exact bytes/content.
6. Immutable artifact proof: archive the exact source SHA, calculate and verify SHA-256, extract to a clean directory, reinstall/check dependencies, compile and rerun product E2E against the extracted artifact.
7. Honest gate separation: unit, integration, product E2E, artifact E2E, dashboard/browser integration, CD and release have separate statuses. A successful Core product E2E does not imply dashboard integration or deployment is accepted.
8. Evidence completeness: record runner, exact command, exit code, test counts, source SHA, artifact ID/digest, logs and uncovered scope. Failed intermediate runs remain diagnostic evidence and are not overwritten by a later pass.

## 3. Work 28 translation — target product journey

The Work 28 product-level scenario must prove this chain, using trusted identities and the one approved route:

DISCOVER deployed MCP identity and tools/list
→ AUTHORIZE trusted caller through Core :8000 for canonical Work ID W28 (with explicit mapping to Sandbox Work key 28)
→ SNAPSHOT a Work-relative source into an immutable snapshot
→ HASH expected source, snapshot and runtime input
→ DISPATCH only through the approved Runtime MCP and Execution Host :8031
→ COLLECT actual exit code, structured test summary, bounded output references and process-tree cleanup
→ VERIFY policy, source/runtime identity, isolation and test result
→ PERSIST protected append-only evidence
→ READBACK through the authorized read API and verify reference + SHA-256 equality
→ REPORT source-bound JSON, CI summary and immutable artifact references.

Negative cases must include Core DENY before side effects, wrong Work ID, forged/missing principal, path traversal/symlink escape, source hash mismatch, unapproved runtime, unavailable isolation, timeout/nonzero exit, zero tests, test failures, incomplete process cleanup, evidence write failure, readback mismatch and secret leakage. No failure case may fall back to another runtime or authority.

## 4. CI stages to adopt

| Gate | Work 28 implementation target | Evidence required |
|---|---|---|
| G0 — provenance | Exact triggering SHA, branch, changed paths and source inventory | SHA + manifest/path report |
| G1 — build hygiene | Python 3.12, declared dependency install, pip check, compileall | versions, commands, exit codes |
| G2 — unit/regression | Existing Work 28 unittest and Linux/Windows lifecycle suites | JUnit/raw logs and exact counts |
| G3 — MCP contract | Actual stdio subprocess, exact registered tool/schema inventory and Core contract compatibility | tools/list digest, subprocess logs |
| G4 — product E2E | Disposable Work fixture through trusted Core authorization, approved runtime and Execution Host; success + negative authorization/policy cases | request/run IDs, identities, exit/test summary, cleanup |
| G5 — immutable artifact | Exact-SHA source archive, SHA-256 verification, clean extraction, dependency/compile checks and rerun of eligible E2E | archive digest + artifact-level test report |
| G6 — evidence persistence | Protected evidence write and authorized readback | evidence ref + matching SHA-256 |
| G7 — independent acceptance | An QA and Ka architecture/security review; Xu consolidates; Vinh controls release decision | separate signed reports; no self-approval |

The CI workflow should run the independent jobs in parallel where safe, then run artifact-level E2E only after required build/test gates succeed. The final report job must run with an always-condition so failures are reported, but it must never turn a failed or missing upstream result into PASS.

## 5. Work 28-specific constraints

- Work 32's meeting lifecycle and endpoint names are examples only; do not copy them into Work 28.
- Keep Core :8000 as sole authorization authority. A test double/local CI service may support component testing but cannot be called deployed Core E2E.
- The current Work 28 CI preflight and signed evidence evaluator remain useful, but they do not prove live MCP 8030 → Core → Runtime → Execution Host integration.
- Do not probe, restart, activate or route to historical MCP 8020. The new Runtime MCP must be separately identified and approved.
- No arbitrary shell, direct workspace/database access, forged caller identity, local fallback authority, duplicate Execution Host, fail-open dispatch or unprotected evidence.
- No secrets in repository artifacts or logs. Attestation keys remain deployment-held and out-of-band.
- Do not auto-deploy, merge/rebase to main, push to production or open Execution Gate. Current status remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
- Sandbox is the controlled build/verification zone; GitHub Work 28 branch is canonical. Sync GitHub → Sandbox only after branch commit and verify exact content. No automatic two-way sync.
- An and Ka remain independent; Vi's CI/self-tests do not replace their reports.

## 6. Implementation sequence

1. Harden the existing Work 28 workflow to the Work 32 exact-SHA/build-hygiene standard: audited SHA-pinned actions, explicit Python 3.12, dependency consistency, compileall and clear failure summaries. Preserve existing Linux/Windows coverage.
2. Add a real MCP stdio contract test for the Work 28 public tools and schema digest, based on the actual server factory/transport; do not mock the transport in the claimed subprocess test.
3. Add the Work 28 disposable product journey only when the real trusted Core authorization route and approved Runtime/Execution Host contract are available. Until then report G4 BLOCKED, not a simulated PASS.
4. Add exact-SHA immutable source artifact build/extract/retest, clearly distinguishing artifact CI from deployed runtime.
5. Connect protected evidence persistence/readback only through the authorized Work 28 evidence service; retain HMAC verification and all path/symlink/secret gates.
6. Run the exact final branch SHA, inspect every job/log/artifact, sync committed files to Sandbox and verify exact readback.
7. Hand the same SHA and evidence package to An and Ka for independent review. No acceptance or release status is inferred from their assignment.

## 7. Baseline and open gaps

At adoption time, Work 28 has four successful CI jobs and a fail-closed evidence evaluator. The latest recorded exact-branch pipeline run is 41723833958 on commit 1f440eb9f21c356423d3a0eb13cb8b717a8694f3. This proves the existing CI preflight only.

Not yet proven: live MCP 8030 process/build identity and tools/list parity; trusted Core principal/WorkContext grant on the deployed path; approved Runtime MCP identity; Execution Host :8031 deployment/isolation attestation; protected evidence persistence and authorized readback; complete deployed request-to-evidence chain. These remain explicit blockers.

## 8. Sign-off boundary

This document records Vi's implementation decision to adapt the Work 32 model to Work 28. It is not An's QA acceptance, Ka's independent review, Xu's gate approval, or Vinh's release authorization.

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]
