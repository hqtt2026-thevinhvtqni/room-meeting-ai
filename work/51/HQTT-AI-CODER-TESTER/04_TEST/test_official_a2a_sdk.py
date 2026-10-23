"""Independent interoperability test against the official A2A Python SDK 1.2.3."""

import asyncio
import json

import httpx
from jwt.api_jwk import PyJWKSet
from jwt.exceptions import PyJWKError

from a2a.client import ClientConfig, ClientFactory
from a2a.client.card_resolver import parse_agent_card
from a2a.types import (
    CancelTaskRequest,
    GetTaskRequest,
    Message,
    Part,
    Role,
    SendMessageRequest,
    TaskState,
    TaskNotCancelableError,
    UnsupportedOperationError,
)
from a2a.utils.signing import InvalidSignaturesError, create_signature_verifier

from a2a_ct.a2a import A2AServer
from a2a_ct.coder_agent import CoderBackend
from a2a_ct.contract import make_demo_contract


def test_official_a2a_sdk_jsonrpc_roundtrip():
    server = A2AServer(CoderBackend())
    server.start()

    async def exercise():
        base_url = server.base_url.rstrip("/")
        trusted_jwks_url = f"{base_url}/.well-known/jwks.json"
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(trusted_jwks_url)
            response.raise_for_status()
            jwks = PyJWKSet.from_dict(response.json())

        def trusted_key_provider(kid, jku):
            # Never trust the JKU just because the unverified card names it.
            if jku != trusted_jwks_url or kid != "work51-ephemeral-card-key-1":
                raise PyJWKError("untrusted Agent Card signing key")
            return jwks[kid].key

        verifier = create_signature_verifier(
            key_provider=trusted_key_provider,
            algorithms=["ES256"],
        )
        client = await ClientFactory(ClientConfig(streaming=False)).create_from_url(
            server.base_url,
            signature_verifier=verifier,
        )
        try:
            brief = make_demo_contract(coder_mode="correct").coder_brief()
            request = SendMessageRequest(
                message=Message(
                    message_id="official-sdk-message-1",
                    role=Role.ROLE_USER,
                    parts=[Part(text=json.dumps(brief, ensure_ascii=False))],
                )
            )
            responses = [event async for event in client.send_message(request)]
            assert len(responses) == 1
            assert responses[0].HasField("task")
            task = responses[0].task
            assert task.status.state == TaskState.TASK_STATE_COMPLETED
            assert task.artifacts
            assert "def sum_digits" in task.artifacts[0].parts[0].text

            fetched = await client.get_task(GetTaskRequest(id=task.id))
            assert fetched.id == task.id
            assert fetched.status.state == TaskState.TASK_STATE_COMPLETED

            # Official A2A rejects cancellation/continuation once a task is terminal.
            try:
                await client.cancel_task(CancelTaskRequest(id=task.id))
            except TaskNotCancelableError:
                pass
            else:
                raise AssertionError("official CancelTask accepted a terminal task")

            continuation = SendMessageRequest(
                message=Message(
                    message_id="official-sdk-message-2",
                    task_id=task.id,
                    role=Role.ROLE_USER,
                    parts=[Part(text=json.dumps(brief, ensure_ascii=False))],
                )
            )
            try:
                async for _ in client.send_message(continuation):
                    pass
            except UnsupportedOperationError:
                pass
            else:
                raise AssertionError("official SendMessage accepted a terminal task")

            # A changed signed field must be rejected by the official verifier.
            async with httpx.AsyncClient() as http_client:
                raw = await http_client.get(
                    f"{base_url}/.well-known/agent-card.json"
                )
                raw.raise_for_status()
                tampered = parse_agent_card(raw.json())
            tampered.description = "tampered after signing"
            try:
                verifier(tampered)
            except InvalidSignaturesError:
                pass
            else:
                raise AssertionError("tampered Agent Card unexpectedly verified")
        finally:
            await client.close()

    try:
        asyncio.run(exercise())
    finally:
        server.stop()
