from __future__ import annotations

import pytest

from room_hop_mcp.browser_agent_adapter.adapter import _configured_port


def test_browser_adapter_port_defaults_to_8787(monkeypatch):
    monkeypatch.delenv("ROOMHOP_BROWSER_ADAPTER_PORT", raising=False)
    assert _configured_port() == 8787


@pytest.mark.parametrize("port", ["8788", "49152", "65535"])
def test_browser_adapter_accepts_configured_port(monkeypatch, port):
    monkeypatch.setenv("ROOMHOP_BROWSER_ADAPTER_PORT", port)
    assert _configured_port() == int(port)


@pytest.mark.parametrize("port", ["", "abc", "0", "-1", "65536"])
def test_browser_adapter_rejects_invalid_port(monkeypatch, port):
    monkeypatch.setenv("ROOMHOP_BROWSER_ADAPTER_PORT", port)
    with pytest.raises(RuntimeError):
        _configured_port()
