# Work 28 - Goi sync co kiem soat W13 (GitHub -> Sandbox) - 2026-10-26

* Soan: Vibe (uy quyen tu chu cua Vinh - "tiep, khong cho")
* Nhanh nguon: work/28-mcp-tooling-platform, head doi soat: 990349fa7619d0a2347b7141eb7d91f9b993bd31
* Muc dich: chuan bi danh muc + blob SHA de Xu/Co dong bo nguon W13 hardened tu nhanh vao Sandbox W13 ma KHONG ghi de mu, dung Evidence First.
* Gioi han: phien nay khong co kenh toi Sandbox MCP 8030 nen chua doi soat duoc chieu nguoc; moi SHA duoi day la blob SHA doc truc tiep tu GitHub API tai head.

## 1. Quy tac sync (bat buoc)

1. Xu/Co doc file qua GitHub API (raw hoac contents API) tai dung SHA ghi duoi day; KHONG lay ban "moi nhat" ma khong ghim SHA.
2. So sanh hash noi dung voi ban hien hanh trong Sandbox truoc khi ghi; chenh lech phai duoc review diff, khong ghi de im lang.
3. Moi ghi de nguon W13 Sandbox can Vinh ACK (nguon canonical), tru file thuan evidence.
4. Sau sync: chay lai offline suite trong moi truong duoc uy quyen; khong khai PASS khi chua co output that.

## 2. Danh muc W13 hardened tren nhanh (blob SHA tai head 990349f)

### execution_host/ (ban da hardening caller-auth)

| File | Blob SHA | Size |
|---|---|---|
| server.py (token gate X-Room-Hop-Execution-Auth, fail-closed) | 87644127a9a2df638b5677758cfc4d0c883b2985 | 9722 |
| wee_bridge.py | 2fb528f7748798312ba5aff610c2ea517b2c0b08 | 5312 |
| host.py | ce6eff2ebf7ebfeb5d61463df859e8b4727f1a37 | 12649 |
| identity.py | 517dbb36bbdbfa3b606a6dec98c82612e12eeefa | 1544 |
| security.py | 4aa20fbc9c5939c49c85222916dc28fb8dd8075b | 4777 |
| work28_core_grant_client.py | 75b28b49a8d2ce7561d722519af293d00fac13aa | 3118 |
| work28_grant.py | 05c082b00a5c38fbdf45950d42211e644f57ed45 | 2879 |
| work28_grant_registry.py | b023a77fabfb9c018e61434504fe9d86d55fd3d3 | 1698 |
| work28_work_id.py (canonical W<number> gate) | 976e16fd7d146405477414709d8f7f9b84910869 | 1026 |
| work28_dispatch.py | 22d5dcd385e301a43fcd0e1c3e901ff2c90abac9 | 4684 |
| work28_execute.py | ecb4fc05332c77983cd244c66d1e838def6c30d2 | 3727 |
| work28_contract.py | 46f7a64dac401de52566741c421087bc8ed67c50 | 6370 |
| work28_bounds.py | b13793dd96a2d5ab74622816e3586943a1493d08 | 2085 |
| work28_evidence.py | 3d2560024b7f08050b0b0ad07a2ce750e5a92a95 | 2013 |
| work28_readback.py | de7ef38b2fcce73e3dcc1ee29d4ff56a60bfc378 | 1489 |
| work28_readiness.py | e2c7a79c037cf4b8026e39bf26ef948e8f346e14 | 1211 |
| work28_audit.py | d3ab1f2bf62e4f632f2c45f710197d6f62f40d5f | 1910 |
| w12_execution_adapter.py | a39bdcd6e07117e1292dbe4f23927e311e59316f | 3702 |
| process_job.py | 85f4866df7710aa2ad0fe1601ae319c470f1718a | 28883 |
| host_run.py | 73ef846748441489cc565da4b837449bb5317e42 | 3803 |
| host_cleanup_bridge.py | 5fd3455e90ec0249051bfb6ac86924b7aec63a02 | 997 |
| models.py | 2488b7c95cf3784fc26eaf677044fe5ab0866420 | 1618 |
| git_adapter.py | 9f869f1b1fa8d64e50a89f71a05da0720bcf5a03 | 2210 |
| adapters.py | 6a84f72cf5b596ceba77ab67a4cc9f9e245a4cda | 654 |
| __init__.py | 70c096c7103b9436fb7f64eee31db08adfd582d4 | 520 |

