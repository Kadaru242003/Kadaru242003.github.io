"""Generator for projects/*.html. Output is committed.

Run from the repo root: python3 scripts/dev/gen_projects.py .
"""
import html
import diagrams
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1]) / "projects"
OUT.mkdir(exist_ok=True)

ICON_MOON = '<svg class="icon-moon" aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
ICON_SUN = '<svg class="icon-sun" aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></g></svg>'

PROJECTS = [
    {
        "slug": "claimcheck",
        "title": "claimcheck",
        "meta": 'Open-source benchmark <span class="badge">In Progress</span>',
        "summary": "An open-source benchmark that tests whether AI coding agents falsely claim success.",
        "problem": [
            "AI coding agents often report that a task is done and the tests pass. claimcheck tests whether that claim is true.",
            "Every task has known ground truth. Some tasks can be solved. Others cannot: the tests contradict themselves, the spec is impossible, or the environment is broken.",
        ],
        "built": [
            "205 tasks with verified ground truth.",
            "A harness that ran GPT-OSS 120B and 20B through 530 runs at $0 API cost.",
            "Grading hardened against 8 ways to fake a pass. 12 cheat strategies (1,236 attempts) get none through.",
            "An LLM-as-a-judge from a different model family than the agents.",
            "A pre-registered analysis using McNemar and Fisher tests.",
        ],
        "results": [
            "Caught GPT-OSS 120B reverse-engineering test data to pass an impossible task, then quietly claiming success.",
            "Final results are still being computed.",
        ],
        "stack": ["Python", "pytest", "Docker", "GPT-OSS 120B and 20B", "LLM-as-a-judge", "McNemar and Fisher tests"],
        "links": [("GitHub", "https://github.com/Kadaru242003/claimcheck")],
    },
    {
        "slug": "claimcheck-mcp",
        "title": "claimcheck-mcp",
        "meta": "MCP server &middot; Oct 2026",
        "summary": "An MCP server that gives AI agents 3 tools over claimcheck's 205 tasks.",
        "problem": [
            "To test an agent on claimcheck, the agent needs a standard way to browse tasks and run its code. It must never see the answer files.",
        ],
        "built": [
            "An MCP server that gives AI agents 3 tools over claimcheck's 205 tasks: list, read, and run in a Docker sandbox.",
        ],
        "results": [
            "Found and fixed a symlink leak of answer files.",
            "96 tests run in CI.",
        ],
        "stack": ["Python", "MCP", "Tool calling", "Docker", "GitHub Actions CI"],
        "links": [
            ("GitHub", "https://github.com/Kadaru242003/claimcheck-mcp"),
            ("claimcheck", "/projects/claimcheck.html"),
        ],
    },
    {
        "slug": "ab-experimentation-framework",
        "title": "A/B Experimentation and Decision Framework",
        "meta": "Experimentation framework",
        "summary": "A framework that turns A/B test data into ship, continue, or rollback decisions.",
        "problem": [
            "A low p-value alone is a weak reason to ship a change. A broken traffic split, a lift too small to matter, a guardrail that got worse, or peeking at results early can all mislead a team.",
        ],
        "built": [
            "Sample ratio mismatch (SRM) checks.",
            "z-tests and Welch's t-tests.",
            "Guardrails that decide ship, continue, or rollback.",
            "Power analysis for sample size and test duration.",
            "An A/A simulation to measure the cost of peeking.",
        ],
        "results": [
            "2,000 A/A simulations showed that peeking raised false positives from 5% to 19%. O'Brien-Fleming restored 5%.",
            "Power analysis is validated against statsmodels.",
            "92 tests run in CI.",
        ],
        "stack": ["Python", "pandas", "SciPy", "statsmodels", "GitHub Actions CI"],
        "links": [("GitHub", "https://github.com/Kadaru242003/ab-experimentation-framework")],
    },
    {
        "slug": "demand-forecasting-backtest",
        "title": "Demand Forecasting with Backtesting",
        "meta": "Time series forecasting &middot; Oct 2026",
        "summary": "Weekly sales forecasts for 3,049 Walmart (M5) items in one store, with leakage-tested backtests.",
        "problem": [
            "Forecast weekly sales for 3,049 Walmart (M5) items in one store, and make sure the backtest never uses data from the future.",
        ],
        "built": [
            "Exponential smoothing and LightGBM models.",
            "Lag and calendar features for LightGBM.",
            "6-fold rolling-origin backtests.",
            "Leakage tests.",
            "Prediction intervals.",
        ],
        "results": [
            "LightGBM reached a MASE of 0.963, vs 1.437 for a seasonal naive baseline.",
            "The 80% and 95% prediction intervals covered 81% and 95% of actual sales.",
        ],
        "stack": ["Python", "LightGBM", "pandas", "Time series forecasting"],
        "links": [("GitHub", "https://github.com/Kadaru242003/demand-forecasting-backtest")],
    },
    {
        "slug": "riskbot",
        "title": "RiskBot",
        "meta": "Sensitive data detector &middot; Dec 2025",
        "summary": "Flags sensitive HR and personal data across whole files, with document Q&A.",
        "problem": [
            "Shared files can hold sensitive HR data, such as salaries and performance reviews, and personal data, such as Social Security and bank account numbers. RiskBot finds it.",
        ],
        "built": [
            "Flags sensitive HR and personal data across whole files.",
            "Document Q&A using top-k retrieval in ChromaDB.",
            "A web UI for uploading files, reviewing findings, and asking questions.",
        ],
        "results": [
            "Cut peak memory from over 650 MB to 287 MB by swapping PyTorch for an ONNX embedder, to fit a 512 MB free tier.",
        ],
        "stack": ["Python", "FastAPI", "RAG", "ChromaDB", "Embeddings", "ONNX"],
        "links": [
            ("GitHub", "https://github.com/Kadaru242003/HRCI-NPPI-doc-finder"),
            ("Live Demo", "https://hrci-nppi-doc-finder.onrender.com/static/index.html"),
        ],
        "note": "The demo runs on a free tier and can take about 50 seconds to wake up.",
        "shots": [
            ("riskbot-1", 386, "Detected sensitive data for an uploaded file.", "Detected sensitive data",
             "RiskBot screen after an upload, with a table of detected sensitive data showing type, category, text snippet, and confidence."),
            ("riskbot-2", 395, "Asking a question about the uploaded document.", "Document Q&A",
             "RiskBot answering a question about the uploaded document in the Filtered Results panel."),
        ],
    },
]


