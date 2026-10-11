"""Assemble the deployable site in _site/.

Copies the static files and, when a contributions JSON file is given and exists,
replaces the <!-- github-activity --> marker in index.html with a GitHub activity
section whose graph is a static inline SVG. Without the JSON, the marker is left
as an HTML comment and the page renders without the section. Standard library only.

Usage: python3 scripts/build.py [contributions.json]
"""
import datetime
import html
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
MARKER = "<!-- github-activity -->"
LOGIN = "Kadaru242003"

FILES = ["index.html", "404.html", "styles.css", "script.js", "favicon.svg", "og-image.png",
         "robots.txt", "sitemap.xml", "resume.pdf"]
ASSET_PATTERNS = ["*.jpg", "*.webp", "*.woff2", "*.txt"]

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def copy_site():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in FILES:
        shutil.copy2(ROOT / name, OUT / name)
    shutil.copytree(ROOT / "projects", OUT / "projects")
    for pattern in ASSET_PATTERNS:
        for src in (ROOT / "assets").rglob(pattern):
            dest = OUT / src.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def graph_svg(cal):
    cell, step, left, top = 11, 14, 4, 18
    weeks = cal["weeks"]
    width = left + len(weeks) * step
    height = top + 7 * step
    parts = []
    last_month = None
    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            date = datetime.date.fromisoformat(day["date"])
            row = (date.weekday() + 1) % 7  # Sunday first, like GitHub
            level = LEVELS.get(day["contributionLevel"], 0)
            parts.append(f'<rect class="l{level}" x="{left + wi * step}" y="{top + row * step}" '
                         f'width="{cell}" height="{cell}" rx="2"/>')
        first = datetime.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != last_month and wi < len(weeks) - 2:
            parts.append(f'<text x="{left + wi * step}" y="11">{MONTHS[first.month - 1]}</text>')
            last_month = first.month
    total = cal["totalContributions"]
    label = f"GitHub contributions graph for {LOGIN}: {total} contributions in the last year"
    return (f'<svg class="gh-graph" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>')


def activity_section(cal):
    total = cal["totalContributions"]
    return f"""<section class="section container reveal" id="github" aria-labelledby="github-title">
      <h2 id="github-title">GitHub Activity</h2>
      <div class="gh-panel">
        <p class="gh-total">{total:,} contributions in the last year</p>
        <section class="gh-scroll" tabindex="0" aria-label="GitHub contributions graph, scrollable">
          {graph_svg(cal)}
        </section>
        <p class="card-links"><a href="https://github.com/{LOGIN}">github.com/{LOGIN}</a></p>
      </div>
    </section>"""


def main():
    copy_site()
    data = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
    index = OUT / "index.html"
    text = index.read_text(encoding="utf-8")
    if MARKER not in text:
        sys.exit("index.html is missing the github-activity marker")
    if data and data.exists():
        cal = json.loads(data.read_text(encoding="utf-8"))
        text = text.replace(MARKER, activity_section(cal))
        index.write_text(text, encoding="utf-8")
        print(f"Built _site with GitHub activity ({cal['totalContributions']} contributions)")
    else:
        print("Built _site without GitHub activity (no contributions data)")


if __name__ == "__main__":
    main()
