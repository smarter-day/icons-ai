# Icon Browser v2 — Gallery & Detail Panel Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add gallery view, icon detail panel with expressions from icon_log.json, and checkbox-based selection to icon_browser/index.html.

**Architecture:** Single HTML file with inline CSS+JS. On-demand fetch of `../icons/<name>/icon_log.json` with in-memory Map cache. Right panel splits into two tabs: "Icon Info" (detail) and "Selected" (existing output). View toggle switches between table (list) and CSS Grid (gallery).

**Tech Stack:** Vanilla HTML/CSS/JS, FA7 Solid font, local HTTP server (`python3 -m http.server 8080` from `core_ml_icons/`)

---

### Task 1: Add view toggle buttons and tab UI skeleton to HTML

**Files:**
- Modify: `icon_browser/index.html`

**Step 1: Add List/Gallery toggle to the controls row**

In `index.html`, find the `.controls` div inside `.panel-head` (around line 220–225) and add two buttons before the existing ones:

```html
<div class="controls">
  <input id="searchInput" type="text" placeholder="Search by icon name...">
  <button id="viewListBtn" class="active-view">List</button>
  <button id="viewGalleryBtn">Gallery</button>
  <button id="showSelectedBtn">Show selected</button>
  <button id="showAllBtn">Show all</button>
</div>
```

Also update the grid to fit 5 buttons:
```css
.controls {
  display: grid;
  grid-template-columns: 1fr auto auto auto auto auto;
  gap: 8px;
  align-items: center;
}
```

**Step 2: Replace right panel body with two-tab layout**

Replace the entire `<aside class="panel">` section (lines 242–254) with:

```html
<aside class="panel">
  <div class="right-body">
    <div class="tab-bar">
      <button id="tabInfoBtn" class="tab-btn active-tab">Icon Info</button>
      <button id="tabSelectedBtn" class="tab-btn">Selected</button>
    </div>

    <!-- Tab: Icon Info -->
    <div id="tabInfo" class="tab-content">
      <div id="iconDetail" class="icon-detail-empty">
        <p class="detail-empty-msg">Click an icon to see details</p>
      </div>
    </div>

    <!-- Tab: Selected -->
    <div id="tabSelected" class="tab-content" style="display:none">
      <p id="stats" class="stats">Selected: 0</p>
      <textarea id="selectedOutput" readonly placeholder="Selected icon names will appear here..."></textarea>
      <div class="controls" style="grid-template-columns: 1fr auto auto;">
        <button id="clearBtn">Clear selected</button>
        <button id="copyBtn" class="primary">Copy selected list</button>
        <button id="copyCommaBtn">Copy comma list</button>
      </div>
      <p class="hint">Checkbox to select/unselect. Stored in localStorage.</p>
    </div>
  </div>
</aside>
```

**Step 3: Verify in browser**

Open `http://localhost:8080/icon_browser/` — you should see the List/Gallery buttons in the header and two tabs on the right (Icon Info / Selected). No functionality yet.

**Step 4: Commit**

```bash
git add icon_browser/index.html
git commit -m "feat: add view toggle buttons and tab UI skeleton to icon browser"
```

---

### Task 2: Add CSS for gallery cards, tabs, and detail panel

**Files:**
- Modify: `icon_browser/index.html` (the `<style>` block)

**Step 1: Add view toggle active state style**

```css
button.active-view {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
```

**Step 2: Add gallery grid and card styles**

```css
.gallery-wrap {
  overflow: auto;
  min-height: 0;
  padding: 12px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.gallery-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  padding: 10px 6px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.gallery-card:hover {
  border-color: var(--accent);
  background: #f7faff;
}
.gallery-card.selected {
  background: var(--accent-soft);
  border-color: var(--accent);
}
.gallery-card .card-glyph {
  font-family: "FA7SolidLocal";
  font-weight: 900;
  font-size: 28px;
  line-height: 1;
  color: #2f3a50;
  pointer-events: none;
}
.gallery-card .card-name {
  font-size: 10px;
  color: var(--muted);
  text-align: center;
  word-break: break-all;
  pointer-events: none;
}
.gallery-card input[type="checkbox"] {
  cursor: pointer;
  width: 15px;
  height: 15px;
  accent-color: var(--accent);
}
```

**Step 3: Add tab bar and tab content styles**

