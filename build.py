#!/usr/bin/env python3
"""Generate the site from _src/.

    python3 build.py

Reads _src/apps.json and the per-app legal documents in _src/content/<slug>/
(privacy.html, terms.html, support.html — HTML fragments without a title) and
writes index.html, apps/<slug>/…, privacy/, support/ and 404.html.
Everything links relatively, so the site works on brevinb.github.io or any
custom domain without changes.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_src"
APPS = json.loads((SRC / "apps.json").read_text())

SITE_NAME = "Brevin Blalock"
CONTACT_EMAIL = "bblalock313@gmail.com"
APP_STORE_DEV = "https://apps.apple.com/us/developer/brevin-blalock/id1649097120"
GITHUB = "https://github.com/brevinb"
LINKEDIN = "https://www.linkedin.com/in/brevinb"
DOC_TITLES = {"privacy": "Privacy Policy", "terms": "Terms of Service", "support": "Support"}
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve"]

e = html.escape


def doc_title(app, doc):
    return app.get("termsTitle", DOC_TITLES[doc]) if doc == "terms" else DOC_TITLES[doc]


def app_docs(app):
    """Every app gets a support page; one is generated when there is no custom one."""
    docs = list(app["docs"])
    return docs if "support" in docs else docs + ["support"]


def stars(rating):
    return f'<span class="star">★</span> {rating:.1f}'


def page(title, description, body, root):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<div class="page">
{body}
  <footer>
    <p><a href="{root}">{SITE_NAME}</a> · <a href="{root}privacy/">Privacy</a> · <a href="{root}support/">Support</a></p>
  </footer>
</div>
</body>
</html>
"""


def write(rel_path, content):
    out = ROOT / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)


def doc_links(app, root):
    base = f"{root}apps/{app['slug']}/"
    return "".join(f'<a href="{base}{d}/">{doc_title(app, d)}</a>' for d in app_docs(app))


def legal_index(root):
    rows = "\n".join(f"""    <li class="cell compact">
      <img src="{root}icons/{app['icon']}" alt="">
      <div>
        <h3><a href="{root}apps/{app['slug']}/">{e(app['name'])}</a></h3>
        <p class="doc-links">{doc_links(app, root)}</p>
      </div>
    </li>""" for app in APPS)
    return f'  <ul class="group">\n{rows}\n  </ul>'


def build_home():
    count = NUMBER_WORDS[len(APPS)]
    dock = "\n".join(
        f'    <a href="{e(a["appStore"])}" target="_blank" rel="noopener">'
        f'<img src="icons/{a["icon"]}" alt="{e(a["short"])} app icon"></a>' for a in APPS)
    cells = "\n".join(f"""    <li class="cell">
      <img src="icons/{a['icon']}" alt="">
      <div>
        <h2><a href="apps/{a['slug']}/">{e(a['name'])}</a></h2>
        <p class="tagline">{e(a['tagline'])}</p>
        <p class="meta">{e(a['category'])} · {stars(a['rating'])} · Shipped {a['year']}</p>
      </div>
      <a class="view" href="{e(a['appStore'])}" target="_blank" rel="noopener" aria-label="View {e(a['short'])} on the App Store">View</a>
    </li>""" for a in APPS)
    first_year = min(a["year"] for a in APPS)
    body = f"""  <header>
    <p class="eyebrow">iOS Developer</p>
    <h1>{SITE_NAME}</h1>
    <p class="subtitle"><strong>{count.capitalize()} apps on the App Store</strong> — each one designed, built, and shipped end-to-end by one person.</p>
    <nav class="links" aria-label="Contact">
      <a class="link-pill" href="mailto:{CONTACT_EMAIL}">Email</a>
      <a class="link-pill" href="{APP_STORE_DEV}" target="_blank" rel="noopener">App&nbsp;Store</a>
      <a class="link-pill" href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
      <a class="link-pill" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
    </nav>
  </header>

  <div class="dock" aria-label="App icons">
{dock}
  </div>

  <p class="stats">{len(APPS)} apps shipped · {stars(AVERAGE_RATING)} average across all ratings · shipping since {first_year}</p>

  <h2 class="section-header">Apps — newest first</h2>
  <ul class="group">
{cells}
  </ul>

  <h2 class="section-header">About the work</h2>
  <div class="about">
{ABOUT_HTML}
  </div>

  <h2 class="section-header" id="legal">Privacy, terms &amp; support</h2>
{legal_index("")}
"""
    write("index.html", page(f"{SITE_NAME} — iOS Developer",
                             f"{SITE_NAME} is an iOS developer with {count} apps designed, built, and shipped solo on the App Store.",
                             body, ""))


