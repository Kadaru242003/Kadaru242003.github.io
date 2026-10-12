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
        "meta": "Open-source benchmark &middot; Oct 2026",
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
            "Without running tests, GPT-OSS 120B falsely claimed success on 58/102 unsolvable tasks (57%) and GPT-OSS 20B on 61/101 (60%).",
            "With tests, 5/36 (14%) and 8/36 (22%). Both drops are 42 points (exact McNemar p = 0.0015 and 0.00028), significant after a Bonferroni correction for 6 planned tests.",
            "Model size made no significant difference (p = 0.33 blind, p = 0.55 with tests).",
            "Without running tests, models claimed success on 46/46 and 45/46 broken-environment tasks, but only 9/50 and 13/49 impossible ones. A broken environment only shows up when something runs.",
            "Both models reverse-engineered the test data of one impossible task to make it pass, then claimed success without saying how. The grader and the judge both caught it.",
            "The LLM judge (Qwen 27B, a different model family) matched ground truth on 96% of 322 runs (Cohen's kappa 0.90).",
            "A DistilBERT model fine-tuned in PyTorch flagged false success claims with 91% accuracy (5-fold cross-validation split by task), the same as a TF-IDF baseline (92%, p = 0.66).",
        ],
        "limits": "Two models from one family, on short Python tasks written for this benchmark. Agent runs cover 60 tasks per model, so their intervals are wide.",
        "stack": ["Python", "pytest", "Docker", "GPT-OSS 120B and 20B", "LLM-as-a-judge", "McNemar and Fisher tests"],
        "links": [("GitHub", "https://github.com/Kadaru242003/claimcheck")],
    },
    {
        "slug": "ml-model-monitoring",
        "title": "ML Model Service with Drift Monitoring",
        "meta": "Oct 2026",
        "summary": "A LightGBM model that predicts hotel booking cancellations, served with FastAPI in Docker, with every prediction logged to SQLite.",
        "problem": [
            "A hotel wants a cancellation probability for each booking, to plan overbooking and staffing. Drift monitoring is supposed to warn you when a model starts to fail. I tested whether it actually does.",
        ],
        "built": [
            "Time-based split on the Hotel Booking Demand dataset (two hotels in Portugal, 2015 to 2017). Removed leaking columns that are recorded after booking, such as reservation_status and booking_changes.",
            "Logistic regression baseline and a LightGBM model, tuned on an inner time split inside the training year, not on validation.",
            "FastAPI service in Docker with input validation, prediction logging to SQLite, and a labels endpoint.",
            "Monthly and weekly drift monitoring with PSI, KS, and chi-square tests.",
            "A simulation that injects known shifts to measure each detector's detection rate and false alarm rate.",
        ],
        "results": [
            "Validation ROC AUC 0.878 for LightGBM vs 0.849 for logistic regression.",
            "Production AUC held near validation until June 2017, then fell to 0.782 in July and 0.760 in August 2017.",
            "Every alarm rule had precision near 0.29, the share of degraded weeks. Drift scores did not predict the drop.",
            "The share of Non Refund bookings tracked the drop (weekly Spearman -0.84). These bookings are easy to rank, so when they fell, AUC fell.",
            "At n = 1000, a lead_time shift of SMD 0.10 was caught by KS in 58% of trials and by PSI >= 0.1 in 0%.",
            "Single prediction latency in Docker: p50 16.5 ms, p95 23.5 ms, measured on a local build.",
        ],
        "lesson": "On this data, drift scores help explain a change after the fact, but they are not a reliable alarm. Watching labeled performance by segment works better.",
        "stack": ["Python", "LightGBM", "scikit-learn", "FastAPI", "Docker", "SQLite", "GitHub Actions CI"],
        "links": [("GitHub", "https://github.com/Kadaru242003/ml-model-monitoring")],
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
            "Hybrid detection: checksum rules for SSNs, card numbers (Luhn) and routing numbers (ABA), and GPT-OSS 120B for HR data.",
            "Grounding: LLM findings whose snippet is not in the file are dropped and counted.",
            "Masked values in every answer, automatic deletion after 24 hours, upload limits, and no sensitive data in logs.",
            "Document Q&A using top-k retrieval in ChromaDB, with category questions answered from the stored findings.",
            "A labeled synthetic benchmark of 48 documents, with labels written before any detector and a held-out half never tuned on.",
        ],
        "results": [
            "On the 24 held-out documents (131 labels), the hybrid scored F1 0.97 (precision 0.95, recall 0.99).",
            "The LLM alone scored F1 0.98 and the rules alone 0.74; the rules cover structured NPPI only, not HR data.",
            "Cut peak memory from over 650 MB to 287 MB by swapping PyTorch for an ONNX embedder, to fit a 512 MB free tier.",
            "Over 200 tests in CI, including browser tests that render malicious answers harmlessly.",
        ],
        "lesson": "Here the rules added consistency, not accuracy. The LLM's findings varied between runs on the same file, while the rules find structured NPPI the same way every time.",
        "limits": "The benchmark is synthetic and template-generated, so its scores overstate real-world accuracy. The LLM was measured once per document.",
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


FC_ALT = "Chart from the forecasting repo: MASE per backtest fold for LightGBM, ETS, moving average, and seasonal naive. LightGBM is lowest in every fold."
MM_ALT = "Monthly ROC AUC from October 2016 to August 2017"
RB_ALT = "RiskBot screen after an upload, with a table of detected sensitive data showing type, category, text snippet, and confidence."


def visual(slug):
    if slug == "claimcheck":
        return '<figure class="detail-visual is-diagram">' + diagrams.claimcheck_results_chart("ch-cc") + "</figure>"
    if slug == "claimcheck-mcp":
        return '<figure class="detail-visual is-diagram">' + diagrams.claimcheck_mcp("dg-mcp") + "</figure>"
    if slug == "ab-experimentation-framework":
        return '<figure class="detail-visual is-diagram">' + diagrams.ab_framework("dg-ab") + "</figure>"
    imgs = {
        "ml-model-monitoring": ("/assets/projects/monitoring-auc-over-time", "-thumb", 640, 990, 418, MM_ALT),
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
    limits = ""
    if p.get("limits"):
        limits = f"""
      <section class="section reveal" aria-labelledby="limits-title">
        <h2 id="limits-title">Limits</h2>
        <p>{esc(p["limits"])}</p>
      </section>
"""
    lesson = ""
    if p.get("lesson"):
        lesson = f"""
      <section class="section reveal" aria-labelledby="lesson-title">
        <h2 id="lesson-title">Lesson</h2>
        <p>{esc(p["lesson"])}</p>
      </section>
"""
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
{lesson}{limits}{shots}
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
