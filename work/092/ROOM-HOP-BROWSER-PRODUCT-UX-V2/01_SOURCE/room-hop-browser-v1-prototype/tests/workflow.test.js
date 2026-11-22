'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const workflow = require('../workflow.js');

test('empty task is rejected', () => {
  const result = workflow.resolveTask('   ', 'search');
  assert.equal(result.ok, false);
  assert.match(result.error, /nhập yêu cầu/i);
});

test('search task text selects search and extracts the user query', () => {
  const result = workflow.resolveTask('Mở Wikipedia và tìm ROOM-HOP', 'browse');
  assert.equal(result.ok, true); assert.equal(result.scenario, 'search'); assert.equal(result.query, 'ROOM-HOP');
});

test('Vietnamese phrase tìm kiếm removes the verb from the query', () => {
  const result = workflow.resolveTask('Tìm kiếm dữ liệu khí hậu trên Wikipedia', 'browse');
  assert.equal(result.scenario, 'search'); assert.equal(result.query, 'dữ liệu khí hậu');
});

test('English search command uses supplied phrase rather than fixed query', () => {
  const result = workflow.resolveTask('Search for climate policy', 'search'); assert.equal(result.query, 'climate policy');
});

test('browse intent selects browse scenario', () => {
  const result = workflow.resolveTask('Mở trang chủ Wikipedia', 'search'); assert.equal(result.scenario, 'browse');
});

test('workflow intent selects test-only workflow scenario', () => {
  const result = workflow.resolveTask('Chạy agent workflow demo', 'search'); assert.equal(result.scenario, 'workflow');
});

test('unclassified task respects selected prepared scenario', () => {
  const result = workflow.resolveTask('ROOM-HOP', 'search'); assert.equal(result.scenario, 'search'); assert.equal(result.query, 'ROOM-HOP');
});

test('browse permissions include only capabilities used by its demo steps', () => {
  assert.deepEqual(workflow.requiredPermissions('browse'), ['readPage', 'inspect', 'screenshot']);
});

test('search permissions exclude workflow-only wait capability', () => {
  assert.deepEqual(workflow.requiredPermissions('search'), ['readPage', 'inspect', 'type', 'click', 'extract', 'screenshot']);
});

test('missing permissions block a scenario until explicitly enabled', () => {
  assert.deepEqual(workflow.missingPermissions('search', {}), ['readPage', 'inspect', 'type', 'click', 'extract', 'screenshot']);
  const enabled = { readPage: true, inspect: true, type: true, click: true, extract: true, screenshot: true };
  assert.deepEqual(workflow.missingPermissions('search', enabled), []);
});

test('disabling a required permission blocks the scenario again', () => {
  const enabled = { readPage: true, inspect: true, type: true, click: true, extract: true, screenshot: false };
  assert.deepEqual(workflow.missingPermissions('search', enabled), ['screenshot']);
});

test('switching to a narrower scenario drops no-longer-required permissions', () => {
  const enabled = { readPage: true, inspect: true, click: true, type: true, wait: true, extract: true, screenshot: true };
  assert.deepEqual(workflow.permissionsForScenario('browse', enabled), {
    readPage: true, inspect: true, click: false, type: false, wait: false, extract: false, screenshot: true
  });
});

test('mock evidence has provenance and no artifact', () => {
  const evidence = workflow.buildMockEvidence('Screenshot simulated', 'Screenshot action', 'No file created', '2026-11-22T00:00:00.000Z');
  assert.equal(evidence.source, 'mock-engine'); assert.equal(evidence.type, 'simulated');
  assert.equal(evidence.timestamp, '2026-11-22T00:00:00.000Z'); assert.equal(evidence.status, 'simulated');
  assert.equal(evidence.artifact, null); assert.equal(evidence.sourceLabel, 'TEST_ONLY fixture');
});

test('completion requires every expected demo step to succeed', () => {
  assert.equal(workflow.isDemoComplete([], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }, { status: 'running' }], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }, { status: 'success' }], 2), true);
});

test('initial UI state is ready only for TEST_ONLY while runtime stays disconnected', () => {
  assert.deepEqual(workflow.getDemoUiState(), { runtime: 'DISCONNECTED', activity: 'TEST_ONLY_READY', canRun: true });
});

test('running UI state never reports a connected or working agent', () => {
  assert.deepEqual(workflow.getDemoUiState({ running: true }), { runtime: 'DISCONNECTED', activity: 'TEST_ONLY_RUNNING', canRun: false });
});

test('human hold blocks only the local test script', () => {
  assert.deepEqual(workflow.getDemoUiState({ held: true }), { runtime: 'DISCONNECTED', activity: 'TEST_ONLY_HELD', canRun: false });
});

test('completion label is TEST_ONLY and runtime remains disconnected', () => {
  assert.deepEqual(workflow.getDemoUiState({ complete: true }), { runtime: 'DISCONNECTED', activity: 'TEST_ONLY_COMPLETE', canRun: true });
});
