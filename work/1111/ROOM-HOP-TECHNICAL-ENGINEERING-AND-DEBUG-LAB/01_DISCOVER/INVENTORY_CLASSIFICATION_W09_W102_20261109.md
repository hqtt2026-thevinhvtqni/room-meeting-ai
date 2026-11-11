# W09 INVENTORY CLASSIFICATION + W102 DUPLICATE TREE HASH REVIEW — C08

- Prepared by: Co — Coder under Cla (CTO)
- Date: 2026-11-09 (UTC+7)
- Scope: read-only Work 09 and Work 102 Sandbox listings/content. No delete, move, overwrite or source mutation in those Works.

## 1. W09 inventory — 4,127 listed entries

Classification uses path and extension rules. Directory entries are counted separately so the 4,127 total reconciles.

| Label | Entries | Rule |
|---|---:|---|
| Dependency cache | 2,321 | Under `.venv`, `venv`, or `site-packages`, excluding the more specific __pycache__ label |
| `__pycache__` | 1,737 | Path contains `__pycache__` or file ends `.pyc` |
| Evidence | 17 | Under `evidence` or `06_EVIDENCE` |
| Artifact | 0 | No matching artifacts/dist/build/log/XML/ZIP/binary output paths in this listing |
| Source code | 8 | `.py`, `.ps1`, `.js`, `.ts`, `.tsx`, `.jsx` outside cache/evidence |
| Documentation/configuration | 32 | Remaining non-directory documentation/config/metadata files |
| Directory structure | 12 | Entries that have descendants in the listing |
| **Total** | **4,127** | Reconciles to Sandbox listing count |

**Finding:** 4,058/4,127 entries (2,321 dependency-cache + 1,737 pycache) are environment/cache content, not application source. No deletion or relocation is proposed or performed. Artifact count is zero under the stated path/extension rules; this is not a statement that no runtime outputs exist outside the listed Work tree.

## 2. W102 duplicate tree comparison

Work 102 Sandbox listing contains 300 entries. The four requested pairs are:
- `04_CODE` ↔ `05_BUILD/04_CODE`
- `05_TEST` ↔ `05_BUILD/05_TEST`
- `06_EVIDENCE` ↔ `EVIDENCE/LEGACY_EVIDENCE_ARCHIVE`
- `07_RELEASE` ↔ `05_BUILD/07_RELEASE`

Hash method: SHA-256 over the exact UTF-8 file content returned by Sandbox readback. Directory entries are not hashed. A file present only on one side is recorded as MISSING on the other side. No content is normalized.


### Pair 1 — 04_CODE ↔ 05_BUILD/04_CODE

| Relative file | 04_CODE SHA-256 | 05_BUILD/04_CODE SHA-256 | Result |
|---|---|---|---|
| `agent_loop_contract.py` | `97b42907505ed7209f7db172fb81566bae3d49edff30b55b6135fdd7fc702609` | `97b42907505ed7209f7db172fb81566bae3d49edff30b55b6135fdd7fc702609` | **MATCH** |
| `agent_loop_runtime.py` | `789e25e99711915fd26cfa3b50cacfaef809b1f6cd2a751a169d5f0a721f3c74` | `789e25e99711915fd26cfa3b50cacfaef809b1f6cd2a751a169d5f0a721f3c74` | **MATCH** |
| `agent_workflow.py` | `5a7e9df5e934c86d8674a23793bb864484a1a378eeebfafff56ff375ed9770bf` | `5a7e9df5e934c86d8674a23793bb864484a1a378eeebfafff56ff375ed9770bf` | **MATCH** |
| `run_agent_loop.py` | `7cd54c100437566d1d1d8a6fa17db92086bcd591a24243c47a57e89ab7904057` | `7cd54c100437566d1d1d8a6fa17db92086bcd591a24243c47a57e89ab7904057` | **MATCH** |

### Pair 2 — 05_TEST ↔ 05_BUILD/05_TEST (batch 1)

