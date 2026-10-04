from pathlib import Path

src = Path(r"Original Reference/fortunes_weave_complete_sheet_2026-10-02.html")
dst = Path(r"fortunes_weave_reference.html")
text = src.read_text(encoding="utf-8")

# Slice original sections by unique markers.
gifts = text.split('<section class="tab-panel" id="tab-2"', 1)[1]
gifts = gifts.split('<section class="tab-panel" id="tab-3"', 1)[0]
gifts = '<section class="tab-panel" id="gifts"' + gifts
gifts = gifts.replace('id="tab-2"', 'id="gifts"').replace('aria-labelledby="tab-button-2"', 'aria-labelledby="tab-gifts"')
gifts = gifts.replace('<h2 class="panel-title">2. Gift giving guide</h2>', '<h2 class="panel-title">Gift giving guide</h2>')

builds = text.split('<section class="tab-panel" id="buildGuide"', 1)[1]
builds = builds.split('<section class="tab-panel" id="tab-7"', 1)[0]
builds = '<section class="tab-panel" id="buildGuide"' + builds
builds = builds.replace('aria-labelledby="tab-button-6"', 'aria-labelledby="tab-builds"')
builds = builds.replace('aria-labelledby="tab-button-7"', 'aria-labelledby="tab-stats"')
builds = builds.replace('aria-labelledby="tab-button-8"', 'aria-labelledby="tab-original"')
builds = builds.replace('aria-labelledby="tab-button-9"', 'aria-labelledby="tab-recruits"')
builds = builds.replace('<h2 class="panel-title">6. Cai &amp; Leda builds (no external links)</h2>', '<h2 class="panel-title">Cai &amp; Leda builds</h2>')
builds = builds.replace('<h2 class="panel-title">7. Class &amp; final stat log</h2>', '<h2 class="panel-title">Class &amp; final stat log</h2>')
builds = builds.replace('<h2 class="panel-title">8. Original clear-data stats</h2>', '<h2 class="panel-title">Original clear-data stats</h2>')
builds = builds.replace('<h2 class="panel-title">9. Shared recruit planner — Part I/II only</h2>', '<h2 class="panel-title">Shared recruit planner — Part I/II only</h2>')
builds = builds.replace('Part III planning · no story spoilers', 'Cross-route planning · no story spoilers')
builds = builds.replace(
    'When versions of a unit are merged, the higher value of each stat is retained. Training different strengths on different routes can therefore complement each other.',
    'When versions of a unit are merged, the higher value of each stat is retained. Raise leftover lows only with classes inside that unit’s intended weapon family; Part 3 returns everyone to that line.',
)
builds = builds.replace(
    '<details class="nested"><summary>Starting party',
    '<p class="small">The collapsible cards below are leftover generic class notes. Use the combined table above for Cai and Leda.</p>\n<details class="nested"><summary>Starting party',
)
builds = builds.replace(
    'The two later-story additions are intentionally omitted from this Part I quick sheet.',
    'Later-story-only additions are omitted from this Part I / II sheet.',
)
builds = builds.replace(
    '<details class="nested" open data-stat-route="Theodora">',
    '<details class="nested persist-open" open data-stat-route="Theodora" data-persist-open="stat-theodora">',
)
builds = builds.replace(
    '<details class="nested" data-stat-route="Dietrich">',
    '<details class="nested persist-open" data-stat-route="Dietrich" data-persist-open="stat-dietrich">',
)
builds = builds.replace(
    '<details class="nested" data-stat-route="Cai">',
    '<details class="nested persist-open" data-stat-route="Cai" data-persist-open="stat-cai">',
)
builds = builds.replace(
    '<details class="nested" data-stat-route="Leda">',
    '<details class="nested persist-open" data-stat-route="Leda" data-persist-open="stat-leda">',
)
plan = Path("_builds_plan_snippet.html").read_text(encoding="utf-8")
start = builds.find('<div class="callout"><strong>Combined plan:')
end = builds.find('<details class="nested"><summary>Cross-route class pairings')
if start < 0 or end < 0:
    raise SystemExit("combined plan markers not found")
