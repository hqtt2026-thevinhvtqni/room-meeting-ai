import pytest

from work05_drive_factory import (
    DRIVE_FILE_SCOPE,
    DriveFactoryError,
    build_connection_bound_drive_adapter,
    build_user_drive_adapter,
)


class FakeCredentials:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class FakeManager:
    def __init__(self, credential):
        self.credential = credential
        self.calls = []

    def credential_for_operation(self, room_id, user_id, connection_id):
        self.calls.append((room_id, user_id, connection_id))
        if (room_id, user_id) != ("room-a", "user-a"):
            raise PermissionError("not owner")
        return self.credential


def test_factory_builds_drive_v3_without_sdk_managed_refresh_token():
    credential = {
        "access_token": "access-token",
        "refresh_token": "refresh-token",
        "scopes": [DRIVE_FILE_SCOPE],
    }
    seen = {}

    def google_build(name, version, **kwargs):
        seen["build"] = (name, version, kwargs)
        return object()

    def adapter_factory(service, *, parent_id):
        seen["adapter"] = (service, parent_id)
        return "adapter"

    result = build_user_drive_adapter(
        credential,
        client_id="client-id",
        client_secret="runtime-secret",
        parent_id="roomhop-folder",
        adapter_factory=adapter_factory,
        credentials_factory=FakeCredentials,
        google_build=google_build,
    )

    assert result == "adapter"
    assert seen["build"][0:2] == ("drive", "v3")
    sdk_credentials = seen["build"][2]["credentials"]
    assert sdk_credentials.kwargs["token"] == "access-token"
    assert "refresh_token" not in sdk_credentials.kwargs
    assert sdk_credentials.kwargs["client_secret"] == "runtime-secret"
    assert seen["adapter"][1] == "roomhop-folder"


def test_connection_bound_factory_resolves_exact_user_and_work_credential():
    manager = FakeManager({
        "access_token": "a",
        "refresh_token": "r",
        "scopes": [DRIVE_FILE_SCOPE],
    })
    result = build_connection_bound_drive_adapter(
        manager, "room-a", "user-a", "connection-a",
        client_id="id", client_secret="secret", parent_id="folder",
        adapter_factory=lambda service, *, parent_id: (service, parent_id),
        credentials_factory=FakeCredentials,
        google_build=lambda *args, **kwargs: "drive-service",
    )
    assert result == ("drive-service", "folder")
    assert manager.calls == [("room-a", "user-a", "connection-a")]


def test_connection_bound_factory_denies_other_user_or_work():
    manager = FakeManager({"access_token": "a", "scopes": [DRIVE_FILE_SCOPE]})
    with pytest.raises(DriveFactoryError, match="not authorized"):
        build_connection_bound_drive_adapter(
            manager, "room-b", "user-b", "connection-a",
            client_id="id", client_secret="secret", parent_id="folder",
            adapter_factory=lambda *a, **k: None,
            credentials_factory=FakeCredentials,
            google_build=lambda *a, **k: None,
        )


def test_factory_rejects_missing_drive_file_scope():
    with pytest.raises(DriveFactoryError, match="drive.file"):
        build_user_drive_adapter(
            {"access_token": "a", "scopes": ["openid", "email"]},
            client_id="id", client_secret="secret", parent_id="folder",
            adapter_factory=lambda *a, **k: None,
            credentials_factory=FakeCredentials,
            google_build=lambda *a, **k: None,
        )