| Relative file | 05_TEST SHA-256 | 05_BUILD/05_TEST SHA-256 | Result |
|---|---|---|---|
| `test_agent_loop_contract.py` | `9ddf9d8f33270b741210962d22ab9a80958bdcf4d2d04a0a7600b6c901caa6c6` | `9ddf9d8f33270b741210962d22ab9a80958bdcf4d2d04a0a7600b6c901caa6c6` | **MATCH** |
| `test_agent_loop_runtime.py` | `a26d0682d49ba2a41883b481388bdccf6a08cfb28e046c756f5773f4ee8c7d73` | `a26d0682d49ba2a41883b481388bdccf6a08cfb28e046c756f5773f4ee8c7d73` | **MATCH** |
| `test_agent_workflow.py` | `4cd664de6576d1496e6573c17fbcb61b28336ef0f3986b53595af3cce2944251` | `4cd664de6576d1496e6573c17fbcb61b28336ef0f3986b53595af3cce2944251` | **MATCH** |
| `test_recovery_regressions_vi.py` | `545e93f36b2a21e4763101c43f37dab1a5300dc066b9ffc3d4194003202f52ff` | `545e93f36b2a21e4763101c43f37dab1a5300dc066b9ffc3d4194003202f52ff` | **MATCH** |

### Pair 2 — 05_TEST ↔ 05_BUILD/05_TEST (batch 2)

| Relative file | 05_TEST SHA-256 | 05_BUILD/05_TEST SHA-256 | Result |
|---|---|---|---|
| `test_reference_verification.py` | `4a57b4cf1c31cdbbf714b1661a9f662fd6f1188a9a59da279bea32f85f03b32e` | `4a57b4cf1c31cdbbf714b1661a9f662fd6f1188a9a59da279bea32f85f03b32e` | **MATCH** |
| `test_workflow_evidence.py` | `1f99bc4b288029b324c7054d902dab4c9d7e368813c3542a6e1259c3c4d08c30` | `1f99bc4b288029b324c7054d902dab4c9d7e368813c3542a6e1259c3c4d08c30` | **MATCH** |

- Extra only in 05_TEST: `ACCEPTANCE_AND_TEST_PLAN.md`, `RUN_WORK102_E2E.ps1`.
- Extra only in 05_BUILD/05_TEST: `.gitkeep` and the `environment/` subtree (7 files). These are path/content differences, not duplicates.

### Pair 4 — 07_RELEASE ↔ 05_BUILD/07_RELEASE

| Relative file | 07_RELEASE SHA-256 | 05_BUILD/07_RELEASE SHA-256 | Result |
|---|---|---|---|
| `HANDOFF_REPORT.md` | `585d31724f46045e911d1acd1e4713e9fb7acef204ff522dbb77455977663ebe` | `585d31724f46045e911d1acd1e4713e9fb7acef204ff522dbb77455977663ebe` | **MATCH** |
| `VI_INDEPENDENT_HANDOFF_V3_20261025.md` | `6b0c56b5fe476dbbb195aecfab2d2c493d05962f61725e788c96e8ab9075a50f` | `6b0c56b5fe476dbbb195aecfab2d2c493d05962f61725e788c96e8ab9075a50f` | **MATCH** |

- Extra only in 07_RELEASE: `PC_ACCEPTANCE_CHECKLIST.md`.
- Extra only in 05_BUILD/07_RELEASE: `.gitkeep`, `LEGACY_PC_ACCEPTANCE_CHECKLIST_DO_NOT_EXECUTE.md`.


## 3. W102 pair results — completed subset and outstanding evidence

### Pair 1 — 04_CODE ↔ 05_BUILD/04_CODE
- Four same-name source files hashed: 4/4 MATCH.
- SHA-256 values are listed above in the pair table.
- Extra entries: `04_CODE/__pycache__` (directory only in source tree) and `05_BUILD/04_CODE/.gitkeep`.
- Disposition: content files MATCH; tree shape DRIFT due to the extra entries.

