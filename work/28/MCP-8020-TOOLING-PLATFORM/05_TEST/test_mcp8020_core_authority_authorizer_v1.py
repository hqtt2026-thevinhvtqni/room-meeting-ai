"""Tests for the Core-authority authorizer bridge (Core vs W12/W13 drift).

Pins the cross-check finding: the execution contract accepts free-form
work ids, Core refuses them; the bridge refuses them first and implements
the adapter's CoreAuthorizer protocol fail-closed. No MCP wiring, no v54
status change, no deployment claim.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution_authority.authority import (
    ExecutionAuthority,
    load_enrolled_identities,
)
from core.execution_authority.store import AppendOnlyRecordStore
from mcp8020_core_authority_authorizer_v1 import (
    CoreAuthorityAuthorizer,
    CoreWorkIdError,
    require_core_canonical_work_id,
)


def build_authority(tmpdir):
    identities = load_enrolled_identities("mcp8020=secret-bridge,other=secret-other")
    works = {
        "W28": {
            "work_name": "TOOLING", "workspace_root": "/w/28",
            "execution_workspace": "/w/28/run", "evidence_root": "/w/28/evidence",
            "allowed_identities": ["mcp8020"],
        }
    }
    store = AppendOnlyRecordStore(str(Path(tmpdir) / "records"))
    return ExecutionAuthority(store=store, enrolled_identities=identities, works=works)


class CanonicalWorkIdTests(unittest.TestCase):
    def test_contract_drift_is_pinned(self):
        # The execution contract module still accepts free-form ids; Core
        # cannot. The drift is real and must be bridged, not ignored.
        from mcp8020_execution_contract_v1 import validate_python_run_request
        ok = validate_python_run_request({
            "work_id": "work28",
            "entry_path": "04_CODE/smoke.py",
            "operation": "RUN_SCRIPT",
            "expected_source_sha256": "a" * 64,
        })
        self.assertEqual(ok["work_id"], "work28")
        with self.assertRaises(CoreWorkIdError):
            require_core_canonical_work_id("work28")

    def test_only_core_canonical_form_passes(self):
        for value in ("W28", "W12", "W13", "W1"):
            self.assertEqual(require_core_canonical_work_id(value), value)
        for bad in ("work28", "28", "w28", "W", "W-28", "W 28", "W28.1", "", None, 28, ["W28"]):
            with self.subTest(value=bad):
                with self.assertRaises(CoreWorkIdError):
                    require_core_canonical_work_id(bad)


class CoreAuthorityAuthorizerTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)
        self.authorizer = CoreAuthorityAuthorizer(authority=self.authority)

    def test_enrolled_allowed_identity_authorized(self):
        self.assertIs(self.authorizer.authorize({"credential": "secret-bridge"}, "W28"), True)

    def test_denials_fail_closed_without_detail(self):
        # wrong credential
        self.assertIs(self.authorizer.authorize({"credential": "wrong"}, "W28"), False)
        # missing credential
        self.assertIs(self.authorizer.authorize({}, "W28"), False)
        self.assertIs(self.authorizer.authorize(None, "W28"), False)
        # enrolled but not allowed for the work
        self.assertIs(self.authorizer.authorize({"credential": "secret-other"}, "W28"), False)
        # unknown canonical work
        self.assertIs(self.authorizer.authorize({"credential": "secret-bridge"}, "W99"), False)

    def test_non_canonical_work_id_refused_before_core(self):
        with self.assertRaises(CoreWorkIdError):
            self.authorizer.authorize({"credential": "secret-bridge"}, "work28")

    def test_constructor_requires_authority_surface(self):
        with self.assertRaises(TypeError):
            CoreAuthorityAuthorizer(authority=object())
        with self.assertRaises(TypeError):
            CoreAuthorityAuthorizer(authority=self.authority, work_id_validator="not-callable")


if __name__ == "__main__":
    unittest.main()
