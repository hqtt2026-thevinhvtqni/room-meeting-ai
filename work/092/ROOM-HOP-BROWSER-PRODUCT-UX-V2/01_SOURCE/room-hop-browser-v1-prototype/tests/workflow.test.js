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
  assert.equal(result.ok, true);
  assert.equal(result.scenario, 'search');
  assert.equal(result.query, 'ROOM-HOP');
});

test('Vietnamese phrase tìm kiếm removes the verb from the query', () => {
  const result = workflow.resolveTask('Tìm kiếm dữ liệu khí hậu trên Wikipedia', 'browse');
  assert.equal(result.scenario, 'search');
  assert.equal(result.query, 'dữ liệu khí hậu');
});

test('English search command uses the supplied phrase rather than a fixed query', () => {
  const result = workflow.resolveTask('Search for climate policy', 'search');
  assert.equal(result.query, 'climate policy');
});

test('browse intent selects browse scenario', () => {
  const result = workflow.resolveTask('Mở trang chủ Wikipedia', 'search');
  assert.equal(result.scenario, 'browse');
});

test('workflow intent selects workflow scenario', () => {
  const result = workflow.resolveTask('Chạy agent workflow demo', 'search');
  assert.equal(result.scenario, 'workflow');
});

test('unclassified task respects the selected prepared scenario', () => {
  const result = workflow.resolveTask('ROOM-HOP', 'search');
  assert.equal(result.scenario, 'search');
  assert.equal(result.query, 'ROOM-HOP');
});

test('browse permissions include only capabilities used by its demo steps', () => {
  assert.deepEqual(workflow.requiredPermissions('browse'), ['readPage', 'inspect', 'screenshot']);
});

test('search permissions exclude workflow-only wait capability', () => {
  assert.deepEqual(workflow.requiredPermissions('search'), ['readPage', 'inspect', 'type', 'click', 'extract', 'screenshot']);
});

test('missing permissions block a scenario until explicitly granted', () => {
  assert.deepEqual(workflow.missingPermissions('search', {}), ['readPage', 'inspect', 'type', 'click', 'extract', 'screenshot']);
  const granted = { readPage: true, inspect: true, type: true, click: true, extract: true, screenshot: true };
  assert.deepEqual(workflow.missingPermissions('search', granted), []);
});

test('revoking a required permission blocks the scenario again', () => {
  const granted = { readPage: true, inspect: true, type: true, click: true, extract: true, screenshot: false };
  assert.deepEqual(workflow.missingPermissions('search', granted), ['screenshot']);
});

test('switching to a narrower scenario drops no-longer-required grants', () => {
  const allGranted = { readPage: true, inspect: true, click: true, type: true, wait: true, extract: true, screenshot: true };
  assert.deepEqual(workflow.permissionsForScenario('browse', allGranted), {
    readPage: true, inspect: true, click: false, type: false, wait: false, extract: false, screenshot: true
  });
});

test('mock evidence has source, type, timestamp, status, and no artifact', () => {
  const evidence = workflow.buildMockEvidence('Screenshot simulated', 'Screenshot action', 'No file created', '2026-11-22T00:00:00.000Z');
  assert.equal(evidence.source, 'mock-engine');
  assert.equal(evidence.type, 'simulated');
  assert.equal(evidence.timestamp, '2026-11-22T00:00:00.000Z');
  assert.equal(evidence.status, 'simulated');
  assert.equal(evidence.artifact, null);
});

test('completion is true only when every expected demo step succeeded', () => {
  assert.equal(workflow.isDemoComplete([], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }, { status: 'running' }], 2), false);
  assert.equal(workflow.isDemoComplete([{ status: 'success' }, { status: 'success' }], 2), true);
});