### Pair 2 — 05_TEST ↔ 05_BUILD/05_TEST
- Six same-name test files hashed: 6/6 MATCH.
- Extra only in `05_TEST`: `ACCEPTANCE_AND_TEST_PLAN.md`, `RUN_WORK102_E2E.ps1`.
- Extra only in `05_BUILD/05_TEST`: `.gitkeep` and seven files under `environment/`.
- Disposition: shared test files MATCH; directory contents DRIFT / not a mirror.

### Pair 4 — 07_RELEASE ↔ 05_BUILD/07_RELEASE
- Two same-name files hashed: 2/2 MATCH.
- Extra only in `07_RELEASE`: `PC_ACCEPTANCE_CHECKLIST.md`.
- Extra only in `05_BUILD/07_RELEASE`: `.gitkeep`, `LEGACY_PC_ACCEPTANCE_CHECKLIST_DO_NOT_EXECUTE.md`.
- Disposition: shared files MATCH; tree shape DRIFT.

### Pair 3 — 06_EVIDENCE ↔ EVIDENCE/LEGACY_EVIDENCE_ARCHIVE
- Listing shows 61 file entries under `06_EVIDENCE/` and 62 under `EVIDENCE/LEGACY_EVIDENCE_ARCHIVE/`; the archive has an additional `README.md`.
- All 61 shared evidence files were SHA-256 compared: 61/61 MATCH. The only extra file is `README.md` in the legacy archive.
- Disposition: 61/61 shared files MATCH; archive-only README retained. Tree shape differs; keep both trees unchanged.

## 4. Overall C08 disposition
- W09 inventory classification: COMPLETE; 4,127/4,127 entries assigned a category.
- W102 duplicate comparisons: all four pairs have complete SHA-256 comparison for every shared file; all shared files MATCH.
- No source Work file was deleted, moved, renamed or overwritten.
- Canonical recommendation is limited to the matching content files in pairs 1, 2 and 4; tree-shape extras remain legacy/staging candidates and must not be removed without owner review.
- **C08 = PARTIAL / BLOCKED** until all shared files in pair 3 are SHA-256 compared and a final canonical recommendation is reviewed.

### Pair 3 — 06_EVIDENCE ↔ EVIDENCE/LEGACY_EVIDENCE_ARCHIVE (files 1–4 of 61)

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `CO_XU_REVIEW_REMEDIATION_20261015.md` | `3e70c5181465e93cac619e8d7618b52c10357da72aecceac74e36ec92de873b6` | `3e70c5181465e93cac619e8d7618b52c10357da72aecceac74e36ec92de873b6` | **MATCH** |
| `DECISION_AND_DELEGATION_20261015.md` | `7c64fb484febced396ada04151e2d8a3aae78e84b198ec135939dac62e21ce43` | `7c64fb484febced396ada04151e2d8a3aae78e84b198ec135939dac62e21ce43` | **MATCH** |
| `DECISION_REPAIR_BUDGET_20261024.md` | `11e9b121dfa505b79d1f2d751ef7b797e006cad57ba06e1897af8a2dee71896a` | `11e9b121dfa505b79d1f2d751ef7b797e006cad57ba06e1897af8a2dee71896a` | **MATCH** |
| `ENTRY_GATE_READ_RECEIPT_20261015.md` | `a5b8f84d960e168e93c818decc1014395661c4520f966efa66f3c2a640efea74` | `a5b8f84d960e168e93c818decc1014395661c4520f966efa66f3c2a640efea74` | **MATCH** |

