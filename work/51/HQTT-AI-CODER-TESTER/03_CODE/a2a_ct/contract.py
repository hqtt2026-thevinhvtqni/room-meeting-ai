"""WorkContract — schema v work51/v1.

Opacity rule (charter §5.5): the Coder never receives acceptance programs.
- coder_brief()  -> what the Coder may see.
- tester_brief() -> acceptance programs go to the Tester only.

The contract is the single source of acceptance criteria. Malformed
contracts are rejected at construction time (G1 Contract gate).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

SCHEMA_VERSION = "work51/v1"

_CODER_MODES = ("correct", "seeded_bug", "always_bug")
_TESTER_MODES = ("normal", "strip_evidence")

_SAFE_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*\.py$")


class ContractError(Exception):
    """Raised when a WorkContract is malformed."""


@dataclass
class WorkContract:
    contract_id: str
    objective: str
    function_signature: str
    artifact_filename: str
    solution_bodies: dict[str, str]          # {"correct": py-code, "buggy": py-code}
    acceptance_programs: list[str]           # tester-only; python source using the function
    max_fix_rounds: int = 2
    sandbox_timeout_s: float = 10.0
    coder_mode: str = "correct"               # correct | seeded_bug | always_bug
    tester_mode: str = "normal"               # normal | strip_evidence (fault injection)
    schema_version: str = SCHEMA_VERSION
    created_by: str = "vinh"

    def validate(self) -> None:
        errors: list[str] = []
        if not self.contract_id or not self.contract_id.strip():
            errors.append("contract_id is required")
        if not self.objective or not self.objective.strip():
            errors.append("objective is required")
        if not self.function_signature.strip().startswith("def "):
            errors.append("function_signature must start with 'def '")
        if not _SAFE_FILENAME.match(self.artifact_filename or ""):
            errors.append("artifact_filename must be a safe .py filename")
        bodies = self.solution_bodies or {}
        for key in ("correct", "buggy"):
            if not (isinstance(bodies.get(key), str) and bodies[key].strip()):
                errors.append(f"solution_bodies[{key!r}] is required")
        if not self.acceptance_programs or not all(
            isinstance(p, str) and p.strip() for p in self.acceptance_programs
        ):
            errors.append("at least one non-empty acceptance program is required")
        if not isinstance(self.max_fix_rounds, int) or not 0 <= self.max_fix_rounds <= 5:
            errors.append("max_fix_rounds must be an int in [0, 5]")
        if not isinstance(self.sandbox_timeout_s, (int, float)) or self.sandbox_timeout_s <= 0:
            errors.append("sandbox_timeout_s must be > 0")
        if self.coder_mode not in _CODER_MODES:
            errors.append(f"coder_mode must be one of {_CODER_MODES}")
        if self.tester_mode not in _TESTER_MODES:
            errors.append(f"tester_mode must be one of {_TESTER_MODES}")
        if errors:
            raise ContractError("; ".join(errors))

    # -- views --------------------------------------------------------------

    def coder_brief(self) -> dict:
        """What the Coder Agent is allowed to see. No acceptance programs."""
        return {
            "kind": "brief",
            "contract_id": self.contract_id,
            "objective": self.objective,
            "function_signature": self.function_signature,
            "artifact_filename": self.artifact_filename,
            "coder_mode": self.coder_mode,
            "solution_bodies": {
                "correct": self.solution_bodies["correct"],
                "buggy": self.solution_bodies["buggy"],
            },
            "max_fix_rounds": self.max_fix_rounds,
        }

    def tester_brief(self) -> dict:
        """Acceptance programs are Tester-only input."""
        return {
            "kind": "verify",
            "contract_id": self.contract_id,
            "acceptance_programs": list(self.acceptance_programs),
            "sandbox_timeout_s": self.sandbox_timeout_s,
            "tester_mode": self.tester_mode,
        }

    # -- serialization -------------------------------------------------------

    def to_dict(self) -> dict:
        self.validate()
        return {
            "schema_version": self.schema_version,
            "contract_id": self.contract_id,
            "objective": self.objective,
            "function_signature": self.function_signature,
            "artifact_filename": self.artifact_filename,
            "solution_bodies": dict(self.solution_bodies),
            "acceptance_programs": list(self.acceptance_programs),
            "max_fix_rounds": self.max_fix_rounds,
            "sandbox_timeout_s": self.sandbox_timeout_s,
            "coder_mode": self.coder_mode,
            "tester_mode": self.tester_mode,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkContract":
        if not isinstance(data, dict):
            raise ContractError("contract payload must be a JSON object")
        required = (
            "contract_id", "objective", "function_signature", "artifact_filename",
            "solution_bodies", "acceptance_programs",
        )
        missing = [k for k in required if k not in data]
        if missing:
            raise ContractError(f"missing required fields: {', '.join(missing)}")
        contract = cls(
            contract_id=data.get("contract_id") or "",
            objective=data.get("objective") or "",
            function_signature=data.get("function_signature") or "",
            artifact_filename=data.get("artifact_filename") or "",
            solution_bodies=data.get("solution_bodies") or {},
            acceptance_programs=data.get("acceptance_programs") or [],
            max_fix_rounds=data.get("max_fix_rounds", 2),
            sandbox_timeout_s=data.get("sandbox_timeout_s", 10.0),
            coder_mode=data.get("coder_mode", "correct"),
            tester_mode=data.get("tester_mode", "normal"),
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            created_by=data.get("created_by", "vinh"),
        )
        contract.validate()
        return contract


def make_demo_contract(coder_mode: str = "correct", tester_mode: str = "normal",
                       contract_id: str = "WORK51-DEMO-001") -> WorkContract:
    """Demo contract used by run_demo.py and the test suite.

    The Coder Agent must produce an artifact implementing:
        sum_digits(s: str) -> int   # sum of decimal digits in s
    Acceptance programs import/use the artifact function; they are never
    sent to the Coder.
    """
    return WorkContract(
        contract_id=contract_id,
        objective="Implement sum_digits(s) that returns the sum of decimal digits in s.",
        function_signature="def sum_digits(s: str) -> int",
        artifact_filename="artifact_sum_digits.py",
        solution_bodies={
            "correct": "return sum(int(ch) for ch in s if ch.isdigit())",
            "buggy": "return len(s)",
        },
        acceptance_programs=[
            "assert sum_digits('a1b2c3') == 6, 'expected 6, got %r' % sum_digits('a1b2c3')",
            "assert sum_digits('') == 0, 'expected 0'",
            "assert sum_digits('99x') == 18, 'expected 18'",
        ],
        coder_mode=coder_mode,
        tester_mode=tester_mode,
    )
