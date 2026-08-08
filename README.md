# TypeScript for Test Automation Engineers

A free, interactive TypeScript reference for QA engineers moving into Playwright.

**Read it here:** https://youvegotnigel.github.io/ts-for-testers/

30 sections covering types, interfaces, classes, generics, utility types, the Page Object Model, and the TypeScript patterns that actually show up in a test framework. Every example is written the way you would write it inside a real suite.

No build tooling to install, no dependencies at runtime, no tracking, no paywall.

---

## What is in it

| | |
|---|---|
| **Sections** | 30, from "what is TypeScript" to a one page summary |
| **Code examples** | 97, all Playwright and TypeScript flavoured |
| **Search** | Filters sections instantly, press `/` from anywhere |
| **Progress** | Mark sections as passed and watch the run summary fill |
| **Themes** | Dark and light, with hand tuned syntax colours for both |
| **Offline** | CSS, JavaScript and syntax highlighting are inlined into `index.html`. The only external request is the IBM Plex web font, which falls back to system fonts with no network |

The page is built around a single idea: it behaves like a test run. Each section is a spec file with a status, the sidebar is runner output, and clearing all 30 prints a completion line like a real runner.

---

## Publish your own copy in five minutes

You do not need a paid plan. GitHub Pages is free for public repositories.

### The fast path, no CI

1. Create a new **public** repository on GitHub. Name it whatever you like, for example `ts-for-testers`.
2. Push this folder to it:
   ```bash
   git init
   git add .
   git commit -m "Add TypeScript cheat sheet"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```
3. In the repository, go to **Settings** then **Pages**.
4. Under **Build and deployment**, set **Source** to `Deploy from a branch`, then choose branch `main` and folder `/docs`. Save.
5. Wait about a minute. Your site is live at `https://YOUR-USERNAME.github.io/YOUR-REPO/`.

That is it. The `docs/` folder is already built and committed, so nothing else needs to run.

### Keeping it up to date

There is no CI workflow in this repository. Editing the content is a local loop:

1. Edit `src/typescript-cheatsheet.md`.
2. Run `python3 src/build.py` to regenerate `docs/index.html`.
3. Commit both the source and the rebuilt `docs/` and push. Pages redeploys from the branch.

If you would rather have GitHub Actions rebuild on every push, add your own workflow that installs `src/requirements.txt`, runs `python3 src/build.py`, and publishes `docs/`, then set **Source** to `GitHub Actions` under Settings then Pages.

### Point it at your own repo

Open `src/build.py` and change the two lines at the top:

```python
GITHUB_USER = "youvegotnigel"
REPO_NAME   = "ts-for-testers"
```

These drive the canonical URL, the social preview metadata, the sitemap, and the GitHub link in the header. Rebuild after changing them.

---

## Editing the content

`src/typescript-cheatsheet.md` is the single source of truth. The rules the build script relies on:

- Each section starts with `## N. Title`, numbered from 1.
- Section numbers must line up with the `SLUGS` list in `src/build.py`. Adding a section means adding a slug.
- Fenced code blocks should carry a language: `ts`, `js`, `bash`, `json`, or `jsonc`.
- Tables use standard Markdown pipe syntax.

Then rebuild:

```bash
pip3 install -r src/requirements.txt
python3 src/build.py
```

The script prints the section count and output size, and fails loudly if it does not find exactly 30 sections. That guard is deliberate: a malformed heading silently dropping a section is the failure mode most likely to slip through.

### Preview locally

```bash
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000.

---

## Repository layout

```
.
├── docs/                       the published site, GitHub Pages serves this
│   ├── index.html              generated, do not edit by hand
│   ├── typescript-cheatsheet.md  downloadable copy of the source
│   ├── favicon.svg
│   ├── robots.txt
│   ├── sitemap.xml
│   └── .nojekyll               tells Pages to skip Jekyll processing
├── src/                        source of truth
│   ├── typescript-cheatsheet.md  the content
│   ├── build.py                Markdown to HTML build
│   ├── style.css               design system
│   ├── app.js                  search, progress, copy, theme
│   └── requirements.txt
└── README.md
```

---

## Design notes

- **Type** is IBM Plex Sans and IBM Plex Mono. IBM built Plex for technical documentation, and the mono face carries all the structural chrome: section numbers, spec filenames, status pills.
- **Colour** follows CI build semantics, which QA engineers already read fluently. Amber is the accent, green means passed and nothing else, red is reserved for pitfalls. Green never decorates, so it always carries state.
- **Syntax highlighting** is baked in at build time with Pygments rather than a runtime JavaScript library. That keeps the page dependency free and working offline.
- **Progress is session only.** A test run does not persist, and neither does this. There is a Reset run button for a fresh pass.

---

## Contributing

Corrections and additions are welcome. Open an issue, or send a pull request against `src/typescript-cheatsheet.md`. Please keep examples short, runnable, and grounded in something a tester would actually write.

---

## License

The written content is licensed under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). The code examples, build script, stylesheet, and JavaScript are licensed under MIT. See [LICENSE](LICENSE).

In short: use it, fork it, translate it, teach from it, use it in your own onboarding. Just keep the attribution.
