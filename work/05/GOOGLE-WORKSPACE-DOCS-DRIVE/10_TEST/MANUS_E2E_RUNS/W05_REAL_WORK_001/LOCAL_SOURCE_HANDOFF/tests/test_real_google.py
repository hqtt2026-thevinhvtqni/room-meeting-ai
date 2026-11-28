"""REAL GOOGLE tests: never substituted with fake tests.

These tests are skipped unless the operator explicitly supplies a credential
file, scopes, parent target, and read-only test document ID. No deletion or
migration is performed by this module.
"""
import os, sys, pytest
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_real_provider import GoogleConfig, validate_config, build_google_services, GoogleWorkspaceProvider
from work05_google_adapter import GoogleWorkspaceAdapter
pytestmark = pytest.mark.real_google
def _real_context():
    config=GoogleConfig.from_env(); target=os.environ.get('W05_REAL_TEST_DOCUMENT_ID',''); result=validate_config(config)
    if not result['ready'] or not target: pytest.skip('REAL GOOGLE prerequisites or explicit safe test document are unavailable')
    docs, drive=build_google_services(config); return GoogleWorkspaceAdapter(GoogleWorkspaceProvider(docs, drive, config.parent_id)), target
def test_real_google_read_only_document():
    adapter, target=_real_context(); result=adapter.read(target); assert result['id'] == target; assert 'revision' in result
