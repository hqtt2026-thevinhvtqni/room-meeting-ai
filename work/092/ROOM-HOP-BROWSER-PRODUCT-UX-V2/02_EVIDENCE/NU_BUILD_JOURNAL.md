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


## Entry 014 — Documentation follow-up and branch-tip CI
- **Thời gian:** 2026-11-22 14:13–14:15 (+07:00).
- **Executor:** Manus executor trong phiên hiện tại; không đại diện Nu độc lập, Xu hay Vinh.
- **Commit/push:** commit `12f74b03e8397c5e366f932d40280cfc28e1d168` được push fast-forward trên cùng branch sau source/test commit `76549220114b4d20cff78e525343837b7e6c9f4c`; remote branch tip read-back khớp. Commit follow-up chỉ đổi 5 tệp manifest/README/acceptance report/build journal/status JSON; application logic và workflow không đổi. README nằm trong path filter nên kích hoạt Actions lần nữa.
- **Actions:** run `44997247247`, URL https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44997247247, event `push`, head SHA trùng branch tip, completed SUCCESS. Các bước static pytest, Node contract tests và upload artifact thành công.
- **Artifact:** `work092-ui-only-pytest-report`, ID `14743304960`, 663 bytes; tải về và phân tích JUnit: 10 tests, 0 failures/errors/skips. Actions log xác nhận Node 18/18.
- **Warning:** GitHub runner lặp lại cảnh báo non-blocking về actions/checkout@v4, setup-node@v4, setup-python@v5 và upload-artifact@v4 bị chuyển từ Node.js 20 sang Node.js 24.
- **Phân biệt bằng chứng:** run `44996828261` kiểm tra source/test commit `7654922…`; run `44997247247` kiểm tra docs-bearing branch tip `12f74b0…`. Không suy rộng thành Runtime/E2E. Không chạy service, API, Browser Runtime, host/port probe hay screenshot.
- **Trạng thái/giới hạn:** branch chưa merge/release; T6/T8/T17, full accessibility/contrast audit, Xu independent review và direct Work Sandbox execution vẫn thiếu. Runtime vẫn BLOCKED; Nu independent dispatch/ACK chưa có bằng chứng.
- **Disposition:** Work 092 tiếp tục **PARTIAL — NOT ACCEPTED**; Xu kiểm tra độc lập, Vinh quyết định cuối.


## Entry 015 — TEST_ONLY accessibility, T6/T8/T17, responsive and preview safety review

