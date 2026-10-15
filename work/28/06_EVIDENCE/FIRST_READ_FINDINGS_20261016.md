# WORK 28 — FIRST READ FINDINGS — 2026-10-16

## Source readback completed by Xu
Branch: `work/28-mcp-tooling-platform`.

| File | Blob SHA | What it proves |
|---|---|---|
| `work/28/README.md` | `60ca48f55360131362e91b22e7d5b80ecc0e2603` | Work remains ACTIVE / NOT LOCKED; runtime E2E remains blocked/unverified. |
| `.github/workflows/work28-mcp-tooling.yml` | `9f8573be16e11b95ee68f0d907772f111a0f3f82` | CI runs `python -m unittest discover -s 05_TEST -v` in Work 28 with `PYTHONPATH=04_CODE`; it is a unit/regression workflow, not live MCP E2E. |
| `04_CODE/tool_contracts.py` | `218664f00994d1f25a54945f3032687b88c237b1` | Contract v1.3.0 explicitly says TrustedPrincipal/WorkContext are data contracts only and do not prove authenticity/authorization; adapter/Core must bind trusted transport identity. |
| `05_TEST/test_tool_contracts.py` | `8f7b9279935230c8890150b7e08c83a12e751139` | Test file covers contract shape/security boundaries; header explicitly says tests do not prove Core authorization, OS isolation or live E2E. |
| `03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md` | `1741180e968f9064f812071cc7baec962dfee868` | Registry is DRAFT / NOT REGISTERED IN LIVE MCP; P0 additions remain proposals. |
| `05_TEST/WORK_28_TEST_PLAN.md` | `224790586eddde11f47858634e77d7c03d2696ce` | G3 approved-runner tests, G4 auth/path/isolation, G5 live MCP→Core→runtime→evidence and G6 full E2E are listed as BLOCKED. |
| `06_EVIDENCE/TOOL_GAP_DECISION_20261015.md` | `a726be0b159a058340084115ac4e32aab70c3305` | P0 sequence is to verify canonical Core/Sandbox API first, then add missing read-only capabilities only if absent. |
| `06_EVIDENCE/CROSS_WORK_TOOL_CAPABILITY_AUDIT_20261015.md` | `4e268958f903fe01876ba6c1f0dc9790115d1984` | Connected-session tool list is not proof of PC MCP :8020 registry; execution tools remain unverified. |

## Immediate decision for Xu
1. Do not start by adding tools blindly. First trace whether Core/Sandbox already provides equivalent search/stat/range-read/capability discovery APIs.
2. The first implementation target, if API trace proves a gap, is the smallest P0 read-only capability with bounded output, Work-root containment, Core authorization, negative tests and readback evidence.
3. Do not register Python execution or add a new runtime. Execution remains NO-GO until the canonical Core/host route and isolation are proven.
4. The current read was source/document inspection via GitHub; it is not a local test run and not live PC :8020 evidence.

## Agent task tracking
- Xu P0: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/8
- Go P0: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/9
- Cla P0: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/10
- Ka CSA P1: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/11

These issues are concrete task specifications. They do not prove that the named agents have acknowledged or begun work. No Work 13 source or tests were changed.
