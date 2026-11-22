"""Static contract checks; these do not simulate or certify a real browser."""
import json
from pathlib import Path

import server

ROOT = Path(server.ROOT)


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_routes_json_has_expected_shape():
    routes = json.loads(read("manus-routes.json"))
    assert isinstance(routes.get("routes"), list)
    assert routes["routes"]
    assert all(set(route) >= {"path", "title"} for route in routes["routes"])


def test_html_uses_only_local_assets_and_states_test_boundary():
    html = read("index.html")
    assert 'href="styles.css"' in html
    assert 'rel="icon" href="data:,"' in html
    assert 'src="workflow.js"' in html and 'src="app.js"' in html
    assert html.index('src="workflow.js"') < html.index('src="app.js"')
    assert 'id="runtimeBadge">DISCONNECTED' in html
    assert "TEST_ONLY UI" in html and "NO NETWORK" in html
    assert "NO REAL CHROMIUM" in html and "NO EXTERNAL API" in html


def test_primary_product_controls_and_reset_exist():
    html = read("index.html")
    for element_id in ("tabs", "newTabBtn", "urlInput", "backBtn", "forwardBtn", "reloadBtn",
                       "taskInput", "taskError", "taskEcho", "runBtn", "resetBtn", "controlBtn",
                       "timeline", "evidence", "passBox", "permissionFeedback"):
        assert f'id="{element_id}"' in html, f"Missing UI contract element: {element_id}"


def test_browser_tabs_and_secondary_panels_have_keyboard_semantics():
    html = read("index.html")
    app = read("app.js")
    assert 'id="tabs" class="tabs" role="tablist"' in html
    assert "select.setAttribute('role', 'tab')" in app
    assert "select.setAttribute('aria-selected', String(selected))" in app
    assert "select.setAttribute('aria-controls', 'browserContent')" in app
    assert "ArrowRight" in app and "ArrowLeft" in app
    assert "event.key === 'Home'" in app and "event.key === 'End'" in app
    assert 'role="tablist" aria-label="Additional TEST_ONLY information"' in html
    assert 'role="tabpanel" aria-labelledby="demoTab"' in html
    assert "selectInfoTab" in app
    assert 'id="closeTabBtn"' in html and "closeCurrentTab" in app
    assert "state.tabs.length <= 1" in app


def test_runtime_is_explicitly_disconnected_and_only_fixture_states_are_possible():
    html = read("index.html")
    app = read("app.js")
    workflow = read("workflow.js")
    assert "Connected · MOCK" not in html + app
    assert "Working · MOCK" not in html + app
    assert "Give control to Agent" not in html + app
    assert "No real agent or browser session" in html + app
    assert "getDemoUiState" in app and "runtime: 'DISCONNECTED'" in workflow
    assert "TEST_ONLY_RUNNING" in workflow and "TEST_ONLY_COMPLETE" in workflow
    assert "canRun: !running && !held" in workflow


def test_permissions_are_local_test_flags_and_accessibly_named():
    html = read("index.html")
    app = read("app.js")
    assert "không cấp quyền trình duyệt" in html
    assert 'aria-pressed="false"' in html
    assert "Enabled for this test only" in app
    assert "aria-label', `${granted ? 'Disable' : 'Enable'} TEST_ONLY permission:" in app
    assert "Workflow.missingPermissions" in app
    assert "state.permissions[key] = !state.permissions[key]" in app


def test_evidence_is_simulated_and_never_claims_real_artifact():
    html = read("index.html")
    app = read("app.js")
    workflow = read("workflow.js")
    assert "SIMULATED EVIDENCE" in html
    assert "No screenshot file was created" in app
    assert "Workflow.buildMockEvidence" in app
    assert "TEST_ONLY DEMO COMPLETE" in html
    assert "artifact: null" in workflow
    assert "PASS</strong>" not in html


def test_styles_include_responsive_focus_and_reduced_motion_support():
    css = read("styles.css")
    assert "@media(max-width:480px)" in css
    assert "@media(max-width:780px)" in css
    assert ".tab:focus-visible" in css
    assert "@media(prefers-reduced-motion:reduce)" in css
    assert "min-height:38px" in css


def test_task_and_status_regions_have_accessible_descriptions():
    html = read("index.html")
    assert 'aria-describedby="taskHelp taskError"' in html
    assert 'id="runtimeConnection">DISCONNECTED</strong>' in html
    assert 'id="browserContent" class="browser-viewport" role="tabpanel"' in html
    assert 'role="progressbar" aria-label="TEST_ONLY script progress"' in html
    assert 'role="alert" aria-live="assertive"' in html


def test_no_external_script_or_runtime_client_is_declared():
    html = read("index.html")
    assert 'src="http' not in html
    assert 'href="http' not in html
    assert "fetch(" not in read("app.js")
    assert "XMLHttpRequest" not in read("app.js")
    assert "WebSocket" not in read("app.js")


def test_optional_preview_server_is_loopback_only_and_uses_an_os_assigned_port():
    server_source = read("server.py")
    assert 'PREVIEW_HOST = "127.0.0.1"' in server_source
    assert "PREVIEW_PORT = 0" in server_source
    assert "0.0.0.0" not in server_source
    assert "8787" not in server_source
    assert "httpd.server_address" in server_source


def test_browser_tablist_contains_only_tabs_and_has_external_close_control():
    html = read("index.html")
    app = read("app.js")
    assert "select.setAttribute('role', 'tab')" in app
    assert "select.setAttribute('aria-controls', 'browserContent')" in app
    assert "tabList.append(select)" in app
    assert 'id="closeTabBtn"' in html
    assert "closeButton.disabled = state.tabs.length <= 1 || state.running" in app
    assert "closeCurrentTab" in app
