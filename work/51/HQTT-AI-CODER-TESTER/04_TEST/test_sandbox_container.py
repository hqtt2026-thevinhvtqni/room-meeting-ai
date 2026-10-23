"""Container sandbox profile (D-04c): docker isolation gates.

Automatically skipped on hosts without Docker (developer laptops); runs
for real on CI runners where Docker is available.
"""

import pytest

from a2a_ct.sandbox import MAX_INPUT_BYTES, SandboxInputError
from a2a_ct.sandbox_container import ContainerSandbox


@pytest.fixture(scope="module")
def container():
    sb = ContainerSandbox()
    if not sb.available():
        pytest.skip("Docker not available on this host")
    return sb


def test_container_runs_program(container):
    run = container.run("x = 1\n", "print(x + 1)\n")
    assert run["ok"], run["stderr"]
    assert run["stdout"].strip() == "2"
    assert run["engine"] == "docker"
    assert run["network_isolated"] is True


def test_container_has_no_network(container):
    program = (
        "import socket\n"
        "try:\n"
        "    socket.create_connection(('example.com', 80), timeout=5)\n"
        "    print('LEAK')\n"
        "except OSError:\n"
        "    print('blocked')\n"
    )
    run = container.run("import socket\n", program)
    assert run["ok"], run["stderr"]
    assert "blocked" in run["stdout"]
    assert "LEAK" not in run["stdout"]


def test_container_does_not_inherit_host_env(container, monkeypatch):
    monkeypatch.setenv("A2A_CT_SECRET", "super-secret-token")
    program = (
        "import os\n"
        "assert 'A2A_CT_SECRET' not in os.environ, 'secret leaked into container'\n"
        "print('env clean')\n"
    )
    run = container.run("import os\n", program)
    assert run["ok"], run["stderr"]


def test_container_input_cap_unchanged(container):
    artifact = "# padding\n" + "x" * (MAX_INPUT_BYTES + 1)
    with pytest.raises(SandboxInputError):
        container.run(artifact, "print('never runs')\n")