- **Thời gian:** 2026-11-22 14:46–14:56 (+07:00).
- **Executor:** Manus executor trong phiên hiện tại; không đại diện Nu/Xu. Không có bằng chứng dispatch/ACK Nu.
- **Phạm vi:** chỉ Work 092 feature branch; không chạm Work 91, Core, Runtime hoặc `main`. Không khởi chạy service, không chạy `tests/test_server.py`, không probe host/port, không truy cập website/API/Internet.
- **T6/T8/T17 source review:** canonical `BIEN_BAN_W092.md` có row-level descriptions; không tìm thấy tài liệu đặc tả chi tiết độc lập trong Work tree. Các JSON E2E cũ chứa claims `agent_state: Done`, `PASS`, và URL fixed-port; giữ chúng như archival, không dùng làm evidence cho source TEST_ONLY hiện tại. T6 giữ PARTIAL; T8 human-readable local actions verified; T17 giữ PARTIAL do backend isolation chưa chạy.
- **Fixes:** `server.py` đổi bind từ `0.0.0.0:8787` sang `127.0.0.1` + port `0` (OS ephemeral); chưa chạy server. CSS text palette được nâng cho readability. Browser tablist chuyển thành direct role=tab children; nút Close current nằm ngoài tablist, disabled khi tab cuối/đang chạy và focus được phục hồi. Initial `aria-invalid=false` được khai báo rõ.
- **Test development findings:** static contract đầu tiên bắt comment literal port cũ; bỏ comment cũ. File smoke bắt duplicate Run button do patch markup; xóa duplicate. Review ARIA tree phát hiện wrapper chứa close-button trong tablist chưa đủ chặt; chuyển close control ra ngoài và sửa smoke/audit để chỉ chấp nhận tab-only children. Mọi lỗi trung gian đã sửa trước run cuối.
- **Final commands/results:** `node --check app.js && node --check workflow.js` PASS; `node --test tests/workflow.test.js` PASS 18/18; `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py` PASS 12/12; `python3 tests/browser_smoke.py` PASS 33/33; `python3 tests/accessibility_audit.py` PASS 70/70; `git diff --check` PASS. Browser requests captured: zero HTTP(S)/WebSocket.
- **Responsive evidence:** headless system Chromium + Playwright opened `file://`; CSS viewports desktop 1920×1080, tablet 768×1024, Android-like emulation/touch 390×844. No horizontal overflow. Captures are full-page UI-only (1920×1971, 768×2274, 390×2770). Mobile result is not a physical Android test.
- **Accessibility evidence:** keyboard focus indicator; tab and secondary-tab semantics; Arrow/Home/End transitions; focus restoration; source-name heuristic; ARIA selection/pressed/expanded/busy/progress; visible error/role=alert/invalid/focus; Loading→Ready/Disconnected; reduced-motion duration 0.00001s; computed contrast samples all ≥4.5:1 (lowest 4.71:1). Screen reader/assistive-tech certification NOT RUN.
- **Evidence files:** `02_EVIDENCE/test-results/accessibility-audit.json`; `02_EVIDENCE/test-results/browser-ui-smoke.json`; `02_EVIDENCE/screenshots/ui-only-desktop-1920x1080.png`, `ui-only-tablet-768x1024.png`, `ui-only-android-emulation-390x844.png`; screenshot index updated.
- **CI/Git:** at entry time, previous branch head was `72b50a902a504b12a50270faa909b0bf08c9ae7a`. Old CI run `44997247247`/artifact `14743304960` applies only to SHA `12f74b0…`, not this source. New push/Actions verification remains pending and must be appended with exact returned SHA/run/artifact; no merge.
- **Disposition:** **PARTIAL — NOT ACCEPTED**. Runtime remains BLOCKED; T6/T17, direct Work Sandbox execution, server isolation, physical Android, assistive technology, Nu dispatch/ACK and Xu independent review are NOT RUN or BLOCKED. Next: commit/push feature branch, verify Actions for source SHA, update canonical evidence, hand to Xu without self-acceptance.


## Entry 016 — remote synchronization and source-matched GitHub Actions verification

- **Thời gian:** 2026-11-22 15:00–15:02 (+07:00).
- **Branch:** `work092/one-shot-20261122`; feature branch only, no merge.
- **Source/test commit:** `3de70ffb9d0883bb94d227428601dddcaf70d2e2`, message `work092: complete TEST_ONLY accessibility and responsive review`. Remote `refs/heads/work092/one-shot-20261122` was verified to equal this SHA immediately after push; local checkout was clean.
- **Actions:** [run 45000773196](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/45000773196), event `push`, branch `work092/one-shot-20261122`, exact head SHA above, completed SUCCESS at 2026-11-22T08:00:44Z.
- **JUnit artifact:** `work092-ui-only-pytest-report`, artifact ID `14745910744`, size 731 bytes, not expired. Downloaded and parsed `work092-static-pytest.xml`: **12 tests, 0 failures, 0 errors, 0 skipped**.
- **Node CI:** job log shows `node --test tests/workflow.test.js`, **18 tests, 18 passed, 0 failed, 0 skipped**. GitHub workflow covers static pytest + Node only; no Playwright, HTTP service, `test_server.py` or Runtime.
- **Local source-matched checks:** Node syntax 2 files PASS; Node 18/18; pytest 12/12; file smoke 33/33; accessibility/responsive audit 70/70; 0 HTTP(S)/WebSocket requests, console errors or page errors; `git diff --check` PASS.
- **Current evidence update:** Actions status JSON and manifest/minutes/acceptance/static-site/source README now record source SHA, run/artifact and limits. The following documentation update is a distinct commit and does not reuse this run's SHA.
- **Disposition:** CI/source sync verified; **Work 092 remains PARTIAL — NOT ACCEPTED**, T6/T17 PARTIAL, Runtime BLOCKED. Xu independent review and Vinh final decision are outstanding.
