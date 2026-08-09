#!/usr/bin/env python3
"""
Builds docs/index.html from src/typescript-cheatsheet.md.

Run it locally with:   python3 src/build.py
Then commit the regenerated docs/ folder; GitHub Pages serves it directly.
"""

import html as htmlmod
import os
import re
import shutil
from datetime import date

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import widgets

# ----------------------------------------------------------------------
# CONFIG: change these two lines to your own repo, then rebuild.
# ----------------------------------------------------------------------
GITHUB_USER = "youvegotnigel"
REPO_NAME = "ts-for-testers"
SITE_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/"
# ----------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_MD = os.path.join(ROOT, "src", "typescript-cheatsheet.md")
OUT_DIR = os.path.join(ROOT, "docs")

PAGE_TITLE = "TypeScript for Test Automation Engineers"
PAGE_DESC = (
    "A free interactive TypeScript reference for QA engineers moving into "
    "Playwright. 31 sections covering types, interfaces, classes, generics, "
    "utility types, the Page Object Model and a visual guide to promises "
    "and flaky tests, with runnable examples."
)

# Section N of the Markdown maps to SLUGS[N - 1]. Adding a section means
# adding its slug here, in the same position.
SLUGS = [
    "what-is-typescript", "setup", "variables", "basic-types", "type-inference",
    "arrays-objects", "special-types", "functions", "interfaces", "type-aliases",
    "interface-vs-type", "unions-intersections", "narrowing", "enums", "classes-pom",
    "generics", "type-assertions", "optional-chaining", "modules", "utility-types",
    "async-await", "promises-flaky-tests", "modern-js", "tsconfig", "test-data-env",
    "playwright-patterns", "compiler-errors", "best-practices", "pitfalls",
    "exercises", "summary",
]
SECTION_COUNT = len(SLUGS)

LANG_LABEL = {
    "ts": "TypeScript", "typescript": "TypeScript",
    "js": "JavaScript", "javascript": "JavaScript",
    "bash": "Shell", "sh": "Shell",
    "json": "JSON", "jsonc": "JSON",
    "": "Text",
}
LANG_LEXER = {"jsonc": "js", "ts": "ts", "": "text"}

formatter = HtmlFormatter(nowrap=True, classprefix="")


def render_code(code, lang):
    try:
        lexer = get_lexer_by_name(LANG_LEXER.get(lang, lang) or "text")
    except Exception:
        lexer = get_lexer_by_name("text")
    body = highlight(code, lexer, formatter).rstrip("\n")
    label = LANG_LABEL.get(lang, lang.upper() or "Text")
    return (
        '<div class="codeblock hl">'
        '<div class="codebar"><span class="lang">' + label + "</span>"
        '<button class="copy" type="button">Copy</button></div>'
        "<pre><code>" + body + "</code></pre></div>"
    )


# GitHub style alerts: "> [!TIP]" on the first line of a blockquote.
# GitHub renders these natively, and here they tint the existing note style.
ALERT_CLASS = {"NOTE": "note", "TIP": "note tip", "WARNING": "note warn"}


def convert(body):
    """Markdown to HTML, with fenced code and figures pulled out first."""
    blocks = []

    def stash(html):
        blocks.append(html)
        return "\n\nBLOCKTOKEN%d\n\n" % (len(blocks) - 1)

    def stash_code(m):
        return stash(render_code(m.group(2), (m.group(1) or "").strip().lower()))

    def stash_widget(m):
        return stash(widgets.render(m.group(1), render_code))

    body = re.sub(r"```([a-zA-Z]*)\n(.*?)```", stash_code, body, flags=re.S)
    body = re.sub(r"^\[widget:([a-z0-9-]+)\][ \t]*$", stash_widget, body, flags=re.M)
    out = markdown.markdown(body, extensions=["tables", "sane_lists"])

    for i, blk in enumerate(blocks):
        out = out.replace("<p>BLOCKTOKEN%d</p>" % i, blk)

    out = re.sub(
        r"<blockquote>\s*<p>\[!(NOTE|TIP|WARNING)\]\s*",
        lambda m: '<blockquote class="%s">\n<p>' % ALERT_CLASS[m.group(1)],
        out,
    )
    out = out.replace("<table>", '<div class="table-scroll"><table>')
    out = out.replace("</table>", "</table></div>")
    out = re.sub(r'<a href="(https?://[^"]+)"',
                 r'<a href="\1" target="_blank" rel="noopener"', out)
    return out


