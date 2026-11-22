# NU BUILD JOURNAL — WORK 092

## 2026-11-22 — One-shot execution and final mirror retest

- Current executor followed the user's ONE-SHOT instruction without pausing for intermediate ACK/approval. Existing NU_ACK is explicitly not proof of an independently dispatched Nu agent.
- Reviewed Work 092 source/evidence through MCP, applied T5/T9/T12 changes, and added task/evidence/permission tests.
- Initial Playwright Chromium run exposed a favicon 404. Added a local data URI favicon and regression assertion; final E2E has zero console/page errors.
- Review found tab close (×) was decorative. Added an accessible close button and logic, prevented closing the final tab, and added static/E2E regression coverage.
- Final tests on Cloud Sandbox mirror reconstructed from MCP read-back: pytest 12/12; Node 14/14; JS syntax checks pass; Playwright+system Chromium 11/11.
- E2E covered tab open/switch/close, URL/Back/Forward/Reload, control handoff, empty task, Search/Browse/Workflow, permissions, evidence provenance, XSS-safe rendering, desktop/mobile overflow and no external page requests/errors.
- Screenshot dimensions: desktop viewport 1920×1080, full page 1920×1833; mobile viewport 390×844, full page 390×2857, scrollWidth=clientWidth=390.
- Distinction: test/browser evidence is mirror-only, not direct Work Sandbox or GitHub Actions. GitHub Actions remains pending until verified run URL/SHA/conclusion/artifact.
- Final disposition at this journal entry: PARTIAL — NOT ACCEPTED; Xu retains acceptance authority.

## GitHub CI verification — 2026-11-22

Branch `work092/one-shot-20261122`, code SHA `dcd75f0a39ca6a1e1b447f92793121c1fb3e2759`; Actions run `44982525770` succeeded. JUnit artifact `work092-pytest-report` ID `14738237995` was downloaded and parsed (12 tests, 0 failures/errors, 0 skipped); Actions log confirms Node 14/14. This does not establish direct Work Sandbox execution. No merge to main; Xu retains acceptance.


## Entry 013 — Verified source sync and current-source GitHub Actions
- **Thời gian:** 2026-11-22 14:06–14:09 (+07:00).
- **Executor:** Manus executor trong phiên hiện tại; không đại diện Nu độc lập, Xu hay Vinh.
- **Phạm vi:** hoàn tất Phương án A trong giới hạn UI/client static TEST_ONLY; không mở Browser Runtime, không chạy service/API, không probe host/port, không sửa Work khác.
- **Source provenance:** mirror `/tmp/work092-ui-mirror-20261122` tại source_root đã ghi trong verification report được tìm lại và tất cả 7 source/test SHA-256 khớp report canonical trước khi copy. `index.html`, `app.js`, `styles.css`, `workflow.js`, `tests/test_static_contract.py`, `tests/workflow.test.js`, `tests/browser_smoke.py` được đồng bộ vào feature branch; SHA giữ nguyên canonical. README được sửa để mô tả trung thực phạm vi và kết quả hiện tại.
- **Local verification trên đúng source snapshot:** `node --check app.js && node --check workflow.js` PASS (2 files); `node --test tests/workflow.test.js` PASS 18/18; `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py` PASS 10/10; `python3 tests/browser_smoke.py` PASS 27/27 qua Playwright/Chromium `file://`, zero HTTP(S) requests. Không chạy test_server.py.
- **Workflow:** root `.github/workflows/work092-pytest.yml` được chuyển sang static-only `tests/test_static_contract.py` + Node `tests/workflow.test.js`; hai bản workflow trong repository giống hệt nhau. Workflow không chạy server fixture, Playwright hoặc Runtime.
- **GitHub:** commit `76549220114b4d20cff78e525343837b7e6c9f4c` được push fast-forward lên `work092/one-shot-20261122`; remote SHA read-back khớp. Không merge/release; `main` không đổi.
- **Actions evidence:** run `44996828261`, URL https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44996828261, event push, head SHA trùng commit, completed SUCCESS. Job steps đều success. JUnit artifact `work092-ui-only-pytest-report`, ID `14744740180`, 663 bytes; download/parse xác nhận 10 tests, 0 failures/errors/skips. Actions log xác nhận Node 18/18. Có warning non-blocking rằng actions v4 đang bị runner force Node.js 24 do Node 20 deprecation.
- **Giới hạn:** đây là static pytest/Node CI, không phải Browser Runtime/E2E; direct Work Sandbox execution vẫn NOT RUN. T6/T8/T17, full accessibility/contrast audit và independent Xu review còn thiếu; chưa có bằng chứng dispatch/ACK Nu độc lập.
- **Evidence:** `02_EVIDENCE/test-results/github-actions-status.json`; report `NU_ACCEPTANCE_REPORT.md`; workflow `02_EVIDENCE/github-workflows/work092-pytest.yml`.
- **Disposition:** Work 092 vẫn **PARTIAL — NOT ACCEPTED**. Xu kiểm tra độc lập, Vinh quyết định cuối. Next: read-after-write xác nhận các hồ sơ canonical đã cập nhật; tiếp tục giữ Runtime BLOCKED.