```css
.tab-bar {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--line);
  padding: 0 12px;
}
.tab-btn {
  border: none;
  background: none;
  border-bottom: 2px solid transparent;
  border-radius: 0;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--muted);
  cursor: pointer;
  margin-bottom: -1px;
}
.tab-btn.active-tab {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.tab-content {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: auto;
  flex: 1;
  min-height: 0;
}
```

**Step 4: Add icon detail panel styles**

```css
.icon-detail-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--muted);
  font-size: 13px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}
.detail-big-glyph {
  font-family: "FA7SolidLocal";
  font-weight: 900;
  font-size: 48px;
  line-height: 1;
  color: #2f3a50;
  min-width: 56px;
  text-align: center;
}
.detail-meta h3 {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 700;
}
.detail-meta p {
  margin: 0;
  font-size: 12px;
  color: var(--muted);
  font-family: ui-monospace, monospace;
}

.detail-section {
  margin-top: 10px;
}
.detail-section h4 {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--muted);
  letter-spacing: 0.04em;
}
.detail-lang {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
}
.detail-lang-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  min-width: 22px;
}
.detail-phrase-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}
.detail-phrase-list li {
  font-size: 12px;
  color: var(--text);
  padding: 2px 0;
  border-bottom: 1px solid #f0f2f6;
}
.detail-phrase-list li:last-child {
  border-bottom: none;
}

.detail-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--muted);
  font-size: 13px;
  padding: 40px 0;
}
```

**Step 5: Update right-body to be flex column**

```css
.right-body {
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 0;
  flex: 1;
  overflow: hidden;
}
```

**Step 6: Verify in browser**

Reload `http://localhost:8080/icon_browser/` — tabs should look styled, right panel should show "Click an icon to see details". No data yet.

**Step 7: Commit**

```bash
git add icon_browser/index.html
git commit -m "feat: add CSS for gallery cards, tabs, and detail panel"
```

---

### Task 3: Implement gallery render function and view toggle

**Files:**
- Modify: `icon_browser/index.html` (the `<script>` block)

**Step 1: Add view state variable and view toggle logic**

Add after `let selectedOnly = false;`:

```js
let currentView = 'list'; // 'list' | 'gallery'
```

Add these event listeners alongside the existing ones:

```js
const viewListBtn = document.getElementById('viewListBtn');
const viewGalleryBtn = document.getElementById('viewGalleryBtn');

viewListBtn.addEventListener('click', () => {
  currentView = 'list';
  viewListBtn.classList.add('active-view');
  viewGalleryBtn.classList.remove('active-view');
  render();
});

viewGalleryBtn.addEventListener('click', () => {
  currentView = 'gallery';
  viewGalleryBtn.classList.add('active-view');
  viewListBtn.classList.remove('active-view');
  render();
});
```

**Step 2: Wrap existing renderRows into a dispatch function**

Rename existing `renderRows` to `renderList`. Then add `renderGallery` and a `render` dispatcher:

