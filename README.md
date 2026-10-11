# kadaru242003.github.io

Personal portfolio of Harshith Kadaru, served at https://kadaru242003.github.io.

Plain HTML, CSS, and a small script (theme toggle and screenshot lightbox). No build step.

## Files

| File | Purpose |
|---|---|
| `index.html` | Home page: Experience, Projects, Achievements, Education, Skills, Contact |
| `projects/*.html` | One detail page per project: problem, what I built, results, stack, links |
| `assets/` | Headshot and RiskBot screenshots (`*-thumb.webp` on cards, `*.webp` in the lightbox, `*.png` originals are not deployed) |
| `styles.css` | Styles, light and dark themes |
| `script.js` | Theme toggle and screenshot lightbox (without JavaScript the site follows the system theme and screenshots open as plain images) |
| `404.html` | Not found page |
| `favicon.svg`, `og-image.png` | Tab icon and social preview image |
| `robots.txt`, `sitemap.xml` | Search engine basics |
| `resume.pdf` | Resume, linked from the hero and Contact |
| `docs/screenshots/` | Full-page screenshots for pull requests (not deployed) |
| `lychee.toml` | Link checker settings |
| `.htmlvalidate.json` | HTML validator settings |
| `.github/workflows/site.yml` | Checks and deployment |

## Checks and deployment

`.github/workflows/site.yml` runs on every pull request, every push to `main`, and weekly:

- **HTML validity**: html-validate and the W3C Nu HTML Checker, plus a check that no file contains an em dash.
- **Broken links**: lychee checks every link on the page. LinkedIn is skipped because it blocks automated requests.

On a push to `main`, if both checks pass, the site is deployed to GitHub Pages.

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
