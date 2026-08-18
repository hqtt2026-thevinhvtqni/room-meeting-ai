# core/identity.py — ROOM HOP — FIX-4
#
# BUILD phase: chua xay Identity Registry / Attestation day du. Chi 1 quy
# tac don gian:
#
#   RUNTIME_IDENTITY = identity THAT duoc gan luc khoi tao process (hardcode
#   trong script hoac tham so dong luc chay - KHONG BAO GIO doc tu noi dung
#   hoi thoai).
#
#   LLM CLAIM != RUNTIME_IDENTITY  ->  UNVERIFIED, ghi log, KHONG cap them
#   quyen gi ca. Moi quyen han van hoan toan dua vao RUNTIME_IDENTITY qua
#   GOV.check() — ham nay chi dung de PHAT HIEN va GHI LOG, khong tung nao
#   thay doi quyen.

from __future__ import annotations

import re

from .governance import GOV, MissionContext

# Cac ten identity da biet trong Capability Matrix — dung de nhan dien claim.
_KNOWN_IDENTITIES = ("vinh", "xu", "claude", "quan_gia", "agent_llama")

_CLAIM_PATTERNS = (
    re.compile(r"\b(?:t[oô]i|m[iì]nh)\s+l[aà]\s+([a-zA-Z_]+)", re.IGNORECASE),
    re.compile(r"\bi\s*am\s+([a-zA-Z_]+)", re.IGNORECASE),
)


def verify_identity_claim(
    runtime_identity: str,
    text: str,
    mission: MissionContext | None = None,
) -> str | None:
    """
    Quet `text` tim cau tu nhan la mot identity da biet. Neu claim khac
    `runtime_identity`, ghi UNVERIFIED vao audit log va tra ve chuoi canh
    bao (de caller in ra cho nguoi dung, KHONG de cap quyen).

    Tra ve None neu khong co claim nao dang ngo vuc.
    """
    if not text:
        return None

    runtime_identity = (runtime_identity or "agent_llama").strip().lower()

    for pattern in _CLAIM_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        claimed = m.group(1).strip().lower()
        if claimed in _KNOWN_IDENTITIES and claimed != runtime_identity:
            warning = (
                f"UNVERIFIED: claimed_identity='{claimed}' != "
                f"runtime_identity='{runtime_identity}'. Khong cap them quyen."
            )
            GOV.audit(
                runtime_identity,
                "IDENTITY_CLAIM",
                "-",
                warning,
                mission or MissionContext(name="identity_check"),
            )
            return warning
    return None