def parse_sections(raw):
    sections = []
    for chunk in re.split(r"\n## ", raw)[1:]:
        head, _, body = chunk.partition("\n")
        if head.strip() == "Table of Contents":
            continue
        m = re.match(r"(\d+)\.\s*(.+)", head.strip())
        if not m:
            continue
        num, title = int(m.group(1)), m.group(2)
        body = body.replace("\n---\n", "\n")
        body = re.sub(r"\n\*Reference document for.*$", "", body, flags=re.S)
        sections.append({
            "num": "%02d" % num,
            "title": title,
            "slug": SLUGS[num - 1],
            "html": convert(body.strip()),
        })
    return sections


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="7" fill="#10151F"/>
<text x="16" y="22" font-family="ui-monospace,monospace" font-size="15"
      font-weight="700" fill="#E8A33D" text-anchor="middle">TS</text>
</svg>
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="author" content="__USER__">
<link rel="canonical" href="__URL__">
<link rel="icon" href="favicon.svg" type="image/svg+xml">

<meta property="og:type" content="article">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__URL__">
<meta property="og:site_name" content="__TITLE__">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESC__">

<meta name="theme-color" content="#10151F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>

<header class="topbar">
  <button class="icon-btn" id="menuBtn" type="button" aria-label="Show sections">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 4h12M2 8h12M2 12h12"/></svg>
  </button>
  <div class="brand">
    <span class="brand-mark">TS</span>
    <span class="brand-name">__TITLE__</span>
  </div>
  <div class="run-summary">
    <span class="stat stat-pass">\u2713 <b id="passCount">0</b> passed</span>
    <span class="stat stat-pend">\u25cb <b id="pendCount">__COUNT__</b> pending</span>
  </div>
  <a class="icon-btn" href="__REPO__" target="_blank" rel="noopener" aria-label="View the source on GitHub">
    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 .2a8 8 0 0 0-2.5 15.6c.4.1.5-.2.5-.4v-1.4c-2 .4-2.5-.5-2.7-1 0-.1-.5-.9-.9-1.1-.3-.2-.7-.6 0-.6.6 0 1 .6 1.2.8.7 1.2 1.8.9 2.3.7 0-.5.3-.9.5-1.1-1.8-.2-3.7-.9-3.7-4 0-.9.3-1.6.8-2.2 0-.2-.3-1 .1-2.1 0 0 .7-.2 2.2.8a7.4 7.4 0 0 1 4 0c1.5-1 2.2-.8 2.2-.8.4 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.2 0 3.1-1.9 3.8-3.7 4 .3.3.6.8.6 1.6v2.2c0 .2.1.5.5.4A8 8 0 0 0 8 .2Z"/></svg>
  </a>
  <button class="icon-btn" id="themeBtn" type="button" aria-label="Switch to light theme"></button>
</header>
<div class="rail"><div class="rail-fill" id="railFill"></div></div>

<div class="scrim"></div>

<nav class="sidebar" aria-label="Sections">
  <div class="search-wrap">
    <div class="search-field">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/></svg>
      <input id="search" type="search" placeholder="Search the reference" autocomplete="off" aria-label="Search the reference">
      <span class="kbd">/</span>
    </div>
  </div>
  <div class="runner-head">Running __COUNT__ specs</div>
  <ul class="speclist">__NAV__</ul>
  <div class="runner-foot" id="runnerFoot">
    <span id="footLabel">0/__COUNT__ specs passed</span>
    <button id="resetBtn" type="button">Reset run</button>
  </div>
</nav>

