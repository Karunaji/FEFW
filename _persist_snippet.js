const STAT_KEY = 'fw-stat-log-v1';
const PLANNER_KEY = 'fw-shared-recruits-v1';

if (localStorage.getItem('fw-tab-v2-classes') !== '1') {
  const priorTab = Number(localStorage.getItem('fw-tab'));
  if (Number.isInteger(priorTab) && priorTab >= 3) {
    localStorage.setItem('fw-tab', String(priorTab + 1));
  }
  localStorage.setItem('fw-tab-v2-classes', '1');
}

function persistSoon() {
  clearTimeout(persistSoon.timer);
  persistSoon.timer = setTimeout(() => { writeProgressFile(); }, 400);
}

function setBackupStatus(message) {
  const el = document.getElementById('backupStatus');
  if (el) el.textContent = message;
}

let progressFileHandle = null;

function collectStorage() {
  const storage = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && key.startsWith('fw-')) storage[key] = localStorage.getItem(key);
  }
  document.querySelectorAll('input.persist').forEach(cb => {
    storage['fw-check-' + cb.id] = cb.checked ? '1' : '0';
  });
  document.querySelectorAll('details.persist-open[data-persist-open]').forEach(el => {
    storage['fw-open-' + el.dataset.persistOpen] = el.open ? '1' : '0';
  });
  storage['fw-theme'] = document.documentElement.classList.contains('light') ? 'light' : 'dark';
  const activeTab = [...document.querySelectorAll('.tab-nav [role="tab"]')].findIndex(tab => tab.getAttribute('aria-selected') === 'true');
  if (activeTab >= 0) storage['fw-tab'] = String(activeTab);
  const giftSearch = document.getElementById('giftSearch');
  if (giftSearch) storage['fw-gift-search'] = giftSearch.value;
  const plannerSearch = document.getElementById('plannerSearch');
  if (plannerSearch) storage['fw-planner-search'] = plannerSearch.value;
  const plannerSort = document.getElementById('plannerSort');
  if (plannerSort) storage['fw-planner-sort'] = plannerSort.value;
  const plannerPending = document.getElementById('plannerPending');
  if (plannerPending) storage['fw-planner-pending'] = plannerPending.checked ? '1' : '0';
  const plannerShowHidden = document.getElementById('plannerShowHidden');
  if (plannerShowHidden) storage['fw-planner-show-hidden'] = plannerShowHidden.checked ? '1' : '0';
  if (typeof statLog !== 'undefined') storage[STAT_KEY] = JSON.stringify(statLog);
  if (typeof plannerState !== 'undefined') storage[PLANNER_KEY] = JSON.stringify(plannerState);
  return storage;
}

function applyStoredDetails() {
  document.querySelectorAll('details.persist-open[data-persist-open]').forEach(el => {
    const saved = localStorage.getItem('fw-open-' + el.dataset.persistOpen);
    if (saved === '1') el.open = true;
    else if (saved === '0') el.open = false;
  });
}

function openHandleDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('fw-progress-file', 1);
    req.onupgradeneeded = () => req.result.createObjectStore('handles');
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function rememberProgressHandle(handle) {
  progressFileHandle = handle;
  try {
    const db = await openHandleDb();
    await new Promise((resolve, reject) => {
      const tx = db.transaction('handles', 'readwrite');
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
      tx.objectStore('handles').put(handle, 'progress');
    });
    db.close();
  } catch (_) { /* IndexedDB unavailable — still write this session */ }
}