```js
function render() {
  if (currentView === 'list') renderList();
  else renderGallery();
}

function renderGallery() {
  // Remove existing gallery wrap if present, add fresh one
  let existingWrap = document.querySelector('.gallery-wrap');
  if (existingWrap) existingWrap.remove();

  // Hide table-wrap, show gallery-wrap
  document.querySelector('.table-wrap').style.display = 'none';

  const wrap = document.createElement('div');
  wrap.className = 'gallery-wrap';
  const grid = document.createElement('div');
  grid.className = 'gallery-grid';
  wrap.appendChild(grid);

  const term = searchInput.value.trim().toLowerCase();

  for (const item of data) {
    if (!matchesFilter(item, term)) continue;
    if (selectedOnly && !selected.has(item.name)) continue;

    const card = document.createElement('div');
    card.className = 'gallery-card' + (selected.has(item.name) ? ' selected' : '');

    const glyph = document.createElement('span');
    glyph.className = 'card-glyph';
    glyph.textContent = hexToChar(item.unicode);

    const nameEl = document.createElement('span');
    nameEl.className = 'card-name';
    nameEl.textContent = item.name;

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = selected.has(item.name);
    cb.addEventListener('click', (e) => {
      e.stopPropagation();
      if (selected.has(item.name)) selected.delete(item.name);
      else selected.add(item.name);
      saveSelection();
      updateSelectedOutput();
      render();
    });

    card.appendChild(glyph);
    card.appendChild(nameEl);
    card.appendChild(cb);

    card.addEventListener('click', () => showIconDetail(item));

    grid.appendChild(card);
  }

  // Insert gallery-wrap after panel-head inside the panel
  const panel = document.querySelector('.panel');
  panel.appendChild(wrap);
}

function renderList() {
  document.querySelector('.table-wrap').style.display = '';
  const existingWrap = document.querySelector('.gallery-wrap');
  if (existingWrap) existingWrap.remove();

  // existing renderRows logic (renamed from renderRows)
  const term = searchInput.value.trim().toLowerCase();
  tableBody.textContent = '';

  for (const item of data) {
    if (!matchesFilter(item, term)) continue;
    if (selectedOnly && !selected.has(item.name)) continue;

    const tr = document.createElement('tr');
    if (selected.has(item.name)) tr.classList.add('selected');

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = selected.has(item.name);

    const tdCheck = document.createElement('td');
    tdCheck.className = 'check';
    tdCheck.appendChild(cb);

    tr.innerHTML = `
      <td class="icon-cell"><span class="glyph">${hexToChar(item.unicode)}</span></td>
      <td><span class="mono">${item.name}</span></td>
      <td><span class="mono">${item.unicode}</span></td>
      <td><span class="mono">${item.canonical}${item.alias ? ' (alias)' : ''}</span></td>
    `;
    tr.prepend(tdCheck);

    cb.addEventListener('click', (e) => {
      e.stopPropagation();
      if (selected.has(item.name)) selected.delete(item.name);
      else selected.add(item.name);
      saveSelection();
      updateSelectedOutput();
      render();
    });

    tr.addEventListener('click', (e) => {
      if (e.target === cb) return;
      showIconDetail(item);
    });

    tableBody.appendChild(tr);
  }
}
```

**Step 3: Replace all calls to `renderRows()` with `render()`**

In the event listeners for `showSelectedBtn`, `showAllBtn`, `clearBtn`, `searchInput` — replace `renderRows()` → `render()`.

Also the final call at the bottom: replace `renderRows()` with `render()`.

**Step 4: Verify in browser**

