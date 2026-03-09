# Local Icon Browser

This folder is fully standalone and does not require external services.

## Files
- `index.html` - local UI for viewing and selecting icons
- `icons-data.js` - icon names and unicode for the current semantic set
- `assets/fa-solid-900.woff2` - local solid Font Awesome webfont

## Running the dev server

Use `serve.py` instead of `python3 -m http.server` — it adds `no-cache` headers so Chrome always loads the latest data.

**From the `core_ml_icons/` directory:**

```bash
python3 icon_browser/serve.py 8080
```

Then open: **http://localhost:8080/icon_browser/**

> The server must be started from `core_ml_icons/`, not from inside `icon_browser/`.
> This is because the browser fetches icon data from `../icons/<name>/icon_log.json`,
> which resolves to `core_ml_icons/icons/` — outside the `icon_browser/` folder.

**Custom port:**

```bash
python3 icon_browser/serve.py 9000
```

## Notes
- Data source used for generation: `icons.enabled.en.semantic.life.v7_compact4.json`
- Icon training data lives in `../icons/<name>/` (train_en.csv, valid_en.csv, test_en.csv, icon_log.json)
