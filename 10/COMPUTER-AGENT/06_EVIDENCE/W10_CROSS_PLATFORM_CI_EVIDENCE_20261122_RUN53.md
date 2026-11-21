# WORK 10 — CROSS-PLATFORM VERIFICATION EVIDENCE — RUN 53

- Document ID: W10-CROSS-PLATFORM-CI-EVIDENCE-20261122-RUN53
- Workflow: Work 10 Cross-Platform Verification
- Run ID: 44960863874 / Run #53
- Branch: `work/10-computer-agent-mirror`
- Exact tested commit: `29daa718509b1c3906527a8cd9358104061e3b85`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44960863874
- Conclusion: SUCCESS — both matrix jobs succeeded.

## Ubuntu 24.04
- Job ID: `137019141770`
- Regression totals: **183 PASS / 0 FAIL / 2 SKIP**
- V8 acceptance validator: 16 PASS / 0 FAIL
- Real Chromium E2E: PASS
- Syntax, contract, safety, HTTP, process containment and host operations: PASS
- Artifact ID: `14728729586`; size 40,047 bytes
- ZIP SHA-256: `cca2583aca62d247c43b795205d63837570e451f3f98e87d4558c035cdcd2b26`

## Windows Server 2022
- Job ID: `137019141975`
- Regression totals: **189 PASS / 0 FAIL / 0 SKIP**
- V8 acceptance validator: 16 PASS / 0 FAIL
- Real Chromium E2E: PASS
- Syntax, contract, safety, HTTP, process containment and host operations: PASS
- Artifact ID: `14729905280`; size 33,922 bytes
- ZIP SHA-256: `f6254b5e1fb0c5d27b98def8434cb2f59781e5c45fffd0af2e771eff61d780bf`

## What this run specifically verifies
The exact Sandbox hardening of `04_CODE/acceptance_validator.py` was synchronized to the canonical branch before this run. The hardened validator now checks:
- exact category catalog (no missing or unknown category);
- policy ID, policy version and schema version;
- valid outcome, lease-state and owner-state sets for every category;
- trusted runner/source commit, schema/validator/policy pins, state equality, artifact and fixture hashes, and signed attestation as already covered by the V8 validator suite.

Both operating-system runners passed the existing 16-case adversarial V8 suite after this hardening. Run #53 does not prove production key provisioning or acceptance validation on the Owner's PC.

## Limitations
- Windows runner is Windows Server 2022, not the physical Windows 10 PC.
- Linux containment remains `LIMITED_NOT_CGROUP_V2`; production cgroup-v2 profile remains open.
- CI HMAC key is test-only; production HMAC key and pinned hash provisioning remain open.
- ROOM-HOP Dashboard / PC Bridge integration E2E remains open.
- Run #53 proves the tested GitHub branch commit only; full Sandbox/GitHub inventory reconciliation remains in progress.

## Disposition
- V8 validator hardening cross-platform CI: **PASS — RUN 53**.
- Physical Windows 10: **NOT RUN**.
- Linux cgroup-v2 production containment: **OPEN**.
- Production key provisioning: **OPEN**.
- ROOM-HOP integration: **OPEN**.
- Work 10: **ACTIVE — NOT RELEASED**; no main merge or release.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