builds = builds[:start] + plan + "\n    " + builds[end:]

orig_stats = Path("_original_stats_snippet.html").read_text(encoding="utf-8")
start = builds.find('<section class="tab-panel" id="originalStats"')
end = builds.find('<section class="tab-panel" id="sharedPlanner"')
if start < 0 or end < 0:
    raise SystemExit("originalStats / sharedPlanner markers not found")
builds = builds[:start] + orig_stats + "\n" + builds[end:]

stat_tab = Path("_stat_tab_snippet.html").read_text(encoding="utf-8")
start = builds.find('<section class="tab-panel" id="statLog"')
end = builds.find('<section class="tab-panel" id="originalStats"')
if start < 0 or end < 0:
    raise SystemExit("statLog / originalStats markers not found")
builds = builds[:start] + stat_tab + "\n" + builds[end:]

adv_classes = Path("_adv_classes_snippet.html").read_text(encoding="utf-8")
start = builds.find('<section class="tab-panel" id="statLog"')
if start < 0:
    raise SystemExit("statLog marker not found for Advanced classes tab")
builds = builds[:start] + adv_classes + "\n" + builds[start:]

script = text.split("<script>", 1)[1]
script = script.split("</script>", 1)[0]

css_extra = """
.route-block > summary { font-size:17px; }
.route-toolbar { display:flex; flex-wrap:wrap; gap:8px; margin:10px 0; }
details.cycle > summary .date { float:none; margin-left:8px; }
.adv-shell { display:flex; align-items:flex-start; gap:10px; width:max-content; max-width:100%; }
.adv-wrap { overflow:auto; flex:0 1 auto; min-width:0; max-width:calc(100% - 50px); padding-right:8px; }
.adv-skills-toggle {
  flex:none;
  position:sticky;
  top:12px;
  writing-mode:vertical-rl;
  transform:rotate(180deg);
  padding:10px 8px;
  font-size:12px;
  font-weight:700;
  letter-spacing:.04em;
  border-radius:0 9px 9px 0;
  align-self:flex-start;
  height:min(240px, 42vh);
  z-index:2;
}
.stat-table th, .stat-table td {
  padding:5px 6px;
  border-right:1px solid var(--line);
}
.stat-table th:last-child, .stat-table td:last-child { border-right:0; }
.stat-table thead th, .adv-table thead th {
  background:var(--bg);
  color:var(--accent);
  font-weight:750;
  letter-spacing:.03em;
  border-bottom:2px solid var(--accent);
}
.stat-table thead th { font-size:12px; }
.stat-table thead th:first-child { background:var(--bg); }
.stat-table tbody tr:nth-child(odd) > * { background:var(--panel2); }
.stat-table tbody tr:nth-child(even) > * { background:var(--chip); }
.stat-table tbody tr:nth-child(odd) td:first-child { background:var(--panel2); }
.stat-table tbody tr:nth-child(even) td:first-child { background:var(--chip); }
.adv-table { width:100%; min-width:980px; border-collapse:collapse; font-size:13px; line-height:1.3; }
.adv-table th, .adv-table td { padding:5px 6px; vertical-align:top; border-right:1px solid var(--line); }
.adv-table th:last-child, .adv-table td:last-child { border-right:0; }
.adv-table thead th { position:sticky; top:0; z-index:1; font-size:12px; }
.adv-table tbody th { text-align:left; white-space:nowrap; font-size:14px; }
.adv-table tbody tr:nth-child(even):not(.adv-group) td,
.adv-table tbody tr:nth-child(even):not(.adv-group) th { background:var(--chip); }
.adv-table .adv-group th {
  border-right:0;
  background:var(--accent);
  color:var(--bg);
  font-size:16px;
  font-weight:750;
  letter-spacing:.02em;
  text-align:left;
  white-space:normal;
  padding:8px 10px;
}
.adv-table .adv-group .why { display:block; margin-top:3px; font-size:12px; font-weight:500; letter-spacing:0; color:var(--bg); opacity:.88; }
.adv-table .sub { display:block; color:var(--muted); font-weight:400; font-size:11px; white-space:normal; max-width:160px; }
.adv-table th:last-child, .adv-table td:last-child {
  max-width:22em;
  overflow:hidden;
  transition:max-width .22s ease, padding .22s ease, opacity .18s ease;
}
#advClasses.skills-collapsed .adv-table { min-width:0; width:max-content; }
#advClasses.skills-collapsed .adv-table thead th:last-child,
#advClasses.skills-collapsed .adv-table tbody td:last-child {
  max-width:0 !important;
  width:0 !important;
  padding:0 !important;
  opacity:0;
  border:0;
  overflow:hidden;
  pointer-events:none;
  font-size:0;
  line-height:0;
}
.adv-table .g { font-variant-numeric:tabular-nums; text-align:right; white-space:nowrap; }
.adv-table .g.pos { color:var(--good); font-weight:650; }
.adv-table .g.neg { color:var(--accent); font-weight:650; }
.adv-table .g.z { color:var(--muted); }
.adv-table .on, .adv-table .mast, .adv-table .unl { display:block; }
.adv-table .mast { margin-top:2px; }
.adv-table .unl { margin-top:2px; color:var(--accent); font-size:10px; }
@media (max-width:720px) {
  #advClasses th:nth-child(4), #advClasses td:nth-child(4) { display:table-cell; }
}
"""

header = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fortune's Weave — Leda &amp; Cai Reference</title>
<script type="application/json" id="fw-embedded-progress"></script>
'''

# Keep original CSS block.
css = text.split("<style>", 1)[1].split("</style>", 1)[0]

cycles = Path("_cycles_snippet.html").read_text(encoding="utf-8")
persist_js = Path("_persist_snippet.js").read_text(encoding="utf-8")

# Patch script: insert persist helpers after const root...
old_checks = """document.querySelectorAll('input.persist').forEach(cb => {
  cb.checked = localStorage.getItem('fw-check-' + cb.id) === '1';
  cb.addEventListener('change', () => localStorage.setItem('fw-check-' + cb.id, cb.checked ? '1' : '0'));
});
document.getElementById('resetChecks').addEventListener('click', () => {
  document.querySelectorAll('input.persist').forEach(cb => {
    cb.checked = false;
    localStorage.removeItem('fw-check-' + cb.id);
  });
});"""

new_checks = """document.querySelectorAll('input.persist').forEach(cb => {
  cb.checked = localStorage.getItem('fw-check-' + cb.id) === '1';
  cb.addEventListener('change', () => {
    localStorage.setItem('fw-check-' + cb.id, cb.checked ? '1' : '0');
    persistSoon();
  });
});
document.getElementById('resetChecks').addEventListener('click', () => {
  const scope = document.getElementById('cycles');
  scope.querySelectorAll('input.persist').forEach(cb => {
    cb.checked = false;
    localStorage.removeItem('fw-check-' + cb.id);
  });
  persistSoon();
});"""

if old_checks not in script:
    raise SystemExit("checkbox persist block not found")
script = script.replace(old_checks, new_checks)

script = script.replace(
    "const saveStats = () => localStorage.setItem(statStorageKey, JSON.stringify(statLog));",
    "const saveStats = () => { localStorage.setItem(statStorageKey, JSON.stringify(statLog)); persistSoon(); };",
)
script = script.replace(
    "const savePlanner = () => localStorage.setItem(plannerKey, JSON.stringify(plannerState));",
    "const savePlanner = () => { localStorage.setItem(plannerKey, JSON.stringify(plannerState)); persistSoon(); };",
)
script = script.replace(
    "localStorage.setItem('fw-theme', light ? 'light' : 'dark');\n});",
    "localStorage.setItem('fw-theme', light ? 'light' : 'dark');\n  persistSoon();\n});",
)
script = script.replace(
    "    localStorage.setItem('fw-tab', String(index));\n    window.scrollTo(0, 0);",
    "    localStorage.setItem('fw-tab', String(index));\n    persistSoon();\n    window.scrollTo(0, 0);",
)

# Restore planner filters from storage after renderPlanner is defined — inject restore near renderPlanner();
script = script.replace(
    "renderPlanner();\n\nconst backupStatus",
    """function restorePlannerFilters() {
  const sort = localStorage.getItem('fw-planner-sort');
  const pending = localStorage.getItem('fw-planner-pending');
  const hidden = localStorage.getItem('fw-planner-show-hidden');
  const searchText = localStorage.getItem('fw-planner-search');
  if (sort) document.getElementById('plannerSort').value = sort;
  if (pending === '1') document.getElementById('plannerPending').checked = true;
  if (hidden === '1') document.getElementById('plannerShowHidden').checked = true;
  if (searchText) document.getElementById('plannerSearch').value = searchText;
}
restorePlannerFilters();
['plannerSearch','plannerSort','plannerPending','plannerShowHidden'].forEach(id => {
  const el = document.getElementById(id);
  const eventName = id === 'plannerSearch' ? 'input' : 'change';
  el.addEventListener(eventName, () => {
    if (id === 'plannerSearch') localStorage.setItem('fw-planner-search', el.value);
    if (id === 'plannerSort') localStorage.setItem('fw-planner-sort', el.value);
    if (id === 'plannerPending') localStorage.setItem('fw-planner-pending', el.checked ? '1' : '0');
    if (id === 'plannerShowHidden') localStorage.setItem('fw-planner-show-hidden', el.checked ? '1' : '0');
    persistSoon();
  });
});
renderPlanner();

const backupStatus""",
)

# Gift search persist
script = script.replace(
    """search.addEventListener('input', () => {
  const q = search.value.trim().toLowerCase();
  document.querySelectorAll('.gift-card').forEach(card => {
    card.style.display = card.dataset.search.includes(q) ? '' : 'none';
  });
});""",
    """const applyGiftSearch = () => {
  const q = search.value.trim().toLowerCase();
  document.querySelectorAll('.gift-card').forEach(card => {
    card.style.display = card.dataset.search.includes(q) ? '' : 'none';
  });
};
search.value = localStorage.getItem('fw-gift-search') || '';
applyGiftSearch();
search.addEventListener('input', () => {
  localStorage.setItem('fw-gift-search', search.value);
  applyGiftSearch();
  persistSoon();
});""",
)

# Hook persist after import success
script = script.replace(
    "backupStatus.textContent = 'Progress imported: checklists, stats, recruits, and preferences restored.';",
    "applyStoredDetails();\n    backupStatus.textContent = 'Progress imported: checklists, stats, recruits, and preferences restored.';\n    persistSoon();",
)

script = script.replace(
    """    const storage = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('fw-')) storage[key] = localStorage.getItem(key);
    }
    document.querySelectorAll('input.persist').forEach(cb => {
      storage['fw-check-' + cb.id] = cb.checked ? '1' : '0';
    });
    storage[statStorageKey] = JSON.stringify(statLog);
    storage[plannerKey] = JSON.stringify(plannerState);
    storage['fw-theme'] = root.classList.contains('light') ? 'light' : 'dark';
    storage['fw-tab'] = String(panels.findIndex(panel => !panel.hidden));
    const backup = {app:'fortunes-weave-quick-sheet', formatVersion:1, exportedAt:new Date().toISOString(), storage};""",
    """    const storage = collectStorage();
    storage[statStorageKey] = JSON.stringify(statLog);
    storage[plannerKey] = JSON.stringify(plannerState);
    const backup = {app:'fortunes-weave-quick-sheet', formatVersion:1, exportedAt:new Date().toISOString(), storage};""",
)

script = script.replace(
    "  ].map(values => Object.fromEntries(statFields.map((field, i) => [field, values[i]]))),\n  Dietrich: [], Cai: [], Leda: []",
    """  ].map(values => Object.fromEntries(statFields.map((field, i) => [field, values[i]]))),
  Dietrich: [
    ['Esmeralda','Dreadnought',50,68,4,46,12,14,21,48,16,22,24],
    ['Ultand','Bishop',49,49,5,24,31,25,28,18,42,40,37],
    ['Mu','Blacksmith',44,51,5,30,14,27,32,27,21,15,24],
    ['Mikaela','Warrior',47,60,5,43,18,24,22,24,13,22,28],
    ['Ninae','Shido',46,57,5,28,16,30,31,21,27,25,21],
    ['Catania','Dreadnought',42,47,4,26,20,23,30,30,16,21,27],
    ['Olympia','Dreadnought',39,41,4,18,28,13,16,25,19,23,23],
    ['Loretta','Dreadnought',40,43,4,21,18,22,22,24,18,16,15],
    ['Sofia','Dreadnought',41,42,4,18,32,9,23,26,21,17,22],
    ['Alexandra','Dreadnought',39,38,4,23,15,22,21,25,21,25,27],
    ['Lilian','Dreadnought',38,41,4,22,14,20,30,22,10,23,15],
    ['Inyoni','Sniper',35,40,5,25,10,22,24,16,11,18,14],
    ['Noctula','Dreadnought',35,51,4,30,7,17,21,29,11,17,15],
    ['Dante','Ovate',35,36,5,11,31,26,26,9,27,19,13]
  ].map(values => Object.fromEntries(statFields.map((field, i) => [field, values[i]]))),
  Cai: [], Leda: []""",
)

script = script.replace(
    "].map(([name, ...ranks]) => [name, Object.fromEntries(skillFields.map((field, i) => [field, ranks[i]]))]));",
    """].map(([name, ...ranks]) => [name, Object.fromEntries(skillFields.map((field, i) => [field, ranks[i]]))]));
const originalSkillRanksDietrich = Object.fromEntries([
  ['Esmeralda','A','S','A','C','E','E','E','B','B','C','A','C'],
  ['Ultand','E','C','E','E','D','A','S','D','B','E','C','D'],
  ['Mu','B','C','A','D','A','C','C','D','C','C','B','B'],
  ['Mikaela','A','B','S','D','B','E','E','D','C','B','B','E'],
  ['Ninae','B','B','C','C','C','E','C','B','C','D','C','D'],
  ['Catania','C','C','D','E','E','E','E','D','D','D','D','C'],
  ['Olympia','E','D','D','E','E','D','B','E','D','D','D','E'],
  ['Loretta','B','B','D','E','D','E','E','E','E','D','D','B'],
  ['Sofia','D','C','C','D','D','D','B','D','C','C','D','D'],
  ['Alexandra','C','B','D','E','E','E','E','E','D','D','E','B'],
  ['Lilian','D','D','D','B','E','E','E','D','D','D','B','D'],
  ['Inyoni','D','E','E','B','E','E','E','E','D','E','C','E'],
  ['Noctula','D','D','D','E','B','E','E','D','E','E','D','E'],
  ['Dante','E','E','E','E','D','C','C','E','E','E','D','E']
].map(([name, ...ranks]) => [name, Object.fromEntries(skillFields.map((field, i) => [field, ranks[i]]))]));""",
)

# The following replace is applied after persistSoon saveStats patch.
script = script.replace(
    """function renderStatRoute(section) {""",
    """function rankIndex(rank) {
  const index = rankOptions.indexOf(rank);
  return index < 0 ? -1 : index;
}
function betterRank(a, b) {
  return rankIndex(a) >= rankIndex(b) ? (a || b || '') : (b || a || '');
}
function maxStat(a, b) {
  const na = Number(a), nb = Number(b);
  const aOk = a !== '' && a != null && Number.isFinite(na);
  const bOk = b !== '' && b != null && Number.isFinite(nb);
  if (aOk && bOk) return Math.max(na, nb);
  if (aOk) return na;
  if (bOk) return nb;
  return '';
}
function mergedClass(theo, diet) {
  const c1 = theo?.class || '';
  const c2 = diet?.class || '';
  if (c1 && c2 && c1 !== c2) return c1 + ' / ' + c2;
  return c1 || c2;
}
function mergedBankedRows() {
  const theo = Object.fromEntries((originalStats.Theodora || []).map(row => [row.name, row]));
  const diet = Object.fromEntries((originalStats.Dietrich || []).map(row => [row.name, row]));
  const names = [];
  (originalStats.Theodora || []).forEach(row => names.push(row.name));
  (originalStats.Dietrich || []).forEach(row => { if (!names.includes(row.name)) names.push(row.name); });
  return names.map(name => {
    const t = theo[name], d = diet[name];
    const row = { name, class: mergedClass(t, d) };
    ['lv','hp','mov','str','mag','spd','dex','def','res','lck','cha'].forEach(field => {
      row[field] = maxStat(t?.[field], d?.[field]);
    });
    row.skills = {};
    skillFields.forEach(field => {
      row.skills[field] = betterRank(originalSkillRanks[name]?.[field], originalSkillRanksDietrich[name]?.[field]);
    });
    return row;
  });
}
function fillStatTable(target, rows, includeClass) {
  const table = document.createElement('table');
  table.className = 'stat-table stat-table-reference';
  const head = document.createElement('thead');
  const header = document.createElement('tr');
  const labels = includeClass ? [...statNames, 'Rating'] : ['Character', ...skillNames];
  labels.forEach(label => { const th = document.createElement('th'); th.textContent = label; header.append(th); });
  head.append(header); table.append(head);
  const body = document.createElement('tbody');
  rows.forEach(row => {
    const tr = document.createElement('tr');
    if (includeClass) {
      [...statFields, 'rating'].forEach(field => {
        const td = document.createElement('td');
        td.textContent = field === 'rating' ? String(statRating(row)) : String(row[field] ?? '');
        tr.append(td);
      });
    } else {
      const name = document.createElement('td'); name.textContent = row.name; tr.append(name);
      skillFields.forEach(field => {
        const td = document.createElement('td'); td.textContent = row.skills?.[field] || '—'; tr.append(td);
      });
    }
    body.append(tr);
  });
  table.append(body);
  target.replaceChildren(table);
}
function renderMergedStats() {
  const rows = mergedBankedRows();
  const statsHost = document.getElementById('mergedStatTable');
  const skillsHost = document.getElementById('mergedSkillTable');
  if (statsHost) fillStatTable(statsHost, rows, true);
  if (skillsHost) fillStatTable(skillsHost, rows, false);
}
function renderStatRoute(section) {"""
)

# Disable per-route editors; Stats tab is the merged view.
script = script.replace(
    "document.querySelectorAll('[data-stat-route]').forEach(section => {",
    "renderMergedStats();\ndocument.querySelectorAll('[data-stat-route]').forEach(section => {",
)
script = script.replace(
    """document.getElementById('toggleStatLock').addEventListener('click', () => {
  statLocked = !statLocked;
  applyStatLock();
});
applyStatLock();
document.getElementById('exportStats').addEventListener('click', () => {
  const quote = value => '"' + String(value ?? '').replaceAll('"', '""') + '"';
  const rows = [['Route', ...statNames, 'Rating', ...skillNames]];
  Object.entries(statLog).forEach(([route, characters]) => characters.forEach(row => {
    rows.push([route, ...statFields.map(field => row[field] ?? ''), statRating(row), ...skillFields.map(field => row.skills?.[field] ?? '')]);
  }));""",
    """function applyStatLock() { /* Merged Stats tab is read-only. */ }
document.getElementById('exportStats').addEventListener('click', () => {
  const quote = value => '"' + String(value ?? '').replaceAll('"', '""') + '"';
  const rows = [['Character', 'Classes', ...statNames.slice(2), 'Rating', ...skillNames]];
  mergedBankedRows().forEach(row => {
    rows.push([row.name, row.class, ...statFields.slice(2).map(field => row[field] ?? ''), statRating(row), ...skillFields.map(field => row.skills?.[field] ?? '')]);
  });""",
)

script += """
window.applyFortuneBackup = async function(obj) {
  const blob = new Blob([JSON.stringify(obj)], {type:'application/json'});
  const file = new File([blob], 'progress.json', {type:'application/json'});
  const data = new DataTransfer();
  data.items.add(file);
  backupFileInput.files = data.files;
  backupFileInput.dispatchEvent(new Event('change'));
};
"""

body_start = r'''</head>
<body>
<main>
<header>
  <div>
    <div class="kicker">Spoiler-light reference</div>
    <h1>Fortune's Weave — Leda &amp; Cai sheet</h1>
    <div class="subtitle">Gifts, Leda and Cai cycle missables, builds, Advanced classes, stats, and shared recruitment. Part I / II only — no later-arc story. Marks save in this browser. To move PCs, copy the HTML plus a progress JSON, or download the sheet with progress baked in.</div>
    <div class="backup-actions">
      <button type="button" id="exportBackup">Download progress JSON</button>
      <button type="button" id="importBackup">Import progress JSON</button>
      <button type="button" id="linkProgressFile">Use a progress file</button>
      <button type="button" id="exportSheet">Download sheet with progress</button>
      <input type="file" id="importBackupFile" accept=".json,application/json" hidden aria-label="Choose a Fortune's Weave progress backup">
      <span id="backupStatus" class="backup-status" role="status"></span>
    </div>
  </div>
  <button id="themeBtn" type="button">Light mode</button>