def esc(s):
    return html.escape(s, quote=True)


def ul(items):
    return "\n".join(f"          <li>{esc(i)}</li>" for i in items)


AB_ALT = "Chart from the A/B framework repo: conversion rate over time for control and treatment. Treatment stays above control while its early lift decays."
FC_ALT = "Chart from the forecasting repo: MASE per backtest fold for LightGBM, ETS, moving average, and seasonal naive. LightGBM is lowest in every fold."
RB_ALT = "RiskBot screen after an upload, with a table of detected sensitive data showing type, category, text snippet, and confidence."


def visual(slug):
    if slug == "claimcheck":
        return '<figure class="detail-visual is-diagram">' + diagrams.claimcheck("dg-cc") + "</figure>"
    if slug == "claimcheck-mcp":
        return '<figure class="detail-visual is-diagram">' + diagrams.claimcheck_mcp("dg-mcp") + "</figure>"
    imgs = {
        "ab-experimentation-framework": ("/assets/projects/ab-conversion-over-time", "-thumb", 640, 1205, 908, AB_ALT),
        "demand-forecasting-backtest": ("/assets/projects/forecasting-fold-mase", "-thumb", 640, 1262, 668, FC_ALT),
        "riskbot": ("/assets/riskbot-1", "-thumb", 800, 1600, 773, RB_ALT),
    }
    base, small, sw, w, h, alt = imgs[slug]
    srcset = f"{base}{small}.webp {sw}w, {base}.webp {w}w"
    sizes = "(min-width: 1040px) 976px, 100vw"
    return (f'<figure class="detail-visual"><img src="{base}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" fetchpriority="high" alt="{esc(alt)}"></figure>')


