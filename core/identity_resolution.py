"""
Identity Resolution — ROOM HOP v0.2.1 (GOVERNANCE RULE)

Đây là tầng "Identity Resolution" trong Authorization Flow đã FINAL_ACCEPTED
(ROOM_HOP_LIFECYCLE_v0.2.1.md):

    JOIN_REQUEST -> Identity Resolution -> Meeting Policy Check -> Meeting Manager -> JOIN_ACCEPTED

Nhiệm vụ DUY NHẤT ở bước này: cho 1 identity_id, xác định:
  1. Đây là human_principal hay ai_agent? (tra 2 Registry TÁCH BIỆT)
  2. registry_check tương ứng — CHỈ dùng đúng 2 giá trị theo quy ước đã khóa:
       human_principal -> NOT_APPLICABLE
       ai_agent        -> REQUIRED_PASS (tìm thấy) / REQUIRED_FAIL (không tìm thấy)
     KHÔNG dùng "SKIPPED" (dễ hiểu nhầm là "không cần kiểm tra gì").

CHƯA làm ở bước này (đúng "Thứ tự triển khai (KHÔNG ĐƯỢC ĐẢO)"):
  - Meeting Policy Check (identity hợp lệ có được vào MEETING cụ thể nào không)
  - JOIN_ACCEPTED / JOIN_REJECTED (việc của MeetingManager)
  - Ghi Evidence 5 nhóm đầy đủ (việc của Secretary, khi được nối vào luồng JOIN)

Registry KHÔNG phải cơ quan cấp quyền tham gia Meeting — nó chỉ trả lời
"identity này có hợp lệ không?". resolve_identity() dừng lại đúng ở câu hỏi đó.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from core.agent_registry import AgentRegistry
from core.principal_registry import PrincipalRegistry

IdentityType = Literal["human_principal", "ai_agent", "unresolved"]
RegistryCheck = Literal["NOT_APPLICABLE", "REQUIRED_PASS", "REQUIRED_FAIL"]


@dataclass(frozen=True)
class IdentityResolution:
    identity_id: str
    identity_type: IdentityType
    registry_check: RegistryCheck
    # Registry nào đã trả lời (để trace/audit) — "principal_registry",
    # "agent_registry", hoặc None nếu unresolved (không có trong registry nào).
    resolved_via: Optional[str]

    @property
    def is_resolved(self) -> bool:
        return self.identity_type != "unresolved"


def resolve_identity(
    identity_id: str,
    principal_registry: PrincipalRegistry | None = None,
    agent_registry: AgentRegistry | None = None,
) -> IdentityResolution:
    """
    Tra identity_id lần lượt qua Principal Registry rồi Agent Registry.
    KHÔNG bao giờ vừa là human_principal vừa là ai_agent — 2 Registry độc lập,
    ai đăng ký ở đâu thì thuộc về đó. Nếu trùng ở cả 2 (lỗi cấu hình), ưu tiên
    Principal Registry và đây là điều nên được phát hiện thủ công (không che
    giấu bằng cách tự động chọn).
    """
    principal_registry = principal_registry or PrincipalRegistry()
    agent_registry = agent_registry or AgentRegistry()

    if principal_registry.exists(identity_id):
        return IdentityResolution(
            identity_id=identity_id,
            identity_type="human_principal",
            registry_check="NOT_APPLICABLE",
            resolved_via="principal_registry",
        )

    if agent_registry.exists(identity_id):
        return IdentityResolution(
            identity_id=identity_id,
            identity_type="ai_agent",
            registry_check="REQUIRED_PASS",
            resolved_via="agent_registry",
        )

    return IdentityResolution(
        identity_id=identity_id,
        identity_type="unresolved",
        registry_check="REQUIRED_FAIL",
        resolved_via=None,
    )
