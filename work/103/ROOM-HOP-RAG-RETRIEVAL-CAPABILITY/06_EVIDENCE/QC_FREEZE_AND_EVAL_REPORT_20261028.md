# Work 103 — Data Freeze, SHA-256 & Approved-Procedure Evaluation (QC, 2026-10-28)

Role: **Qc — Coder**. Trigger: nhãn đã được duyệt (EVAL_SET v2, 50 answerable +
15 no-answer; audit tại `LABELED_SET_AUDIT_20261028.md`, chấp thuận theo
quyết định Xu 2026-10-28 ghi trong `ACCEPTANCE_AND_E2E_PLAN.md`).
Deliverables of this task: **tệp nhãn đã khóa (frozen), SHA-256 fingerprints,
báo cáo kiểm thử chạy theo quy trình đã duyệt.**

## 1. What was frozen and how

New tooling (never edits the labeled data itself):

- `04_CODE/freeze_eval_set.py` — validates EVAL_SET.json with the strict
  schema in `rag_eval.validate_eval_set`, computes SHA-256 fingerprints, runs
  the approved evaluation procedure at the operating point, and writes an
  immutable freeze manifest + raw artifacts. Exit 1 (no manifest written) if
  schema validation or the baseline gate fails.
- `04_CODE/verify_frozen_eval_set.py` — recomputes hashes on the current file
  and re-runs the evaluation, requiring EXACT reproduction of every recorded
  ranking metric and gate verdict.

Freeze record: `06_EVIDENCE/FROZEN_EVAL_SET_v2.json` (status
`FROZEN_IMMUTABLE`). Two hash kinds are recorded deliberately:

- `file_sha256` — byte-exact tamper evidence over the committed file.
- `canonical_sha256` — SHA-256 over canonical JSON (`sort_keys=True`,
  compact separators, UTF-8): content equality that survives formatting-only
  changes, so reproducibility checks don't break on cosmetic edits.

## 2. SHA-256 fingerprints (freeze basis)

| Item | SHA-256 |
|---|---|
| `05_TEST/EVAL_SET.json` (11,641 bytes, version 2) — file_sha256 | `ab60cabdeee6254e11ee6889c20b6f2e68cd5072687bafcb314fb7c9a37c9f07` |
| EVAL_SET.json — canonical_sha256 | `03d1c964ce33689d5fcfcc56c6b1c2d0a8079b109055f78e183d4fd17e15ae` |
| labeled_queries (50) — canonical_sha256 | `c44eded3b829c180dd63ae155721231c8f226f4442e49011769c95040a07d9e4` |
| no_answer_queries (15) — canonical_sha256 | `82116d0279cd469592a9d33743dbe83833e0aafa715e22c97b0b39de5af54228` |
| corpus source-id list (8 docs) — canonical_sha256 | `8ec8e622e32c1be4e2454efce3408780cdd237b3a8f972ffe532b1930e3f5ce1` |
| Freeze manifest `FROZEN_EVAL_SET_v2.json` | `b9cc53ed6977c568fc84bd0aa8ce4b258b3cfd1002cda61f90fe62c51c7e4684` |
| Tool `freeze_eval_set.py` | `b00ba38dd974d0dff814f12e92625bee1af70f21d4fa420c3965130d2a7432a6` |
| Tool `verify_frozen_eval_set.py` | `5de22a6a13e07dc2568f0d5b4b4da5f55b6b646acc71c4627d2505bda9b660f8` |

Provenance: commit `5f91f3ea2143dafaa5af958dc2bb431399e93621` (tree
`8c05feccedb83e2d44d01b09d1c9a63fbd12cb5d`), branch tip containing EVAL_SET
v2 unchanged. The worktree was dirty ONLY with the new QC tools being added by
this task; the labeled set itself matches the committed blob exactly
(`git diff` empty). Frozen at 2026-10-28T22:47:04+07:00.

## 3. Test report — executed per the approved procedure

Environment: Python 3.12.10, linux, local run from the branch checkout.
Raw stdout captured under `06_EVIDENCE/frozen/`.

