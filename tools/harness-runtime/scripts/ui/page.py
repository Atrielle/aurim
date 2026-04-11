from __future__ import annotations

HTML_PAGE = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Aurim Harness Console</title>
  <style>
    :root { font-family: Inter, system-ui, sans-serif; color: #1f2937; background: #f5f7fb; }
    body { margin: 0; padding: 24px; }
    .wrap { max-width: 1100px; margin: 0 auto; display: grid; gap: 16px; }
    .card { background: white; border-radius: 14px; border: 1px solid #e5e7eb; padding: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.04); }
    h1 { margin: 0 0 8px; }
    p { margin: 0; color: #4b5563; }
    .grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
    label { font-size: 12px; color: #6b7280; display: block; margin-bottom: 4px; }
    input, select { width: 100%; padding: 8px 10px; border: 1px solid #d1d5db; border-radius: 8px; }
    button { border: 0; border-radius: 10px; padding: 10px 14px; background: #0f766e; color: #fff; cursor: pointer; }
    button.secondary { background: #475569; }
    .actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
    pre { margin: 0; background: #0b1020; color: #e5e7eb; border-radius: 10px; padding: 12px; overflow: auto; min-height: 220px; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    @media (max-width: 900px) { .grid, .row { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<div class=\"wrap\">
  <section class=\"card\">
    <h1>Harness Console</h1>
    <p>Run lifecycle commands from a UI while keeping the same runner gates.</p>
  </section>

  <section class=\"card\">
    <div class=\"grid\">
      <div>
        <label>Run ID</label>
        <input id=\"runId\" placeholder=\"sprint-020\" />
      </div>
      <div>
        <label>Unit ID (optional)</label>
        <input id=\"unitId\" placeholder=\"WU-001\" />
      </div>
      <div>
        <label>Report path (collect only)</label>
        <input id=\"reportPath\" placeholder=\"tools/harness-runtime/artifacts/runs/sprint-020/unit-report.md\" />
      </div>
      <div>
        <label>Known Runs</label>
        <select id=\"knownRuns\"></select>
      </div>
    </div>
    <div class=\"actions\">
      <button onclick=\"runCmd('create-run')\">create-run</button>
      <button onclick=\"runCmd('validate-contract')\">validate-contract</button>
      <button onclick=\"runCmd('freeze-contract')\">freeze-contract</button>
      <button onclick=\"runCmd('plan-units')\">plan-units</button>
      <button onclick=\"runCmd('dispatch-unit')\">dispatch-unit</button>
      <button onclick=\"runCmd('collect-unit')\">collect-unit</button>
      <button onclick=\"runCmd('gate-units')\">gate-units</button>
      <button onclick=\"runCmd('run-status')\">run-status</button>
      <button onclick=\"runCmd('gate-generator')\">gate-generator</button>
      <button onclick=\"runCmd('gate-close')\">gate-close</button>
      <button class=\"secondary\" onclick=\"runRegression()\">unit regression</button>
      <button class=\"secondary\" onclick=\"loadRuns()\">refresh runs</button>
    </div>
  </section>

  <section class=\"card row\">
    <div>
      <label>Command</label>
      <pre id=\"command\">(none)</pre>
    </div>
    <div>
      <label>Output</label>
      <pre id=\"output\">Ready.</pre>
    </div>
  </section>
</div>
<script>
async function postJson(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return response.json();
}

function selectedRunId() {
  const runId = document.getElementById('runId').value.trim();
  if (runId) return runId;
  const known = document.getElementById('knownRuns').value.trim();
  return known;
}

async function runCmd(command) {
  const payload = {
    command,
    run_id: selectedRunId(),
    unit_id: document.getElementById('unitId').value.trim(),
    report: document.getElementById('reportPath').value.trim()
  };
  const result = await postJson('/api/run-command', payload);
  document.getElementById('command').textContent = result.command_line || '(no command)';
  document.getElementById('output').textContent = result.output || result.error || '(no output)';
  if (payload.run_id) document.getElementById('runId').value = payload.run_id;
  await loadRuns();
}

async function runRegression() {
  const result = await postJson('/api/run-regression', {});
  document.getElementById('command').textContent = result.command_line;
  document.getElementById('output').textContent = result.output;
}

async function loadRuns() {
  const response = await fetch('/api/runs');
  const data = await response.json();
  const select = document.getElementById('knownRuns');
  select.innerHTML = '<option value="">(select)</option>';
  for (const runId of data.runs) {
    const option = document.createElement('option');
    option.value = runId;
    option.textContent = runId;
    select.appendChild(option);
  }
}

loadRuns();
</script>
</body>
</html>"""
