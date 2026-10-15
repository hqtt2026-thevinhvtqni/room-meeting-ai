# KA-W28-EXECUTION-MODEL-SIMPLIFIED
Date: 2026-10-15 (UTC+07)
Signed by: Ka — CSA / Work 28 Coordinator (identity: ka-csa)
Authority: Vinh — Final Authority

## Binding execution decision
Vinh has simplified delivery: Ka leads the Work 28 build; Go owns implementation and delivers the integrated product; when Go finishes, Go reports the complete result to Vinh and Xu for final testing. Do not burden Vinh with slice-by-slice assignments or repetitive checkpoint approvals.

## Single delivery mission
Go owns one end-to-end delivery from current source audit through implementation, regression tests, an automatic runner where the approved environment permits, evidence/logs, and one consolidated handoff. WP1-WP7 are internal checklist items only. Continue all safe sandbox work without waiting for a new assignment. Report blockers together in the final handoff.

## Required handoff
One consolidated report must include:
- changed files and source/version identity;
- tests actually executed, exact command, exit code, counts and logs;
- tests not run and why;
- contract serialization behavior and regression coverage, including KA-AUDIT-28-07;
- runner and E2E results, distinguishing source review, local test, approved runner, and live E2E;
- runtime/MCP/Core/WorkContext/isolation dependencies and blockers;
- integrity hashes only when actually computed by an available approved tool;
- concise instructions for Xu and Vinh to independently retest.

## Acceptance flow
1. Go builds and submits the complete integrated handoff.
2. Xu and Vinh independently retest the delivered result.
3. Ka reviews evidence and consolidates PASS/BLOCKED findings.
4. Vinh makes the final acceptance/release decision.

Cla may provide security review as a supporting independent review, but Cla's review must not unnecessarily stop safe contract/tool building. Any actual security risk remains explicitly blocked and must not be represented as passed.

## Safety and truthfulness boundaries
Continue safe, isolated sandbox implementation and testing. Do not enable python_run, mutate live registry, write to PC/GitHub, sync, merge, or release without separate authorization. Do not claim tests, live E2E, or security PASS without actual evidence. Keep live MCP E2E and release marked BLOCKED/NO-GO until their prerequisites and evidence exist.

## Signature
Ka — Chief System Architect (CSA), Work 28 Coordinator
Date: 2026-10-15 (UTC+07)
This is a textual coordination signature, not a cryptographic signature.