### Pair 3 — files 5–8 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `EXECUTION_LOG_20261015.md` | `93ce7c68a01a2dd0ac15d5c2670c8c21e59243b8cf018472c0425d9ebcfb06d9` | `93ce7c68a01a2dd0ac15d5c2670c8c21e59243b8cf018472c0425d9ebcfb06d9` | **MATCH** |
| `GATE_A_SOURCE_AUDIT_20261024.md` | `78c685b4ad79173420662097583b3916a314dcec4a3b964adddd0a747cfb85bb` | `78c685b4ad79173420662097583b3916a314dcec4a3b964adddd0a747cfb85bb` | **MATCH** |
| `INITIAL_SOURCE_AUDIT_20261015.md` | `c387cea3d78cd9a82050f7b704995facbb97d3bad3feffae8cd092533b5580f6` | `c387cea3d78cd9a82050f7b704995facbb97d3bad3feffae8cd092533b5580f6` | **MATCH** |
| `KA_INDEPENDENT_REVIEW_WITH_XU_20261024.md` | `13e04e78327387599cf9497a3185d2d017987a5cdb5a1ff9472cd4889ab6fae1` | `13e04e78327387599cf9497a3185d2d017987a5cdb5a1ff9472cd4889ab6fae1` | **MATCH** |

### Pair 3 — files 9–12 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `LEGACY_DOC-014_EVIDENCE-REGISTER-POINTER.md` | `fb5843cb1dbe5ddf9739beb9731bc257034972b45f417097bd4da565260ee7aa` | `fb5843cb1dbe5ddf9739beb9731bc257034972b45f417097bd4da565260ee7aa` | **MATCH** |
| `STATUS_SNAPSHOT_20261024_READY_FOR_PC.md` | `e38ddf0a625b5448a07a980a5c74e3d5af31d4c543cf93b55dda33263aa7d6e6` | `e38ddf0a625b5448a07a980a5c74e3d5af31d4c543cf93b55dda33263aa7d6e6` | **MATCH** |
| `VI_CURRENT_VERIFY_20261024/RUN_BUNDLE.json` | `5220424a219c5055aa53a3a9634afb49e8e8b0af03e69ecedd19d05cd61ab73c` | `5220424a219c5055aa53a3a9634afb49e8e8b0af03e69ecedd19d05cd61ab73c` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/RUN_MANIFEST.json` | `3a8a0112520c0d75af99e3b30b1a48a5eeb34ca9ddff0c1618393d30dd4a5d8b` | `3a8a0112520c0d75af99e3b30b1a48a5eeb34ca9ddff0c1618393d30dd4a5d8b` | **MATCH** |

### Pair 3 — files 13–16 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/collect.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/collect.stdout.txt` | `88490f00a72273cb1edae23f3a9d482ed90b3a4484d79d72ecd1034ade809f57` | `88490f00a72273cb1edae23f3a9d482ed90b3a4484d79d72ecd1034ade809f57` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/demo.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/demo.stdout.txt` | `55c23ffbf8ca64c44b05187ecec88e2f21d8c0aee1226aa58d71b328da4313aa` | `55c23ffbf8ca64c44b05187ecec88e2f21d8c0aee1226aa58d71b328da4313aa` | **MATCH** |

### Pair 3 — files 17–20 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/demo/checkpoints/w102-5f663f5bfd49459b9e2ebd9135bccefe.json` | `41ed82dc74e10595fb245d38c49de9df5c3f85451e1b74b52f33b0fcc75b25a2` | `41ed82dc74e10595fb245d38c49de9df5c3f85451e1b74b52f33b0fcc75b25a2` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/demo/w102-5f663f5bfd49459b9e2ebd9135bccefe.jsonl` | `a797089960b74f171a18c4f08aecce3901f741f02b0ee2992d94a179dd0f4e02` | `a797089960b74f171a18c4f08aecce3901f741f02b0ee2992d94a179dd0f4e02` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/dependencies.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/dependencies.stdout.txt` | `b49009c561e8b8cc6676d34a0013430bf769d3eaa9808cec8253e24242e21cbb` | `b49009c561e8b8cc6676d34a0013430bf769d3eaa9808cec8253e24242e21cbb` | **MATCH** |

