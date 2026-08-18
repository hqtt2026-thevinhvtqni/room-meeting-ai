import pytest

from core.agent_registry import AgentRegistry, Agent, AgentValidationError


def test_registry_loads_known_agents():
    registry = AgentRegistry()
    ids = {a.id for a in registry.list_agents()}
    assert "xu" in ids
    assert "claude" in ids


def test_get_existing_agent():
    registry = AgentRegistry()
    xu = registry.get("xu")
    assert xu.name == "Xu"
    assert xu.role == "CEO"


def test_get_unknown_agent_raises():
    registry = AgentRegistry()
    with pytest.raises(KeyError):
        registry.get("does_not_exist")


def test_exists():
    registry = AgentRegistry()
    assert registry.exists("claude") is True
    assert registry.exists("nobody") is False


def test_agent_from_dict_missing_required_field():
    with pytest.raises(AgentValidationError):
        Agent.from_dict({"id": "x", "name": "X", "role": "Y"})  # thiếu provider, capabilities


def test_agent_permissions_authority_default_empty_dict():
    # forward-compatible fields phải mặc định rỗng, không None gây lỗi downstream
    agent = Agent.from_dict(
        {
            "id": "test_agent",
            "name": "Test",
            "role": "Tester",
            "provider": "none",
            "capabilities": ["testing"],
        }
    )
    assert agent.permissions == {}
    assert agent.authority == {}
