from __future__ import annotations
from typing import Protocol, Any

class BrowserAdapter(Protocol):
    def execute(self, execution_id: str, ctx: Any, action: dict[str, Any], timeout_seconds: float) -> dict[str, Any]: ...
class GitHubGateway(Protocol):
    def verify_head(self, execution_id: str, ctx: Any, expected_head: str) -> dict[str, Any]: ...
class CIAdapter(Protocol):
    def verify(self, execution_id: str, ctx: Any, commit_sha: str) -> dict[str, Any]: ...

def unavailable(kind: str, execution_id: str) -> dict[str, Any]:
    return {'status':'NOT_CONFIGURED','kind':kind,'execution_id':execution_id,'reason':f'{kind}_adapter_not_injected'}