### Pair 3 — files 21–24 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/pytest.junit.xml` | `0ceffdc5cbd874e2cd4ed127af304f02544f44ecd8747bd3e0cab40718c51110` | `0ceffdc5cbd874e2cd4ed127af304f02544f44ecd8747bd3e0cab40718c51110` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/pytest.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/20261025T135722Z-58be2c5213db/pytest.stdout.txt` | `c47715303eeb271cabdd4d63dcf114d2fb90334e89c6f9e7ed3050efd23ef317` | `c47715303eeb271cabdd4d63dcf114d2fb90334e89c6f9e7ed3050efd23ef317` | **MATCH** |
| `VI_INDEPENDENT_BUILD_20261025/MCP8030_DELIVERY_RECEIPT_20261025.json` | `d8d27c9fbb002e5e3060d2e693adad96b6ea896a1d504adc6fb8b76118678425` | `d8d27c9fbb002e5e3060d2e693adad96b6ea896a1d504adc6fb8b76118678425` | **MATCH** |

### Pair 3 — files 25–28 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_INDEPENDENT_BUILD_20261025/RUN_BUNDLE.json` | `4b71d9a3fc721da9c6b47208273de7ed006fe0c2b28fb8ffaa9374543c19c456` | `4b71d9a3fc721da9c6b47208273de7ed006fe0c2b28fb8ffaa9374543c19c456` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/RUN_MANIFEST.json` | `ef83d1b2ce8df5eb9a4e3ddaa13a5c492ced72147f5d6cd0909f6c9b479084f6` | `ef83d1b2ce8df5eb9a4e3ddaa13a5c492ced72147f5d6cd0909f6c9b479084f6` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/collect.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/collect.stdout.txt` | `46eced083cd86ba1225e138f84458a96571863af58720c6607f07fda893d0d6d` | `46eced083cd86ba1225e138f84458a96571863af58720c6607f07fda893d0d6d` | **MATCH** |

### Pair 3 — files 29–32 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_LOCAL_VERIFY_20261024/demo.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/demo.stdout.txt` | `0139d66598590b45d5a3a0126ae1340af0804f5f58474f5431e5bc87706695e4` | `0139d66598590b45d5a3a0126ae1340af0804f5f58474f5431e5bc87706695e4` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/demo/checkpoints/w102-285e4dd126c245048c5a85665cdb920a.json` | `a12456b455392b65f0fab0e3b1e397b83be8fe34cca7997820a8e193c31d3113` | `a12456b455392b65f0fab0e3b1e397b83be8fe34cca7997820a8e193c31d3113` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/demo/w102-285e4dd126c245048c5a85665cdb920a.jsonl` | `0fcf0aa9549074374aefd7f3fca72e9aaf0628096d946246648a9896f1b8f455` | `0fcf0aa9549074374aefd7f3fca72e9aaf0628096d946246648a9896f1b8f455` | **MATCH** |

### Pair 3 — files 33–36 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_LOCAL_VERIFY_20261024/dependencies.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/dependencies.stdout.txt` | `7920b4a00de0b36fd368ce8b42f07f6175ca241b0b670d47ee803c01c75de84d` | `7920b4a00de0b36fd368ce8b42f07f6175ca241b0b670d47ee803c01c75de84d` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/expanded_recovery_before.command.json` | `4b66815254b255cbde1ca0939bb81f64263b68c710e1b74eb75dac88cc9307ff` | `4b66815254b255cbde1ca0939bb81f64263b68c710e1b74eb75dac88cc9307ff` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/expanded_recovery_before.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |

### Pair 3 — files 37–40 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_LOCAL_VERIFY_20261024/expanded_recovery_before.stdout.txt` | `79b19c777e9d66320ac26e660cbe366081a19682a4a3253281b613046ac66859` | `79b19c777e9d66320ac26e660cbe366081a19682a4a3253281b613046ac66859` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/pytest.junit.xml` | `79d2d8bf6212b76b80c3fcd65a91aa764699f94839b1dc73aea38cb58262811f` | `79d2d8bf6212b76b80c3fcd65a91aa764699f94839b1dc73aea38cb58262811f` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/pytest.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/pytest.stdout.txt` | `4e59725b64b16c4b8d70a332b60e8e10048c2f9ecca76c39fb68348328e74f60` | `4e59725b64b16c4b8d70a332b60e8e10048c2f9ecca76c39fb68348328e74f60` | **MATCH** |

