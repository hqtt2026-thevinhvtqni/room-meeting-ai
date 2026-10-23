"""Independent interoperability test against the official A2A Python SDK 1.2.3."""

import asyncio
import json

from a2a.client import ClientConfig, ClientFactory
from a2a.types import (
    CancelTaskRequest,
    GetTaskRequest,
    Message,
    Part,
    Role,
    SendMessageRequest,
    TaskState,
)

from a2a_ct.a2a import A2AServer
from a2a_ct.coder_agent import CoderBackend
from a2a_ct.contract import make_demo_contract


def test_official_a2a_sdk_jsonrpc_roundtrip():
    server = A2AServer(CoderBackend())
    server.start()

    async def exercise():
        client = await ClientFactory(ClientConfig(streaming=False)).create_from_url(
            server.base_url
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

            canceled = await client.cancel_task(CancelTaskRequest(id=task.id))
            # A completed task is terminal; cancel is a no-op, per Work 51 contract.
            assert canceled.status.state == TaskState.TASK_STATE_COMPLETED
        finally:
            await client.close()

    try:
        asyncio.run(exercise())
    finally:
        server.stop()
