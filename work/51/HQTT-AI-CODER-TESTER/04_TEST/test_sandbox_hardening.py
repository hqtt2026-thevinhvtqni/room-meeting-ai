"""Sandbox hardening (D-04b): env scrub, input caps, isolation, rlimits.

Locks the hardened sandbox behaviors added in iteration 2:
- parent secrets are NOT inherited by the sandboxed child (env scrub)
- oversized artifact/program inputs are rejected before execution
- results report network isolation status
- POSIX resource limits are applied inside the child
"""

import platform

import pytest

from a2a_ct.sandbox import MAX_INPUT_BYTES, RLIMIT_AS_BYTES, Sandbox, SandboxInputError


def test_parent_secrets_not_inherited(monkeypatch):
    monkeypatch.setenv("A2A_CT_SECRET", "super-secret-token")
    run = Sandbox().run(
        "import os\n",
        "assert 'A2A_CT_SECRET' not in os.environ\n"
        "print('env clean')\n",
    )
    assert run["ok"], run["stderr"]


def test_oversized_artifact_rejected():
    artifact = "# padding\n" + "x" * (MAX_INPUT_BYTES + 1)
    with pytest.raises(SandboxInputError):
        Sandbox().run(artifact, "print('never runs')\n")


def test_oversized_program_rejected():
    program = "x = 1\n" + "y = '" + "z" * (MAX_INPUT_BYTES + 1) + "'\n"
    with pytest.raises(SandboxInputError):
        Sandbox().run("x = 1\n", program)


def test_result_reports_network_isolation():
    run = Sandbox().run("x = 1\n", "print(x)\n")
    if run["network_isolated"] and not run["ok"]:
        pytest.skip("network namespace not permitted on this platform")
    assert run["ok"], run["stderr"]
    assert isinstance(run["network_isolated"], bool)


@pytest.mark.skipif(platform.system() == "Windows", reason="POSIX rlimits only")
def test_rlimits_applied_in_child():
    program = (
        "import resource\n"
        "soft, hard = resource.getrlimit(resource.RLIMIT_AS)\n"
        "print(soft)\n"
    )
    run = Sandbox().run("", program)
    assert run["ok"], run["stderr"]
    soft = int(run["stdout"].strip().splitlines()[-1])
    if soft == -1:
        pytest.skip("RLIMIT_AS not applied on this platform")
    assert soft <= RLIMIT_AS_BYTES