### Pair 3 — files 41–44 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_LOCAL_VERIFY_20261024/recovery_regressions.command.json` | `4b66815254b255cbde1ca0939bb81f64263b68c710e1b74eb75dac88cc9307ff` | `4b66815254b255cbde1ca0939bb81f64263b68c710e1b74eb75dac88cc9307ff` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/recovery_regressions.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/recovery_regressions.stdout.txt` | `a9405046a62f98f6430be02d3262f4a24128e3b4f9a2622b01a8a88c0230b511` | `a9405046a62f98f6430be02d3262f4a24128e3b4f9a2622b01a8a88c0230b511` | **MATCH** |
| `VI_LOCAL_VERIFY_20261024/test_recovery_regressions.py` | `139598fbbdb656bb4bcd5b7ba91f199eef1c2a317f406eae1315fe16a434de2c` | `139598fbbdb656bb4bcd5b7ba91f199eef1c2a317f406eae1315fe16a434de2c` | **MATCH** |

### Pair 3 — files 45–48 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_LOCAL_VERIFY_20261024/verify_snapshot.py` | `4fbada031c80f55c8b2dd6c367ac21cf5760dbaf79e9e13df531212a7e17baf6` | `4fbada031c80f55c8b2dd6c367ac21cf5760dbaf79e9e13df531212a7e17baf6` | **MATCH** |
| `VI_PATCH_REVIEW_20261024/FINDINGS_AND_HANDOFF.md` | `b7a7cd5d619fce185a577f5a5654ef356f725e788cd933cb16ba62f3f12c7027` | `b7a7cd5d619fce185a577f5a5654ef356f725e788cd933cb16ba62f3f12c7027` | **MATCH** |
| `VI_PATCH_REVIEW_20261024/PATCH_MANIFEST.json` | `9d9b325017600b0e5ae6ac36ef4a9fdc0aec6c0b3ea02b5789ba9420db1e75e5` | `9d9b325017600b0e5ae6ac36ef4a9fdc0aec6c0b3ea02b5789ba9420db1e75e5` | **MATCH** |
| `VI_PATCH_REVIEW_20261024/SUPERSEDED_CANDIDATE_RUN_BUNDLE.json` | `624a8df650f02b22320cb9b041f594bb02157b923622b2ed2a776468bd73e9f5` | `624a8df650f02b22320cb9b041f594bb02157b923622b2ed2a776468bd73e9f5` | **MATCH** |

### Pair 3 — files 49–52 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_PATCH_REVIEW_20261024/proposed_fix.patch` | `3dc3172e891993df80388613f3444e12fff33932895276cce7e1d8057ea17239` | `3dc3172e891993df80388613f3444e12fff33932895276cce7e1d8057ea17239` | **MATCH** |
| `VI_PATCH_V2_REVIEW_20261024/FINDINGS_AND_HANDOFF.md` | `6ab5ca72f4b8e3a28deb9606320e5ebe79b89ec61185cf66ac81d8c03c24bc1c` | `6ab5ca72f4b8e3a28deb9606320e5ebe79b89ec61185cf66ac81d8c03c24bc1c` | **MATCH** |
| `VI_PATCH_V2_REVIEW_20261024/PATCH_MANIFEST.json` | `804d9cd671bc06168ff2f9a16236da285833f9df2b2cf0cb08401bba46fb9e7e` | `804d9cd671bc06168ff2f9a16236da285833f9df2b2cf0cb08401bba46fb9e7e` | **MATCH** |
| `VI_PATCH_V2_REVIEW_20261024/RUN_BUNDLE.json` | `d7552cad037b04b3f8044d627a874213aa905d851a3216ee81bfbd293109add7` | `d7552cad037b04b3f8044d627a874213aa905d851a3216ee81bfbd293109add7` | **MATCH** |

