"""PersistentTaskStore (D-08b): task state must survive restarts.

PLAN P3 requires task state after restart. These tests prove the
persistent store round-trips task state through a JSON file with atomic
rename, and that continuation/idempotency work across a simulated restart.
"""

import json

import pytest

from a2a_ct.a2a import LocalClient
from a2a_ct.coder_agent import CoderBackend
from a2a_ct.contract import make_demo_contract
from a2a_ct.task_store import PersistentTaskStore, TaskStoreError


def _client(tmp_path, name="tasks.json"):
    backend = CoderBackend(PersistentTaskStore(tmp_path / name))
    return LocalClient(backend), tmp_path / name


def test_store_survives_restart(tmp_path):
    client, path = _client(tmp_path)
    first = client.send(make_demo_contract().coder_brief())
    # Simulated restart: a brand-new store over the same file.
    resurrected = PersistentTaskStore(path)
    task = resurrected.get(first["id"])
    assert task is not None
    assert task["state"] == "completed"
    assert task["metadata"]["coder"]["version"] == 1


def test_continuation_survives_restart(tmp_path):
    client, path = _client(tmp_path)
    brief = make_demo_contract(coder_mode="seeded_bug").coder_brief()
    first = client.send(brief)
    # Restart: new backend + client on the same persistent file.
    backend2 = CoderBackend(PersistentTaskStore(path))
    client2 = LocalClient(backend2)
    feedback = dict(brief)
    feedback["kind"] = "feedback"
    feedback["round"] = 1
    second = client2.send(feedback, task_id=first["id"])
    assert second["id"] == first["id"]
    assert second["artifacts"][0]["metadata"]["version"] == 2


def test_store_file_is_valid_json_object(tmp_path):
    client, path = _client(tmp_path)
    client.send(make_demo_contract().coder_brief())
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict) and len(data) == 1


def test_reload_picks_up_external_changes(tmp_path):
    client, path = _client(tmp_path)
    first = client.send(make_demo_contract().coder_brief())
    store = PersistentTaskStore(path)
    external = json.loads(path.read_text(encoding="utf-8"))
    external[first["id"]]["metadata"]["touched"] = True
    path.write_text(json.dumps(external), encoding="utf-8")
    store.reload()
    assert store.get(first["id"])["metadata"]["touched"] is True


def test_corrupt_file_rejected(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("this is { not json", encoding="utf-8")
    with pytest.raises(TaskStoreError):
        PersistentTaskStore(path)


def test_entry_id_mismatch_rejected(tmp_path):
    path = tmp_path / "mismatch.json"
    path.write_text(json.dumps({"t-1": {"id": "t-2", "state": "completed"}}),
                    encoding="utf-8")
    with pytest.raises(TaskStoreError):
        PersistentTaskStore(path)
