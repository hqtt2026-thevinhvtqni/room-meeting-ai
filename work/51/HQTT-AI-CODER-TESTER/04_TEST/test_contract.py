"""G1 Contract gate: valid contracts pass, malformed ones are rejected."""

import pytest

from a2a_ct.contract import ContractError, WorkContract, make_demo_contract


def test_valid_contract_passes():
    contract = make_demo_contract()
    contract.validate()  # must not raise
    assert contract.coder_mode == "correct"
    assert len(contract.acceptance_programs) == 3


def test_missing_objective_rejected():
    contract = make_demo_contract()
    contract.objective = "   "
    with pytest.raises(ContractError, match="objective"):
        contract.validate()


def test_bad_signature_rejected():
    contract = make_demo_contract()
    contract.function_signature = "sum_digits(s)"
    with pytest.raises(ContractError, match="function_signature"):
        contract.validate()


def test_unsafe_filename_rejected():
    contract = make_demo_contract()
    contract.artifact_filename = "../evil.py"
    with pytest.raises(ContractError, match="artifact_filename"):
        contract.validate()


def test_no_acceptance_programs_rejected():
    contract = make_demo_contract()
    contract.acceptance_programs = []
    with pytest.raises(ContractError, match="acceptance program"):
        contract.validate()


def test_bad_max_fix_rounds_rejected():
    contract = make_demo_contract()
    contract.max_fix_rounds = 9
    with pytest.raises(ContractError, match="max_fix_rounds"):
        contract.validate()


def test_coder_brief_hides_acceptance_programs():
    brief = make_demo_contract().coder_brief()
    assert "acceptance_programs" not in brief
    assert "solution_bodies" in brief


def test_from_dict_rejects_missing_fields():
    with pytest.raises(ContractError, match="missing required fields"):
        WorkContract.from_dict({"contract_id": "x"})


def test_from_dict_rejects_non_object():
    with pytest.raises(ContractError):
        WorkContract.from_dict(["not", "a", "dict"])


def test_roundtrip_to_dict_from_dict():
    contract = make_demo_contract(coder_mode="seeded_bug")
    clone = WorkContract.from_dict(contract.to_dict())
    assert clone.to_dict() == contract.to_dict()