| Step | Command | Result | Artifact |
|---|---|---|---|
| Schema validation (strict) | inside freeze/eval tools | PASS (raises on any violation) | — |
| Baseline eval gate @ min_score=0.35, top_k=5, chunking 300/40 | `python 04_CODE/rag_eval.py` | **PASS, exit 0** | `frozen/eval_gate_stdout_20261028.txt` |
| Unit tests — retrieval suite | `python -m unittest discover -s 05_TEST -p test_rag_retrieval.py` | **OK 19/19, exit 0** | `frozen/unit_retrieval_stdout_20261028.txt` |
| Unit tests — eval-harness suite | `python -m unittest discover -s 05_TEST -p test_rag_eval.py` | **OK 24/24, exit 0** | `frozen/unit_eval_stdout_20261028.txt` |
| Freeze run | `python 04_CODE/freeze_eval_set.py` | manifest written, **exit 0** | `FROZEN_EVAL_SET_v2.json`, `frozen/FROZEN_EVAL_SET_v2/eval_operating_metrics.json` |
| Verify-after-freeze | `python 04_CODE/verify_frozen_eval_set.py` | ✅ intact, results reproduce exactly, **exit 0** | `frozen/verify_stdout_20261028.txt` |
| Negative control: append one newline to EVAL_SET.json | verify tool | ❌ detected via file_sha256/file_bytes mismatch, **exit 1**; a re-freeze attempt is refused (**exit 2**) until a new version/approval exists | demonstrated in-session; original restored byte-identical (`sha256sum` = `ab60cabd…`) |

Metrics reproduced at the operating point (identical to the audited baseline):
Hit@5 = 1.000, MRR = 1.000, Recall@5 = 0.970, Precision@5 = 0.860,
answered_rate = 1.000, no_answer_accuracy = 0.8667 (13/15), near-miss leaks =
2 (ONT-khu-C dBm @0.355 threshold-sensitive; doanh-thu-Q4-Hà-Nội @0.512
threshold-robust), ranked_misses = 0. All six gate floors met
(≥0.90 hit/recall/mrr/answered, ≥0.80 precision/no-answer).

## 4. Limits and governance notes (honest scope)

- This freeze covers the **labeled evaluation data + code fingerprint**, not
  production integration. Gate G4 (MCP→Core E2E) remains CLOSED; Work 103
  stays IN DEVELOPMENT. No release/DONE claim.
- `min_score = 0.35` remains the experimental operating value carried into the
  freeze; the experiment evidence proposes recalibration candidates but, per
  Xu's decision, defaults were NOT silently changed here.
- Latency (`avg_latency_ms` ≈ 0.03) is recorded but excluded from exact-match
  verification by design; tiny 8-document corpus makes it directional only.
- CI (GitHub Actions) re-enforces schema + gate on every push to work/103
  paths; the freeze adds the tamper-evidence layer CI does not provide.
- Re-freeze policy: any content change requires bumping EVAL_SET `version`
  and a new approval; then run `freeze_eval_set.py --out
  ../06_EVIDENCE/FROZEN_EVAL_SET_v<N>.json`. Byte-level churn without content
  change still trips `file_sha256`; use `canonical_sha256` for cross-format
  comparison.

## 5. Files produced by this task

```
04_CODE/freeze_eval_set.py                       (new QC tool)
04_CODE/verify_frozen_eval_set.py                (new QC tool)
06_EVIDENCE/FROZEN_EVAL_SET_v2.json              (freeze manifest, FROZEN_IMMUTABLE)
06_EVIDENCE/frozen/FROZEN_EVAL_SET_v2/eval_operating_metrics.json
06_EVIDENCE/frozen/eval_gate_stdout_20261028.txt
06_EVIDENCE/frozen/unit_retrieval_stdout_20261028.txt
06_EVIDENCE/frozen/unit_eval_stdout_20261028.txt
06_EVIDENCE/frozen/verify_stdout_20261028.txt
06_EVIDENCE/QC_FREEZE_AND_EVAL_REPORT_20261028.md (this report)
```

Next owners: Xu reviews and records acceptance of the freeze in the shared
Nhật ký; Qw may independently re-run `verify_frozen_eval_set.py` as a
third-party check; task 03 (controlled improvement) must measure against this
frozen fingerprint, not a drifting copy.
