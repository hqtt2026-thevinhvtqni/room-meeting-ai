"""Dashboard projection contract validation using JSON Schema Draft 2020-12."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

WORK_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = WORK_ROOT / "DASHBOARD"


def load_dashboard():
    schema = json.loads((DASHBOARD / "PRODUCT_STATUS.schema.json").read_text(encoding="utf-8"))
    data = json.loads((DASHBOARD / "PRODUCT_STATUS.json").read_text(encoding="utf-8"))
    return schema, data


def test_dashboard_product_status_matches_json_schema():
    schema, data = load_dashboard()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    assert not errors, "\\n".join(
        f"{list(error.path)}: {error.message}" for error in errors
    )


def test_dashboard_keeps_local_snapshot_and_blocked_gates_explicit():
    _, data = load_dashboard()
    assert data["source_mode"] == "local_snapshot"
    assert data["work_entry"]["status"] == "BLOCKED"
    gates = {item["gate_id"]: item["status"] for item in data["work_entry"]["gates"]}
    assert gates["WE-G4"] == "BLOCKED"
    assert gates["WE-G5"] == "BLOCKED"
    packages = {item["wp_id"]: item["status"] for item in data["work_packages"]}
    assert packages["WP-76-07"].startswith("BLOCKED")