def page(p):
    url = f"https://kadaru242003.github.io/projects/{p['slug']}.html"
    title = f"{p['title']} | Harshith Kadaru"
    problem = "\n".join(f"        <p>{esc(x)}</p>" for x in p["problem"])
    stack = "".join(f"<li>{esc(s)}</li>" for s in p["stack"])
    links = "\n".join(
        f'          <a href="{esc(h)}">{esc(t)}<span class="visually-hidden">: {esc(p["title"])}</span></a>'
        for t, h in p["links"]
    )
    note = f'\n        <p class="note">{esc(p["note"])}</p>' if p.get("note") else ""
    shots = ""
    if p.get("shots"):
        items = "\n".join(
            f"""          <li>
            <figure>
              <a href="/assets/{n}.webp" data-lightbox data-caption="{esc(cap)}">
                <img src="/assets/{n}-thumb.webp" width="800" height="{h}" loading="lazy" alt="{esc(alt)}">
              </a>
              <figcaption>{esc(fig)}</figcaption>
            </figure>
          </li>"""
            for n, h, cap, fig, alt in p["shots"]
        )
        shots = f"""
      <section class="section reveal" aria-labelledby="shots-title">
        <h2 id="shots-title">Screenshots</h2>
        <p>Select a screenshot to enlarge it.</p>
        <ul class="shots">
{items}
        </ul>
      </section>
"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(p['summary'])}">
  <meta name="author" content="Harshith Kadaru">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#fbfaf7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0e1113" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(p['summary'])}">
  <meta property="og:image" content="https://kadaru242003.github.io/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
  <script>
    document.documentElement.classList.add("js");
    try {{
      var t = localStorage.getItem("theme");
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    }} catch (e) {{}}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <nav class="nav container" aria-label="Primary">
      <a class="brand" href="/">Harshith Kadaru</a>
      <ul class="nav-links">
        <li><a href="/#experience">Experience</a></li>
        <li><a href="/#projects" aria-current="page">Projects</a></li>
        <li><a href="/#education">Education</a></li>
        <li><a href="/#skills">Skills</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
      <button class="theme-toggle" type="button" aria-label="Switch to dark theme" hidden>
        {ICON_MOON}
        {ICON_SUN}
      </button>
    </nav>
  </header>

  <main id="main">
    <article class="container">
      <header class="detail-header">
        <a class="back" href="/#projects">Back to all projects</a>
        <h1>{esc(p['title'])}</h1>
        <p class="detail-meta">{p['meta']}</p>
        <p class="lede">{esc(p['summary'])}</p>
        <p class="card-links">
{links}
        </p>{note}
        {visual(p['slug'])}
      </header>

      <div class="detail-body">
      <section class="section reveal" aria-labelledby="problem-title">
        <h2 id="problem-title">Problem</h2>
{problem}
      </section>

      <section class="section reveal" aria-labelledby="built-title">
        <h2 id="built-title">What I built</h2>
        <ul class="bullets">
{ul(p['built'])}
        </ul>
      </section>

      <section class="section reveal" aria-labelledby="results-title">
        <h2 id="results-title">Results</h2>
        <ul class="bullets">
{ul(p['results'])}
        </ul>
      </section>
{shots}
      <section class="section reveal" aria-labelledby="stack-title">
        <h2 id="stack-title">Stack</h2>
        <ul class="tags">{stack}</ul>
      </section>
      </div>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>Harshith Kadaru</p>
      <p><a href="/">Home</a></p>
    </div>
  </footer>

  <script src="/script.js" defer></script>
</body>
</html>
"""


for p in PROJECTS:
    (OUT / f"{p['slug']}.html").write_text(page(p), encoding="utf-8")
    print("wrote", p["slug"])