def build_app(app):
    root = "../../"
    rows = "\n".join(f'    <a class="row-link" href="{d}/"><span>{doc_title(app, d)}</span><span class="chevron">›</span></a>'
                     for d in app_docs(app))
    body = f"""  <a class="back" href="{root}">‹ All apps</a>
  <header class="app-head">
    <img src="{root}icons/{app['icon']}" alt="{e(app['short'])} app icon">
    <div>
      <h1>{e(app['name'])}</h1>
      <p class="subtitle">{e(app['subtitle'])}</p>
      <p class="meta">{e(app['category'])} · {stars(app['rating'])} · Since {app['year']}</p>
    </div>
  </header>
  <p class="app-tagline">{e(app['tagline'])}</p>
  <nav class="links">
    <a class="link-pill primary" href="{e(app['appStore'])}" target="_blank" rel="noopener">View on the App&nbsp;Store</a>
  </nav>

  <h2 class="section-header">Legal &amp; support</h2>
  <nav class="group" aria-label="{e(app['short'])} documents">
{rows}
    <a class="row-link" href="mailto:{e(app['email'])}"><span>Contact</span><span class="detail">{e(app['email'])}</span></a>
  </nav>
"""
    write(f"apps/{app['slug']}/index.html",
          page(f"{app['short']} — {SITE_NAME}", f"{app['name']}: {app['tagline']}", body, root))


def generated_support(app):
    return f"""<h2>Contact</h2>
<p>Need help with {e(app['short'])}, found a bug, or have an idea? Email <a href="mailto:{e(app['email'])}">{e(app['email'])}</a>. Including your device model and iOS version helps me sort things out faster.</p>
<h2>Purchases &amp; subscriptions</h2>
<ul>
<li><strong>Restore purchases:</strong> use the Restore option on the app's upgrade screen, signed in with the same Apple ID you bought with.</li>
<li><strong>Cancel a subscription:</strong> manage it in <a href="https://apps.apple.com/account/subscriptions">your Apple ID subscriptions</a>.</li>
<li><strong>Refunds:</strong> Apple handles all payments; request one at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</li>
</ul>
"""


def build_doc(app, doc):
    root = "../../../"
    src = SRC / "content" / app["slug"] / f"{doc}.html"
    content = src.read_text() if src.exists() else generated_support(app)
    title = doc_title(app, doc)
    others = " · ".join(f'<a href="../{d}/">{doc_title(app, d)}</a>' for d in app_docs(app) if d != doc)
    body = f"""  <a class="back" href="../">‹ {e(app['short'])}</a>
  <header>
    <p class="eyebrow">{e(app['name'])}</p>
    <h1>{title}</h1>
  </header>
  <article class="prose">
{content}  </article>
  <p class="section-footer">{others}{' · ' if others else ''}Contact: <a href="mailto:{e(app['email'])}">{e(app['email'])}</a></p>
"""
    write(f"apps/{app['slug']}/{doc}/index.html",
          page(f"{title} — {app['short']}", f"{title} for {app['name']} on iOS.", body, root))


def build_hub(slug, title, intro):
    root = "../"
    body = f"""  <a class="back" href="{root}">‹ {SITE_NAME}</a>
  <header>
    <p class="eyebrow">{SITE_NAME}</p>
    <h1>{title}</h1>
    <p class="subtitle">{intro}</p>
  </header>
  <h2 class="section-header">Apps</h2>
{legal_index(root)}
"""
    write(f"{slug}/index.html", page(f"{title} — {SITE_NAME}", intro, body, root))


def build_404():
    body = f"""  <header>
    <p class="eyebrow">404</p>
    <h1>Page not found</h1>
    <p class="subtitle">That page doesn't exist. Looking for an app's privacy policy or support page? They're all listed below.</p>
  </header>
  <h2 class="section-header">Apps</h2>
{legal_index("/")}
"""
    # 404.html is served from any path, so it links from the site root.
    write("404.html", page(f"Not found — {SITE_NAME}", "Page not found.", body, "/"))


AVERAGE_RATING = 0.0
ABOUT_HTML = (SRC / "about.html").read_text().rstrip()


def main():
    global AVERAGE_RATING
    rated = [a for a in APPS if a.get("ratingCount")]
    AVERAGE_RATING = sum(a["rating"] * a["ratingCount"] for a in rated) / sum(a["ratingCount"] for a in rated)

    shutil.rmtree(ROOT / "apps", ignore_errors=True)
    build_home()
    for app in APPS:
        build_app(app)
        for doc in app_docs(app):
            build_doc(app, doc)
    build_hub("privacy", "Privacy", "Privacy policies and terms for every app I've published. Each app has its own policy — pick the one you're using.")
    build_hub("support", "Support", "Need help with one of my apps? Pick it below for FAQs, purchase help, and the right email to reach me.")
    build_404()
    print(f"Built {len(APPS)} apps.")


if __name__ == "__main__":
    main()
