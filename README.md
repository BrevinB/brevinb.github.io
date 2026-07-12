# Brevin Blalock — Portfolio

A single-page portfolio site listing all 8 App Store apps. No build step, no dependencies — just `index.html` and an `icons/` folder.

## Preview locally

```sh
open index.html
```

## Host it for free

**GitHub Pages** (recommended — gives you `https://<username>.github.io`):

```sh
cd portfolio
git init && git add -A && git commit -m "Portfolio site"
gh repo create <username>.github.io --public --source=. --push
```

Then in the repo: Settings → Pages → deploy from the `main` branch. The site goes live at `https://<username>.github.io` in about a minute. (Name the repo anything else and it lives at `https://<username>.github.io/<repo>` instead.)

**Netlify Drop** (fastest): go to https://app.netlify.com/drop and drag this folder in.

## Customizing

- **Contact links** — Email (bblalock313@gmail.com), App Store, GitHub, and LinkedIn pills live in `index.html` under `<nav class="links">`.
- **App data** — names, taglines, ratings, and years are plain HTML in the `<ul class="group">` list. When you ship a new app, copy a `<li class="cell">` block, drop its icon in `icons/`, and update the stats line under the icon dock.
