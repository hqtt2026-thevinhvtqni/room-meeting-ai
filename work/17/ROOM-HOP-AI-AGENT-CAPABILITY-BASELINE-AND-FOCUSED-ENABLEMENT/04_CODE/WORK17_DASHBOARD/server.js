import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));
const port = Number(process.env.PORT || 3000);
const bridgeUrl = process.env.MCP_BRIDGE_URL || '';
const bridgeToken = process.env.MCP_BRIDGE_TOKEN || '';
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.json':'application/json; charset=utf-8' };
const requiredKeys = ['meta','summary','gates','portfolio','agents','members','gaps','e2e'];

async function readCache() {
  const parsed = JSON.parse(await readFile(join(root, 'live-data.json'), 'utf8'));
  return { ...parsed, meta: { ...parsed.meta, source: 'mcp-cache', fresh: false, bridgeConfigured: Boolean(bridgeUrl) } };
}
function validPayload(value) { return value && requiredKeys.every((key) => key in value); }
async function readLiveData() {
  if (bridgeUrl) {
    try {
      const headers = { 'Accept':'application/json' };
      if (bridgeToken) headers.Authorization = `Bearer ${bridgeToken}`;
      const response = await fetch(bridgeUrl, { headers, signal: AbortSignal.timeout(7000) });
      if (!response.ok) throw new Error(`MCP bridge HTTP ${response.status}`);
      const payload = await response.json();
      if (!validPayload(payload)) throw new Error('MCP bridge payload thiếu trường chuẩn hóa');
      return { ...payload, meta: { ...payload.meta, source:'mcp-live', fresh:true, syncedAt:new Date().toISOString(), bridgeConfigured:true } };
    } catch (error) {
      const cached = await readCache();
      return { ...cached, meta: { ...cached.meta, warning:`Live bridge lỗi: ${error.message}`, bridgeConfigured:true } };
    }
  }
  return readCache();
}
function sendJson(res, status, body) { res.writeHead(status, {'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','Access-Control-Allow-Origin':'*'}); res.end(JSON.stringify(body)); }

http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (url.pathname === '/api/live') {
    try { return sendJson(res, 200, await readLiveData()); }
    catch (error) { return sendJson(res, 500, { error:'live_data_unavailable', detail:error.message }); }
  }
  if (url.pathname === '/api/health') {
    return sendJson(res, 200, { ok:true, service:'work17dash', bridgeConfigured:Boolean(bridgeUrl), cacheAvailable:true, checkedAt:new Date().toISOString() });
  }
  let pathname = url.pathname === '/' ? '/index.html' : url.pathname;
  if (pathname === '/manus-routes.json') pathname = '/public/manus-routes.json';
  const file = normalize(join(root, pathname));
  if (!file.startsWith(root)) { res.writeHead(403); return res.end('Forbidden'); }
  try { const body = await readFile(file); res.writeHead(200, {'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store'}); res.end(body); }
  catch { res.writeHead(404, {'Content-Type':'text/plain'}); res.end('Not found'); }
}).listen(port, '0.0.0.0', () => console.log(`Work 17 dashboard listening on ${port}; MCP bridge ${bridgeUrl ? 'configured' : 'not configured'}`));
