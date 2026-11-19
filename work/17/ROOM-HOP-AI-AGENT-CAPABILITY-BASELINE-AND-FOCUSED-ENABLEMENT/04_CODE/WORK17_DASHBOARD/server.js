import http from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { extname, relative, resolve, sep, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));
const rootReal = await realpath(root);
const port = Number(process.env.PORT || 3000);
const bridgeUrl = process.env.MCP_BRIDGE_URL || '';
const bridgeToken = process.env.MCP_BRIDGE_TOKEN || '';
const LIVE_MAX_AGE_MS = Number(process.env.MCP_LIVE_MAX_AGE_MS || 5 * 60 * 1000);
const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8'
};
const requiredKeys = ['meta', 'summary', 'gates', 'portfolio', 'agents', 'members', 'gaps', 'e2e'];

const isObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const isString = (v) => typeof v === 'string';
const isFiniteNumber = (v) => typeof v === 'number' && Number.isFinite(v);

export function validPayload(value) {
  if (!isObject(value) || !requiredKeys.every((key) => Object.hasOwn(value, key))) return false;
  if (!isObject(value.meta) || !isString(value.meta.syncedAt) || !Number.isFinite(Date.parse(value.meta.syncedAt))) return false;
  if (!isObject(value.summary) || !['works', 'mirrors', 'agentsRead', 'p0Open'].every((k) => isFiniteNumber(value.summary[k]))) return false;
  if (!isObject(value.portfolio) || !['works', 'mirrors', 'missingMirrors'].every((k) => isFiniteNumber(value.portfolio[k]))) return false;
  if (!Array.isArray(value.gates) || !value.gates.every((x) => isObject(x) && ['id', 'name', 'state', 'detail'].every((k) => isString(x[k])))) return false;
  const tupleArrays = [
    [value.agents, 4],
    [value.members, 4],
    [value.gaps, 7],
    [value.e2e, 5]
  ];
  return tupleArrays.every(([rows, width]) =>
    Array.isArray(rows) && rows.every((row) =>
      Array.isArray(row) && row.length === width && row.every(isString)
    )
  );
}

export function isFreshLivePayload(value, now = Date.now()) {
  if (!validPayload(value)) return false;
  if (value.meta.source !== 'mcp-live' || value.meta.fresh !== true) return false;
  const age = now - Date.parse(value.meta.syncedAt);
  return age >= -60_000 && age <= LIVE_MAX_AGE_MS;
}

async function readCache() {
  const parsed = JSON.parse(await readFile(resolve(root, 'live-data.json'), 'utf8'));
  if (!validPayload(parsed)) throw new Error('MCP cache không đúng schema BRIDGE_CONTRACT');
  return {
    ...parsed,
    meta: { ...parsed.meta, source: 'mcp-cache', fresh: false, bridgeConfigured: Boolean(bridgeUrl) }
  };
}

async function readLiveData() {
  if (!bridgeUrl) return readCache();
  try {
    const headers = { Accept: 'application/json' };
    if (bridgeToken) headers.Authorization = `Bearer ${bridgeToken}`;
    const response = await fetch(bridgeUrl, { headers, signal: AbortSignal.timeout(7000) });
    if (!response.ok) throw new Error(`MCP bridge HTTP ${response.status}`);
    const payload = await response.json();
    if (!isFreshLivePayload(payload)) {
      throw new Error('Bridge payload không đạt schema/provenance/freshness; chỉ chấp nhận source=mcp-live, fresh=true và syncedAt còn hạn');
    }
    return {
      ...payload,
      meta: { ...payload.meta, bridgeConfigured: true, warning: undefined }
    };
  } catch (error) {
    const cached = await readCache();
    return {
      ...cached,
      meta: { ...cached.meta, warning: `Live bridge không được xác minh: ${error.message}`, bridgeConfigured: true }
    };
  }
}

function sendJson(res, status, body) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff'
  });
  res.end(JSON.stringify(body));
}

async function resolveStaticFile(pathname) {
  let decoded;
  try { decoded = decodeURIComponent(pathname); }
  catch { throw Object.assign(new Error('Invalid URL encoding'), { statusCode: 400 }); }
  if (decoded.includes(String.fromCharCode(0))) throw Object.assign(new Error('Invalid path'), { statusCode: 400 });
  const candidate = resolve(rootReal, `.${decoded}`);
  const rel = relative(rootReal, candidate);
  if (rel === '..' || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
    throw Object.assign(new Error('Forbidden'), { statusCode: 403 });
  }
  const actual = await realpath(candidate);
  const actualRel = relative(rootReal, actual);
  if (actualRel === '..' || actualRel.startsWith(`..${sep}`) || isAbsolute(actualRel)) {
    throw Object.assign(new Error('Forbidden'), { statusCode: 403 });
  }
  return actual;
}

export function createServer() {
  return http.createServer(async (req, res) => {
    let url;
    try { url = new URL(req.url, 'http://localhost'); }
    catch { res.writeHead(400); return res.end('Bad Request'); }

    if (!['GET', 'HEAD'].includes(req.method)) {
      res.writeHead(405, { Allow: 'GET, HEAD' });
      return res.end('Method Not Allowed');
    }

    if (url.pathname === '/api/live') {
      try { return sendJson(res, 200, await readLiveData()); }
      catch (error) { return sendJson(res, 503, { error: 'live_data_unavailable', detail: error.message }); }
    }

    if (url.pathname === '/api/health') {
      let cacheAvailable = false;
      let cacheError = null;
      try { await readCache(); cacheAvailable = true; }
      catch (error) { cacheError = error.message; }
      const body = {
        ok: cacheAvailable,
        service: 'work17dash',
        process: 'alive',
        readiness: cacheAvailable ? 'ready-with-cache' : 'degraded-no-valid-cache',
        bridge: bridgeUrl ? 'configured-not-probed' : 'not-configured',
        bridgeConfigured: Boolean(bridgeUrl),
        cacheAvailable,
        cacheError,
        contract: 'BRIDGE_CONTRACT.md',
        checkedAt: new Date().toISOString()
      };
      return sendJson(res, cacheAvailable ? 200 : 503, body);
    }

    let pathname = url.pathname === '/' ? '/index.html' : url.pathname;
    if (pathname === '/manus-routes.json') pathname = '/public/manus-routes.json';
    try {
      const file = await resolveStaticFile(pathname);
      const body = await readFile(file);
      res.writeHead(200, {
        'Content-Type': types[extname(file)] || 'application/octet-stream',
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff'
      });
      return res.end(req.method === 'HEAD' ? undefined : body);
    } catch (error) {
      const status = error.statusCode || (error.code === 'ENOENT' || error.code === 'ENOTDIR' ? 404 : 500);
      res.writeHead(status, { 'Content-Type': 'text/plain; charset=utf-8', 'X-Content-Type-Options': 'nosniff' });
      return res.end(status === 403 ? 'Forbidden' : status === 404 ? 'Not found' : status === 400 ? 'Bad Request' : 'Internal Server Error');
    }
  });
}

const invokedPath = process.argv[1] ? resolve(process.argv[1]) : '';
if (invokedPath === resolve(fileURLToPath(import.meta.url))) {
  createServer().listen(port, '127.0.0.1', () => {
    console.log(`Work 17 dashboard listening on http://127.0.0.1:${port}`);
    console.log(`  MCP bridge: ${bridgeUrl || 'not configured → MCP CACHE (live-data.json)'}`);
    console.log('  Live acceptance requires a schema-valid, provenance-labelled, fresh MCP payload.');
  });
}
