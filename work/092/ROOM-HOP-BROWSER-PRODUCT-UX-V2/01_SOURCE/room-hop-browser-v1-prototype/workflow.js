(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.RoomHopWorkflow = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const SCENARIOS = Object.freeze(['browse', 'search', 'workflow']);
  const ALL_PERMISSIONS = Object.freeze(['readPage', 'inspect', 'click', 'type', 'wait', 'extract', 'screenshot']);
  const REQUIRED_PERMISSIONS = Object.freeze({
    browse: Object.freeze(['readPage', 'inspect', 'screenshot']),
    search: Object.freeze(['readPage', 'inspect', 'type', 'click', 'extract', 'screenshot']),
    workflow: Object.freeze(['readPage', 'inspect', 'type', 'click', 'wait', 'extract', 'screenshot'])
  });

  function resolveTask(input, selectedScenario) {
    const task = String(input == null ? '' : input).trim();
    if (!task) return { ok: false, error: 'Hãy nhập yêu cầu trước khi chạy kịch bản demo.' };

    let scenario = SCENARIOS.includes(selectedScenario) ? selectedScenario : 'search';
    const lower = task.toLocaleLowerCase();
    if (/\b(agent\s+workflow|workflow)\b/i.test(task) || lower.includes('quy trình')) scenario = 'workflow';
    else if (/\b(search|find|browse\s+for)\b/i.test(task) || lower.includes('tìm') || lower.includes('tra cứu')) scenario = 'search';
    else if (/\b(browse|open|visit)\b/i.test(task) || lower.includes('mở') || lower.includes('duyệt') || lower.includes('xem')) scenario = 'browse';

    let query = '';
    if (scenario === 'search') {
      const match = task.match(/(?:tìm(?:\s+kiếm)?|tra cứu|search(?:\s+for)?|find)\s+(.+)$/i);
      query = match ? match[1] : task.replace(/^\s*(?:please\s+)?(?:search(?:\s+for)?|find)\s+/i, '');
      query = query.replace(/\s+(?:on|in|trên)\s+wikipedia\s*$/i, '').replace(/[.!?]+\s*$/, '').trim();
      if (!query) return { ok: false, error: 'Hãy thêm từ khóa cần tìm trong kịch bản Search.' };
    }
    return { ok: true, task, scenario, query };
  }

  function requiredPermissions(scenario) { return (REQUIRED_PERMISSIONS[scenario] || []).slice(); }
  function permissionsForScenario(scenario, permissions) {
    const allowed = new Set(requiredPermissions(scenario));
    const granted = permissions || {};
    return Object.fromEntries(ALL_PERMISSIONS.map((name) => [name, allowed.has(name) && granted[name] === true]));
  }
  function missingPermissions(scenario, permissions) {
    const granted = permissions || {};
    return requiredPermissions(scenario).filter((name) => granted[name] !== true);
  }
  function buildMockEvidence(id, action, detail, timestamp) {
    return {
      id: String(id), action: String(action), source: 'mock-engine', sourceLabel: 'Mock demo engine',
      type: 'simulated', timestamp: timestamp || new Date().toISOString(), status: 'simulated',
      artifact: null, detail: String(detail)
    };
  }
  function isDemoComplete(history, expectedSteps) {
    return Number.isInteger(expectedSteps) && expectedSteps > 0 && Array.isArray(history) &&
      history.length === expectedSteps && history.every((item) => item && item.status === 'success');
  }

  return Object.freeze({
    SCENARIOS, REQUIRED_PERMISSIONS, resolveTask, requiredPermissions,
    permissionsForScenario, missingPermissions, buildMockEvidence, isDemoComplete
  });
});
