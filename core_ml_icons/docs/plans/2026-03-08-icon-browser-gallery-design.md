# Icon Browser v2 — Gallery View & Detail Panel

**Date:** 2026-03-08
**Status:** Approved

## Summary

Improve `icon_browser/index.html` with:
1. Gallery view (in addition to existing list view)
2. Detail panel on the right showing icon expressions from `icon_log.json`
3. Checkboxes for selection (click = details, checkbox = select)
4. Two-tab right panel: "Icon Info" and "Selected"

## Architecture

### Left Panel — View Toggle

Header adds **List / Gallery** toggle buttons alongside search and show selected/all buttons.

**List view** (existing table, modified):
- `Sel` column: real `<input type="checkbox">` instead of ✓ symbol
- Row click (excluding checkbox): loads detail into right panel "Icon Info" tab
- Checkbox click: toggles icon selection

**Gallery view** (new CSS Grid):
- ~5–6 cards per row, responsive
- Each card: glyph icon (clickable) + name label + checkbox at bottom
- Card click (excluding checkbox): loads detail and switches to "Icon Info" tab
- Checkbox: toggles selection independently

### Right Panel — Two Tabs

**"Icon Info" tab:**
- Large glyph icon + name + unicode + canonical
- Sections from `icon_log.json` categories (each EN / RU):
  - Search Terms
  - Phrases per Search Term
  - Regular
  - Conversational
  - Typo
  - Boundary
  - Valid
  - Test
- Loading spinner while fetching
- Empty state when no icon selected

**"Selected" tab:**
- Existing functionality: textarea with selected names, Copy (newline), Copy (comma), Clear

### Data Loading

- Fetch on demand: `fetch('../icons/${name}/icon_log.json')`
- In-memory cache via `Map` — no duplicate requests on re-click
- Server: `python3 -m http.server 8080` from `core_ml_icons/` root

## File Changes

- `icon_browser/index.html` — single file, all CSS and JS inline

## Non-Goals

- No changes to `icons-data.js` generation scripts
- No backend or build tooling
- No multi-language toggle UI (EN and RU shown together)
