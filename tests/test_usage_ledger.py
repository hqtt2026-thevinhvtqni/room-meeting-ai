import json
from types import SimpleNamespace

from core import usage_ledger
from core.usage_ledger import extract_usage, new_usage_event, record_usage_event


def test_anthropic_usage_maps_reported_tokens():
    actual = extract_usage("anthropic", {"input_tokens": 12, "output_tokens": 7, "cache_read_input_tokens": 3})
    assert actual["input_tokens"] == 12
    assert actual["output_tokens"] == 7
    assert actual["cached_input_tokens"] == 3
    assert actual["usage_source"] == "provider_reported"


def test_openai_usage_maps_cached_and_reasoning_tokens():
    actual = extract_usage("openai", {
        "prompt_tokens": 10, "completion_tokens": 5,
        "prompt_tokens_details": {"cached_tokens": 4},
        "completion_tokens_details": {"reasoning_tokens": 2},
    })
    assert (actual["input_tokens"], actual["output_tokens"]) == (10, 5)
    assert actual["cached_input_tokens"] == 4
    assert actual["reasoning_tokens"] == 2


def test_groq_usage_maps_prompt_completion_tokens():
    actual = extract_usage("groq", {"prompt_tokens": 9, "completion_tokens": 6})
    assert (actual["input_tokens"], actual["output_tokens"]) == (9, 6)


def test_groq_usage_maps_sdk_nested_objects():
    usage = SimpleNamespace(
        prompt_tokens=9,
        completion_tokens=6,
        prompt_tokens_details=SimpleNamespace(cached_tokens=2),
        completion_tokens_details=SimpleNamespace(reasoning_tokens=3),
    )
    actual = extract_usage("groq", usage)
    assert (actual["input_tokens"], actual["output_tokens"]) == (9, 6)
    assert actual["cached_input_tokens"] == 2
    assert actual["reasoning_tokens"] == 3


def test_google_usage_metadata_maps_token_counts():
    actual = extract_usage("google", {
        "prompt_token_count": 20, "candidates_token_count": 8,
        "cached_content_token_count": 2, "thoughts_token_count": 3,
    })
    assert (actual["input_tokens"], actual["output_tokens"]) == (20, 8)
    assert actual["cached_input_tokens"] == 2
    assert actual["reasoning_tokens"] == 3


def test_missing_usage_remains_null_not_zero():
    actual = extract_usage("openai", None)
    assert actual["usage_source"] == "unavailable"
    assert actual["input_tokens"] is None
    assert actual["output_tokens"] is None


def test_event_is_created_before_recording_and_has_correlation():
    event = new_usage_event(
        provider="groq", model="llama-test", caller="intent_router",
        correlation={"work_id": "104", "task_id": "task-1"},
    )
    assert event["event_id"]
    assert event["occurred_at"]
    assert event["work_id"] == "104"
    assert event["task_id"] == "task-1"
    assert event["meeting_id"] is None


def test_record_writes_one_jsonl_row_and_redacts_unapproved_fields(tmp_path, monkeypatch):
    path = tmp_path / "usage.jsonl"
    monkeypatch.setenv("USAGE_LEDGER_PATH", str(path))
    event = new_usage_event(provider="openai", model="test-model", caller="chat")
    event.update(input_tokens=11, output_tokens=4, usage_source="provider_reported")
    event["prompt"] = "PRIVATE PROMPT MUST NOT BE STORED"
    event["api_key"] = "SECRET"
    record_usage_event(event)
    rows = path.read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1
    row = json.loads(rows[0])
    assert row["input_tokens"] == 11
    assert row["cost_status"] == "unavailable"
    assert row["cost_amount"] is None
    assert "prompt" not in row and "api_key" not in row
    assert "PRIVATE PROMPT" not in rows[0] and "SECRET" not in rows[0]


def test_ledger_write_failure_never_raises(tmp_path, monkeypatch):
    # A directory at the target file path deterministically causes open("a") to fail.
    target = tmp_path / "blocked.jsonl"
    target.mkdir()
    monkeypatch.setenv("USAGE_LEDGER_PATH", str(target))
    failure_path = tmp_path / "failures.log"
    monkeypatch.setenv("USAGE_LEDGER_FAILURES_PATH", str(failure_path))
    record_usage_event(new_usage_event(provider="openai", model="test", caller="test"))
    assert failure_path.exists()
    failure_row = json.loads(failure_path.read_text(encoding="utf-8").splitlines()[0])
    assert failure_row == {"timestamp": failure_row["timestamp"], "count": 1}



def test_size_rotation_indexes_completed_part_file(tmp_path, monkeypatch):
    ledger_path = tmp_path / "usage.jsonl"
    index_path = tmp_path / "index.jsonl"
    monkeypatch.setenv("USAGE_LEDGER_PATH", str(ledger_path))
    monkeypatch.setenv("USAGE_LEDGER_INDEX_PATH", str(index_path))
    monkeypatch.setattr(usage_ledger, "_MAX_FILE_BYTES", 1)

    record_usage_event(new_usage_event(provider="openai", model="test", caller="test"))
    record_usage_event(new_usage_event(provider="openai", model="test", caller="test"))

    rotated = tmp_path / "usage.part2.jsonl"
    assert rotated.exists()
    indexed = [json.loads(line) for line in index_path.read_text(encoding="utf-8").splitlines()]
    assert len(indexed) == 1
    assert indexed[0]["file"] == str(rotated)
    assert indexed[0]["event_count"] == 1