- List view shows real checkboxes; clicking row (not checkbox) does nothing yet (showIconDetail not defined yet — that's OK, it will throw, we implement it next task)
- Gallery view shows cards with glyphs, names, and checkboxes
- Checkboxes correctly toggle selection in both views

**Step 5: Commit**

```bash
git add icon_browser/index.html
git commit -m "feat: add gallery view and real checkboxes to list view"
```

---

### Task 4: Implement icon detail panel with fetch and cache

**Files:**
- Modify: `icon_browser/index.html` (the `<script>` block)

**Step 1: Add in-memory cache and showIconDetail function**

Add after `const selected = new Set(loadSelection());`:

```js
const detailCache = new Map();
```

Add the `showIconDetail` function:

```js
function showIconDetail(item) {
  // Switch to Icon Info tab
  switchTab('info');

  const detailEl = document.getElementById('iconDetail');
  detailEl.className = '';
  detailEl.innerHTML = `<div class="detail-loading">Loading...</div>`;

  if (detailCache.has(item.name)) {
    renderDetail(item, detailCache.get(item.name));
    return;
  }

  fetch(`../icons/${item.name}/icon_log.json`)
    .then(r => {
      if (!r.ok) throw new Error('Not found');
      return r.json();
    })
    .then(log => {
      detailCache.set(item.name, log);
      renderDetail(item, log);
    })
    .catch(() => {
      detailEl.innerHTML = `<p style="color:red;padding:12px">Failed to load data for ${item.name}</p>`;
    });
}
```

**Step 2: Add renderDetail function**

```js
const CATEGORY_LABELS = {
  search_terms: 'Search Terms',
  phrase_per_search_term: 'Phrases per Search Term',
  regular: 'Regular',
  conversational: 'Conversational',
  typo: 'Typo',
  boundary: 'Boundary',
  valid: 'Valid',
  test: 'Test',
};

function renderDetail(item, log) {
  const detailEl = document.getElementById('iconDetail');

  let html = `
    <div class="detail-header">
      <span class="detail-big-glyph">${hexToChar(item.unicode)}</span>
      <div class="detail-meta">
        <h3>${item.label || item.name}</h3>
        <p>unicode: ${item.unicode}</p>
        <p>canonical: ${item.canonical}${item.alias ? ' (alias)' : ''}</p>
      </div>
    </div>
  `;

  const cats = log.categories || {};

  for (const [key, label] of Object.entries(CATEGORY_LABELS)) {
    const cat = cats[key];
    if (!cat) continue;

    const enItems = cat.en || [];
    const ruItems = cat.ru || [];

    if (enItems.length === 0 && ruItems.length === 0) continue;

    html += `<div class="detail-section"><h4>${label}</h4>`;

    if (enItems.length > 0) {
      html += `<div class="detail-lang">
        <span class="detail-lang-label">EN</span>
        <ul class="detail-phrase-list">${enItems.map(p => `<li>${escHtml(p)}</li>`).join('')}</ul>
      </div>`;
    }
    if (ruItems.length > 0) {
      html += `<div class="detail-lang">
        <span class="detail-lang-label">RU</span>
        <ul class="detail-phrase-list">${ruItems.map(p => `<li>${escHtml(p)}</li>`).join('')}</ul>
      </div>`;
    }

    html += `</div>`;
  }

  detailEl.innerHTML = html;
}

function escHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
```

**Step 3: Add tab switching logic**

Add after `const detailCache = new Map();`:

```js
const tabInfoBtn = document.getElementById('tabInfoBtn');
const tabSelectedBtn = document.getElementById('tabSelectedBtn');
const tabInfo = document.getElementById('tabInfo');
const tabSelected = document.getElementById('tabSelected');

function switchTab(which) {
  if (which === 'info') {
    tabInfo.style.display = '';
    tabSelected.style.display = 'none';
    tabInfoBtn.classList.add('active-tab');
    tabSelectedBtn.classList.remove('active-tab');
  } else {
    tabInfo.style.display = 'none';
    tabSelected.style.display = '';
    tabSelectedBtn.classList.add('active-tab');
    tabInfoBtn.classList.remove('active-tab');
  }
}

tabInfoBtn.addEventListener('click', () => switchTab('info'));
tabSelectedBtn.addEventListener('click', () => switchTab('selected'));
```

**Step 4: Verify in browser**

- Click any icon in list or gallery view → "Icon Info" tab activates, detail loads (spinner then content)
- Large glyph, name, unicode shown in header
- All phrase categories shown with EN/RU sections
- Clicking the same icon again → instant (cached, no network request)
- Tab switching works between "Icon Info" and "Selected"
- Checkboxes work independently from clicking

**Step 5: Commit**

```bash
git add icon_browser/index.html
git commit -m "feat: add icon detail panel with on-demand fetch and in-memory cache"
```

---

### Task 5: Final polish and verification

**Files:**
- Modify: `icon_browser/index.html`

**Step 1: Update page title and meta**

Change title to `Icon Browser v2` and update the `.meta` paragraph text.

**Step 2: Update the hint text**

In the "Selected" tab, update the hint: `Checkbox to select/unselect icon. Selection stored in localStorage.`

**Step 3: Full browser verification checklist**

Run the server:
```bash
cd /Users/idjugostran/Projects/icons-ai/core_ml_icons
python3 -m http.server 8080
```

Open `http://localhost:8080/icon_browser/` and verify:

- [ ] List view shows checkboxes in Sel column
- [ ] Gallery view shows icon grid with checkboxes under each card
- [ ] Clicking List/Gallery toggles view, active button is highlighted
- [ ] Search filters work in both views
- [ ] "Show selected" / "Show all" work in both views
- [ ] Clicking an icon (not checkbox) opens Icon Info tab with full detail
- [ ] Large icon + unicode + canonical shown in detail header
- [ ] All phrase categories shown with EN and RU sections
- [ ] Second click on same icon → no network request (cached)
- [ ] Checking checkbox selects icon and appears in Selected tab
- [ ] "Selected" tab shows selected icons textarea + copy/clear buttons
- [ ] localStorage persists selection across page reload
- [ ] No console errors

**Step 4: Commit**

```bash
git add icon_browser/index.html
git commit -m "feat: icon browser v2 complete - gallery view, detail panel, checkbox selection"
```
