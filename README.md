# Brevin Blalock — Developer Site

Portfolio plus the privacy policies, terms, and support pages for all my App Store apps. Served by GitHub Pages at https://brevinb.github.io.

## Layout

| URL | What it is |
|---|---|
| `/` | Portfolio home |
| `/apps/<slug>/` | App page: App Store link + legal & support links |
| `/apps/<slug>/privacy/` | Privacy policy (use this as the App Store Connect **Privacy Policy URL**) |
| `/apps/<slug>/terms/` | Terms of service, where the app has one |
| `/apps/<slug>/support/` | Support page (use this as the App Store Connect **Support URL**) |
| `/privacy/`, `/support/` | Index of every app's docs |

Slugs: `tub-pirates`, `fridgecig`, `gomoku`, `memorizeit`, `ink-well-keeper`, `quietquest`, `scriptureai`, `extramile`, `prtracker`.

## Editing

Everything except `assets/site.css` and `icons/` is generated — edit the sources, then rebuild:

```sh
python3 build.py
python3 -m http.server 8765   # preview at http://localhost:8765
```

- **`_src/apps.json`** — app list (order = newest first), ratings, taglines, contact email, and which docs each app has.
- **`_src/content/<slug>/{privacy,terms,support}.html`** — the documents, as HTML fragments without a title. An app with no `support.html` gets a generated support page using its contact email.
- **`_src/about.html`** — the "About the work" blurb on the home page.

**Shipping a new app:** add an entry to `apps.json`, drop its icon (320×320 PNG) in `icons/`, add its `privacy.html` under `_src/content/<slug>/`, rebuild, commit.

`_src/`, `build.py`, and this README are excluded from the published site via `_config.yml`. All links are relative, so moving to a custom domain needs only a `CNAME` file.
