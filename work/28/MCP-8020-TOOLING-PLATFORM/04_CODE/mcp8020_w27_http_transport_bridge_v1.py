"""Arity bridge: RuntimeAdapter Transport.execute(payload) ↔ HttpTransport.execute(wc, er)."""
from __future__ import annotations

from typing import Any, Protocol


class TwoArgExecuteTransport(Protocol):
    def execute(
        self,
        work_context: dict[str, Any],
        execution_request: dict[str, Any],
    ) -> dict[str, Any]:
        ...


class TransportBridgeError(TypeError):
    """Raised when payload cannot be safely split for HttpTransport."""


class W27HttpTransportBridge:
    def __init__(self, http_transport: TwoArgExecuteTransport) -> None:
        if not callable(getattr(http_transport, "execute", None)):
            raise TypeError("http_transport must provide execute(...)")
        self._http = http_transport

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise TransportBridgeError("payload must be a dict")
        if "work_context" not in payload or "execution_request" not in payload:
            raise TransportBridgeError(
                "payload must contain work_context and execution_request "
                "(W13 envelope); flat RuntimeAdapter-only payloads are refused"
            )
        work_context = payload["work_context"]
        execution_request = payload["execution_request"]
        if not isinstance(work_context, dict) or not isinstance(execution_request, dict):
            raise TransportBridgeError("work_context and execution_request must be dicts")
        return self._http.execute(work_context, execution_request)


__all__ = ["TransportBridgeError", "W27HttpTransportBridge"]
