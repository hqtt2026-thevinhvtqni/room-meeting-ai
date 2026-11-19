#!/usr/bin/env node
/**
 * Work 17 — local bridge simulator.
 * This stub reads the local cache only. It is NEVER a real MCP source and
 * deliberately reports mcp-stub / fresh=false so it cannot pass live acceptance.
 */
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { validPayload } from './server.js';

const root = fileURLToPath(new URL('.', import.meta.url));
const port = Number(process.env.BRIDGE_PORT || 3100);

async function loadPayload() {
  const raw = JSON.parse(await readFile(resolve(root, 'live-data.json'), 'utf8'));
  if (!validPayload(raw)) throw new Error('live-data.json thiếu schema chuẩn theo BRIDGE_CONTRACT');
  return {
    ...raw,
    meta: {
      ...raw.meta,
      source: 'mcp-stub',
      fresh: false,
      bridgeConfigured: true,
      note: `${raw.meta.note || ''} | local stub: cache replay only; NOT real MCP delivery`
    }
  };
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || '/', 'http://localhost');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');

  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { Allow: 'GET, HEAD' });
    return res.end('Method Not Allowed');
  }
  if (url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    return res.end(JSON.stringify({
      ok: true,
      service: 'work17-mcp-bridge-stub',
      mode: 'stub-cache-replay',
      realMcp: false,
      checkedAt: new Date().toISOString()
    }));
  }
  if (['/api/work17-live', '/api/live', '/'].includes(url.pathname)) {
    try {
      const body = await loadPayload();
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(req.method === 'HEAD' ? undefined : JSON.stringify(body));
    } catch (error) {
      res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(JSON.stringify({ error: 'stub_failed', detail: error.message }));
    }
  }
  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  return res.end('Not found');
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Work 17 local bridge stub listening on http://127.0.0.1:${port}`);
  console.log('  Mode: mcp-stub / fresh=false / realMcp=false (never MCP LIVE)');
});