async function restoreProgressHandle() {
  try {
    const db = await openHandleDb();
    const handle = await new Promise((resolve, reject) => {
      const tx = db.transaction('handles', 'readonly');
      const req = tx.objectStore('handles').get('progress');
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
    db.close();
    if (!handle) return;
    const query = await handle.queryPermission({ mode: 'readwrite' });
    if (query !== 'granted') {
      const next = await handle.requestPermission({ mode: 'readwrite' });
      if (next !== 'granted') return;
    }
    progressFileHandle = handle;
    setBackupStatus('Linked progress file is ready. Copy that JSON with this HTML when you switch PCs.');
  } catch (_) { /* no stored handle */ }
}

async function writeProgressFile() {
  if (!progressFileHandle) return;
  try {
    const backup = {app:'fortunes-weave-quick-sheet', formatVersion:1, exportedAt:new Date().toISOString(), storage: collectStorage()};
    const writable = await progressFileHandle.createWritable();
    await writable.write(JSON.stringify(backup, null, 2));
    await writable.close();
    setBackupStatus('Saved to progress file.');
  } catch (error) {
    setBackupStatus(`Could not write progress file: ${error.message}`);
  }
}

(function hydrateEmbeddedProgress() {
  const el = document.getElementById('fw-embedded-progress');
  if (!el) return;
  const raw = el.textContent.trim();
  if (!raw) return;
  try {
    const backup = JSON.parse(raw);
    if (backup?.app !== 'fortunes-weave-quick-sheet' || !backup.storage) return;
    const hasLocal = Object.keys(localStorage).some(key => key.startsWith('fw-'));
    if (hasLocal) return;
    Object.entries(backup.storage).forEach(([key, value]) => {
      if (key.startsWith('fw-') && typeof value === 'string') localStorage.setItem(key, value);
    });
  } catch (_) { /* ignore a bad embed */ }
})();

document.querySelectorAll('details.persist-open[data-persist-open]').forEach(el => {
  el.addEventListener('toggle', () => {
    localStorage.setItem('fw-open-' + el.dataset.persistOpen, el.open ? '1' : '0');
    persistSoon();
  });
});
applyStoredDetails();

const ledaRoute = document.getElementById('route-leda');
const caiRoute = document.getElementById('route-cai');
document.getElementById('openLedaOnly')?.addEventListener('click', () => {
  ledaRoute.open = true; caiRoute.open = false; persistSoon();
});
document.getElementById('openCaiOnly')?.addEventListener('click', () => {
  caiRoute.open = true; ledaRoute.open = false; persistSoon();
});
document.getElementById('openBothRoutes')?.addEventListener('click', () => {
  ledaRoute.open = true; caiRoute.open = true; persistSoon();
});

document.getElementById('linkProgressFile')?.addEventListener('click', async () => {
  if (!window.showOpenFilePicker && !window.showSaveFilePicker) {
    setBackupStatus('This browser cannot keep a linked file. Use Download all progress, then Import on the other PC.');
    return;
  }
  try {
    if (window.showOpenFilePicker) {
      const [handle] = await window.showOpenFilePicker({
        types: [{description: "Fortune's Weave progress", accept: {'application/json': ['.json']}}],
        multiple: false
      });
      await rememberProgressHandle(handle);
      const file = await handle.getFile();
      const text = (await file.text()).trim();
      if (text && window.applyFortuneBackup) await window.applyFortuneBackup(JSON.parse(text));
      else await writeProgressFile();
      setBackupStatus('Using progress file. Copy that JSON with this HTML when you switch PCs.');
      return;
    }
  } catch (error) {
    if (error && error.name === 'AbortError') return;
  }
  try {
    const handle = await window.showSaveFilePicker({
      suggestedName: 'fortunes_weave_progress.json',
      types: [{description: "Fortune's Weave progress", accept: {'application/json': ['.json']}}]
    });
    await rememberProgressHandle(handle);
    await writeProgressFile();
    setBackupStatus('Created progress file. Copy it with this HTML to another PC.');
  } catch (inner) {
    if (inner && inner.name !== 'AbortError') setBackupStatus(`Could not link a file: ${inner.message}`);
  }
});

document.getElementById('exportSheet')?.addEventListener('click', () => {
  try {
    const backup = {app:'fortunes-weave-quick-sheet', formatVersion:1, exportedAt:new Date().toISOString(), storage: collectStorage()};
    const root = document.documentElement.cloneNode(true);
    let tag = root.querySelector('#fw-embedded-progress');
    if (!tag) {
      tag = document.createElement('script');
      tag.type = 'application/json';
      tag.id = 'fw-embedded-progress';
      const firstScript = root.querySelector('script:not([type]), script[type="text/javascript"]');
      firstScript ? firstScript.parentNode.insertBefore(tag, firstScript) : root.querySelector('body').append(tag);
    }
    tag.textContent = JSON.stringify(backup);
    const html = '<!doctype html>\n' + root.outerHTML;
    const url = URL.createObjectURL(new Blob([html], {type:'text/html;charset=utf-8'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'fortunes_weave_reference.html';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setBackupStatus('Downloaded this sheet with progress baked in. Open that copy on the other PC.');
  } catch (error) {
    setBackupStatus(`Could not export the sheet: ${error.message}`);
  }
});

restoreProgressHandle();

(function initAdvSkillsToggle() {
  const panel = document.getElementById('advClasses');
  const btn = document.getElementById('advSkillsToggle');
  if (!panel || !btn) return;
  const apply = (collapsed) => {
    panel.classList.toggle('skills-collapsed', collapsed);
    panel.querySelectorAll('.adv-group th').forEach(th => { th.colSpan = collapsed ? 11 : 12; });
    btn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    btn.textContent = collapsed ? 'Show skills' : 'Hide skills';
    localStorage.setItem('fw-adv-skills', collapsed ? '1' : '0');
  };
  apply(localStorage.getItem('fw-adv-skills') === '1');
  btn.addEventListener('click', () => {
    apply(!panel.classList.contains('skills-collapsed'));
    persistSoon();
  });
})();