### Pair 3 — files 53–56 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `VI_PATCH_V2_REVIEW_20261024/proposed_fix_v2.patch` | `07a26132f7fcc184127687834436bc8a019c28595bc7d46a4930906b01f51276` | `07a26132f7fcc184127687834436bc8a019c28595bc7d46a4930906b01f51276` | **MATCH** |
| `WORK102_RUNNER_STATIC_REVIEW_20261024.md` | `972dcd6255eac4ba9304b20c0c2c7e62eb90e94f3ed25f7a6b01dbb3f557ef5a` | `972dcd6255eac4ba9304b20c0c2c7e62eb90e94f3ed25f7a6b01dbb3f557ef5a` | **MATCH** |
| `WORK_102_AUTONOMOUS_BUILD_JOURNAL_20261015.md` | `9d609fbbe3d1519cddeffe18b4a3f62b3d5b2d70bb50a35e1962597c00c37803` | `9d609fbbe3d1519cddeffe18b4a3f62b3d5b2d70bb50a35e1962597c00c37803` | **MATCH** |
| `WORK_102_AUTONOMOUS_BUILD_MINUTES_20261015.md` | `135639e36346c05532961e58d6939379e9379b9d271cece55d30366abb4dadca` | `135639e36346c05532961e58d6939379e9379b9d271cece55d30366abb4dadca` | **MATCH** |

### Pair 3 — files 57–60 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `WORK_102_ENGINEERING_JOURNAL_20261015.md` | `22c30624b9320504bd682e879f8dbb314de34918b8e93b552b670ace0932c53d` | `22c30624b9320504bd682e879f8dbb314de34918b8e93b552b670ace0932c53d` | **MATCH** |
| `WORK_102_MEETING_MINUTES_20261015_1039.md` | `6f355577312e8b7e98eda3fd86eb7c5f2a439232f9f88a757f15e7f18e93e2b6` | `6f355577312e8b7e98eda3fd86eb7c5f2a439232f9f88a757f15e7f18e93e2b6` | **MATCH** |
| `WORK_102_STATUS_20261015.md` | `b178c2ab59bfe96b2e91a7cba8acb45df98627c5ec5c1e2ccdf947ebc1632439` | `b178c2ab59bfe96b2e91a7cba8acb45df98627c5ec5c1e2ccdf947ebc1632439` | **MATCH** |
| `XU_FOLLOWUP_REVIEW_20261015.md` | `6affe0837f0ff4b0dac6c63302f0914c576ef15519cfab25e0cd8841bf5473d2` | `6affe0837f0ff4b0dac6c63302f0914c576ef15519cfab25e0cd8841bf5473d2` | **MATCH** |

### Pair 3 — files 61–61 of 61

| Relative file | 06_EVIDENCE SHA-256 | LEGACY_EVIDENCE_ARCHIVE SHA-256 | Result |
|---|---|---|---|
| `XU_INDEPENDENT_STATIC_REVIEW_20261015.md` | `c0c4276a2ec959c853a9ecbaf174e2c2592cbd8977785cc3d7bf26335c87bc77` | `c0c4276a2ec959c853a9ecbaf174e2c2592cbd8977785cc3d7bf26335c87bc77` | **MATCH** |

- Extra only in legacy archive: `README.md`.


## 5. C08 completion correction — 2026-11-09
- The earlier interim count for pair 3 (71/72) was a listing-entry count that included directory entries. Recomputed file-only inventory using descendant detection: 61 files in `06_EVIDENCE`, 62 in `EVIDENCE/LEGACY_EVIDENCE_ARCHIVE`, 61 shared relative paths.
- SHA-256 comparison completed for all 61 shared files in batches; 61/61 MATCH. Archive-only file: `README.md`.
- Pair 1: 4/4 shared files MATCH. Pair 2: 6/6 shared test files MATCH. Pair 4: 2/2 shared files MATCH.
- Therefore all 73 shared file pairs across the four directory comparisons MATCH (4 + 6 + 61 + 2). Extra files/directories are documented; no cleanup action performed.
- Final status: W09 inventory 4,127/4,127 classified; W102 four pair comparisons complete for all shared files; C08 = READY FOR CLA REVIEW. No delete/move/overwrite.