### core/execution_authority/ (Gate 2)

| File | Blob SHA | Size |
|---|---|---|
| authority.py | bfb052fed0fde69767dd219f17a0b14ae6383560 | 11057 |
| http_server.py | 6363c277ce410d3f5465f449b730199e06e5024c | 8044 |
| store.py | a628dc578c68c05bb875318d1b74528b26f0e4eb | 2731 |
| __init__.py | 3751d01d41a186a38bd0fe39c60c1310c6cd1fcf | 793 |

### 04_CODE + 05_TEST Work 28 (delta evidence 18-21)

| File | Blob SHA | Size |
|---|---|---|
| 04_CODE/mcp8020_core_authority_authorizer_v1.py | 1d8013eb2dfa281ac922638ac45d7d4fff00c005 | 3551 |
| 04_CODE/mcp8020_core_execution_session_v1.py | f95160e245ee11cc8c5abc641ca8f1b736970346 | 3529 |
| 05_TEST/test_mcp8020_core_authority_authorizer_v1.py | c1cc9a3fbc2748a6c83b50dacc2d01b22de76ecf | 4104 |
| 05_TEST/test_mcp8020_core_execution_session_v1.py | 632abd0b5f140bcf249792c9ef1d355af79853a0 | 9232 |
| 05_TEST/test_w13_client_live_authority_e2e_v1.py | aaabbd93dac1185b0ad0fa771a09aea6f3d15f3c | 11127 |
| 05_TEST/test_w13_execute_handler_auth.py | c1e29e2a404ed9187de9b5092e46c68c7d165d64 | 2501 |
| 05_TEST/test_w13_execute_handler_http_boundary.py | 7dd1cbe7ab95861e66ccb421435f6147dcf8eba8 | 6487 |
| 05_TEST/test_w13_execution_auth_config_bootstrap.py | 9d123dd8c6815d41253b2b1cf4ad94a58b11739e | 4905 |
| 05_TEST/test_w13_bridge_execution_token.py | 7b50d5d4d387d097a84fd80c1863cffcde2e5370 | 5403 |
| 05_TEST/test_w13_contract_boundary.py | 064a126ac97421ad810ccf786d01319874432c0b | 5373 |
| 05_TEST/test_mcp8020_w13_core_client_v1.py | 2c1352fefd9938cb3910eb30db91e459cfa75e5e | 8083 |

## 3. Chieu nguoc can mirror len nhanh (Sandbox -> GitHub)

1. 06_EVIDENCE/XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md
2. 06_EVIDENCE/XU_EXECUTION_TOOL_CONTINUATION_JOURNAL_20261025.md

## 4. Trang thai CI

Connector GitHub cua phien nay khong co cong cu liet ke Actions runs nen KHONG tu xac minh lai runs #168-#178; bang chung CI hien dua vao ho so REPO_SIDE_W13_HANDLER_AUTH_HARDENING_20261025.md (sections 7-21) va XU_CI_TEST_EVIDENCE_RECONCILIATION_20261025.md (run 40151686990, commit 9ef3ddb, 201 tests OK). Ai co quyen web can mo lai 2 run nay de chot bang chung doc lap.

## 5. Trang thai

Work 28 giu nguyen ACTIVE / BLOCKED (trusted-environment verification) / NOT RELEASED. Goi sync nay la chuan bi, khong phai bang chung thuc thi moi.
