import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer, validPayload, isFreshLivePayload } from '../04_CODE/WORK17_DASHBOARD/server.js';

const fixture = () => ({
  meta: { source: 'mcp-cache', fresh: false, syncedAt: new Date().toISOString() },
  summary: { works: 71, mirrors: 17, agentsRead: 13, p0Open: 5 },
  gates: [{ id: 'G0', name: 'Inventory', state: 'REFRESHED', detail: 'snapshot' }],
  portfolio: { works: 71, mirrors: 17, missingMirrors: 54 },
  agents: [['Agent', 'E1', 'candidate', 'source']],
  members: [['AI-01', 'Xu', 'declared', 'not proven']],
  gaps: [['GAP-01', 'Dispatch', 'A2A', 'P0', 'OPEN', 'receipt and ACK', 'G3']],
  e2e: [['01', 'Request', 'intent', 'W70', 'OPEN']]
});

test('accepts the canonical dashboard payload shape', () => {
  assert.equal(validPayload(fixture()), true);
});

test('rejects missing sections, wrong tuple widths, invalid timestamps and non-numeric KPIs', () => {
  const missing = fixture(); delete missing.members;
  assert.equal(validPayload(missing), false);

  const badTuple = fixture(); badTuple.gaps[0].pop();
  assert.equal(validPayload(badTuple), false);

  const badTime = fixture(); badTime.meta.syncedAt = 'not-a-date';
  assert.equal(validPayload(badTime), false);

  const badKpi = fixture(); badKpi.summary.works = '71';
  assert.equal(validPayload(badKpi), false);
});

test('accepts only explicitly labelled, fresh MCP live payloads', () => {
  const live = fixture();
  live.meta.source = 'mcp-live';
  live.meta.fresh = true;
  live.meta.syncedAt = new Date().toISOString();
  assert.equal(isFreshLivePayload(live), true);

  const cache = fixture();
  assert.equal(isFreshLivePayload(cache), false);

  const stub = fixture();
  stub.meta.source = 'mcp-stub';
  stub.meta.fresh = false;
  assert.equal(isFreshLivePayload(stub), false);

  const stale = { ...live, meta: { ...live.meta, syncedAt: new Date(Date.now() - 10 * 60_000).toISOString() } };
  assert.equal(isFreshLivePayload(stale), false);
});

test('health reports actual cache readiness and static traversal is denied', async (t) => {
  const server = createServer();
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise((resolve) => server.close(resolve)));
  const address = server.address();
  const base = `http://127.0.0.1:${address.port}`;

  const healthResponse = await fetch(`${base}/api/health`);
  assert.equal(healthResponse.status, 200);
  const health = await healthResponse.json();
  assert.equal(health.ok, true);
  assert.equal(health.cacheAvailable, true);
  assert.equal(health.process, 'alive');

  const traversal = await fetch(`${base}/..%2fWORK17_DASHBOARD2/secret.txt`);
  assert.equal(traversal.status, 403);

  const method = await fetch(`${base}/api/live`, { method: 'POST' });
  assert.equal(method.status, 405);
});