</header>

<nav class="tab-nav" role="tablist" aria-label="Cheat sheet sections">
  <button type="button" role="tab" id="tab-gifts" aria-controls="gifts" aria-selected="false" tabindex="-1">Gifts</button>
  <button type="button" role="tab" id="tab-cycles" aria-controls="cycles" aria-selected="false" tabindex="-1">Cycles</button>
  <button type="button" role="tab" id="tab-builds" aria-controls="buildGuide" aria-selected="false" tabindex="-1">Builds</button>
  <button type="button" role="tab" id="tab-classes" aria-controls="advClasses" aria-selected="false" tabindex="-1">Classes</button>
  <button type="button" role="tab" id="tab-stats" aria-controls="statLog" aria-selected="false" tabindex="-1">Stats</button>
  <button type="button" role="tab" id="tab-original" aria-controls="originalStats" aria-selected="false" tabindex="-1">Original stats</button>
  <button type="button" role="tab" id="tab-recruits" aria-controls="sharedPlanner" aria-selected="false" tabindex="-1">Shared recruits</button>
</nav>
'''

out = (
    header
    + "<style>\n"
    + css
    + css_extra
    + "\n</style>\n"
    + body_start
    + gifts
    + cycles
    + builds
    + "</main>\n<script>\n"
    + persist_js
    + "\n"
    + script
    + "\n</script>\n</body>\n</html>\n"
)
dst.write_text(out, encoding="utf-8")
Path("index.html").write_text(out, encoding="utf-8")
print(f"Wrote {dst} and index.html ({len(out):,} chars)")
