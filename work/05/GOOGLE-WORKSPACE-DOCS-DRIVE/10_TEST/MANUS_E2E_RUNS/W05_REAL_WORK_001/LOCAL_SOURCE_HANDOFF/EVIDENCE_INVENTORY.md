# Work 05 Canonical Source Handoff — Evidence Inventory

Canonical target: `GOOGLE-WORKSPACE-DOCS-DRIVE/10_TEST/MANUS_E2E_RUNS/W05_REAL_WORK_001/LOCAL_SOURCE_HANDOFF/`

## Local source/test verification

Source files: 6 implementation files under `src/`. Test files: 7 files under `tests/`. Local evidence files: 46 under `evidence/`. Local result: **24 passed, 1 deselected**.

## Canonical read-back verified

ROOM-HOP read responses confirmed the presence and content of the six source files, seven test files, `pytest.ini`, `WORK05_SOURCE_HANDOFF.md`, connection/OAuth documentation, REAL GOOGLE/G09 readiness documentation, and Room UI documentation under the canonical handoff path.

## Local artifact hashes

```text
0663f47a863d8ba24b5688fb11d0be82ae89c7cf88568af32b9b751482fbf3e8  src/work05_mock.py
271a56fe313d100a745d09106a4d666606379b0a3c0052d713aa10c55fb72951  tests/test_work05_real_provider.py
3c57386bb1fcedef432aa7f07523a186cd1c1e5626b8493cee9cba35e40b31db  tests/test_work05_mock.py
3e2a43d48ac8bbc09cfe1bd64d1bac9ad99cd40a9ca67c53957d80940cbc5138  src/work05_connections.py
3e976411aa76fa1d97cd2dcf487439d1c9e0ed7f39cce8e09130447a8a360ba4  src/work05_google_adapter.py
442964b91c63ba4bb87d3dd871aed4e66456dc57af5a00f29a453ab9cc5783c9  src/work05_real_provider.py
84d546ecae94aed131b9478ffdd1a716750652e63fb98edf82c0faff9923d4df  tests/test_work05_g09.py
8ddee9f6324c2814d5ea9a608d0f6d6d15f855de077ee04ce67cb728dffd04ab  tests/test_real_google.py
a7a8a78399da70a1fe78a1059d38ff5fe50a8b0e400df2ff2352b1e187188ace  tests/test_work05_google_adapter.py
ab793ecc0e040cbd6da80bfb52cbdb7e4ab814388acfa1430189e39a1e26317e  tests/test_work05_services.py
b6cc774ecd5ced92e1a86b63058c68715567e87a661400beebab350fd056a7fd  pytest.ini
bdfb6551cf23763e412ee1e80a0438a89be42b9ded5878a3ace3c6ee39da7d29  tests/test_work05_connections.py
f33e8288724309c8a246bc75bdfcf67b9cf654d51343691afbe5de137762b39e  src/work05_reconcile.py
f44325251e3a4ddf6efa0cc7ebbe791c98175cacc196fce8bc7465d2222e0923  src/work05_services.py
```

## Local evidence inventory

Local-only filenames include Phase-1 root failures and pytest outputs; Phase-2, Phase-3, and Phase-4 plans/build/test/recovery/QE/release/checksum records; connection/OAuth documents; REAL GOOGLE/G09 recovery documents; and Room UI readiness documents. The connection, REAL GOOGLE/G09, and Room UI documents are individually persisted and read back under this canonical handoff.

## Classification

**VERIFIED_CANONICAL_READBACK:** source files, test files, `pytest.ini`, connection/OAuth docs, REAL GOOGLE/G09 readiness docs, Room UI docs, `WORK05_SOURCE_HANDOFF.md`, and this inventory.

**HISTORICAL_CANONICAL:** original `W05_REAL_WORK_001` phase/run evidence already present in canonical Work 05 before this handoff.

**LOCAL_ONLY_UNTIL_COPIED:** local Phase-2/Phase-3/Phase-4 continuation evidence and root completion artifacts not individually read back from canonical in this operation.

**BLOCKED:** REAL GOOGLE runtime, production secret manager, and Room UI browser E2E.