<main class="main">
  <div class="wrap">

    <div class="hero">
      <div class="console">
        <div><span class="prompt">$</span> <span class="cmd">npx playwright test</span> <span class="flag">--project=typescript-fundamentals</span></div>
        <div class="out">Running __COUNT__ specs with 1 worker<span class="caret"></span></div>
      </div>
      <h1>TypeScript for <em>test automation engineers</em></h1>
      <p class="lede">A working reference for QA engineers moving from manual testing, JavaScript, or Java into Playwright with TypeScript. Every example is written the way you would actually write it inside a framework. Free to read, free to fork, free to teach from.</p>
      <div class="hero-meta">
        <span class="chip"><b>__COUNT__</b> sections</span>
        <span class="chip">Playwright <b>+</b> TypeScript</span>
        <span class="chip">strict mode <b>on</b></span>
        <span class="chip">Node <b>20+</b></span>
        <span class="chip">Press <b>/</b> to search</span>
      </div>
    </div>

    __SPECS__

    <div class="noresults" id="noResults">
      <p>0 specs matched "<span id="queryEcho"></span>"</p>
      <span>Try a shorter term, like generics, fixture, enum, or await.</span>
    </div>

    <footer class="pagefoot">
      <span>Updated __DATE__</span>
      <span class="sep">|</span>
      <a href="typescript-cheatsheet.md" download>Download the Markdown</a>
      <span class="sep">|</span>
      <a href="__REPO__" target="_blank" rel="noopener">Source on GitHub</a>
      <span class="spacer"></span>
      <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>
    </footer>

  </div>
</main>

<button class="totop" id="toTop" type="button" aria-label="Back to top">
  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M8 13V3.5M3.8 7.7L8 3.4l4.2 4.3"/></svg>
</button>

<script>__JS__</script>
</body>
</html>
"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    sections = parse_sections(open(SRC_MD, encoding="utf-8").read())
    if len(sections) != SECTION_COUNT:
        raise SystemExit("Expected %d sections, found %d"
                         % (SECTION_COUNT, len(sections)))

    nav, specs = [], []
    for s in sections:
        fname = "%s-%s.spec.ts" % (s["num"], s["slug"])
        nav.append(
            '<li><a href="#%s"><span class="glyph">\u25cb</span>'
            '<span class="num">%s</span><span class="label">%s</span></a></li>'
            % (s["slug"], s["num"], htmlmod.escape(s["title"]))
        )
        specs.append(
            '<section class="spec" id="%s">'
            '<div class="spec-bar">'
            '<span class="spec-file"><span class="dot"></span>%s</span>'
            '<span class="pill">pending</span></div>'
            "<h2>%s</h2>"
            '<div class="prose">%s</div>'
            '<button class="markdone" type="button" aria-pressed="false">'
            '<span class="tick">\u25cb</span>'
            '<span class="markdone-label">Mark as passed</span></button>'
            "</section>"
            % (s["slug"], fname, htmlmod.escape(s["title"]), s["html"])
        )

    page = (TEMPLATE
            .replace("__CSS__", open(os.path.join(here, "style.css"), encoding="utf-8").read())
            .replace("__JS__", open(os.path.join(here, "app.js"), encoding="utf-8").read())
            .replace("__NAV__", "\n".join(nav))
            .replace("__SPECS__", "\n\n".join(specs))
            .replace("__TITLE__", PAGE_TITLE)
            .replace("__DESC__", PAGE_DESC)
            .replace("__URL__", SITE_URL)
            .replace("__REPO__", f"https://github.com/{GITHUB_USER}/{REPO_NAME}")
            .replace("__USER__", GITHUB_USER)
            .replace("__COUNT__", str(SECTION_COUNT))
            .replace("__DATE__", date.today().strftime("%d %B %Y")))

    if "BLOCKTOKEN" in page:
        raise SystemExit("A code block or widget token survived conversion. "
                         "Tokens must sit on their own line, with a blank "
                         "line either side.")

    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(OUT_DIR, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    open(os.path.join(OUT_DIR, ".nojekyll"), "w").write("")
    open(os.path.join(OUT_DIR, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % SITE_URL)
    open(os.path.join(OUT_DIR, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n</urlset>\n"
        % (SITE_URL, date.today().isoformat()))
    shutil.copyfile(SRC_MD, os.path.join(OUT_DIR, "typescript-cheatsheet.md"))

    print("Built %s" % os.path.join(OUT_DIR, "index.html"))
    print("  sections: %d" % len(sections))
    print("  size:     %d KB" % (len(page) // 1024))
    print("  site url: %s" % SITE_URL)


if __name__ == "__main__":
    main()
