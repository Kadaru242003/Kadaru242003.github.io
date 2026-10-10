# kadaru242003.github.io

Personal portfolio of Harshith Kadaru, served at https://kadaru242003.github.io.

Plain HTML, CSS, and a few lines of JavaScript (the light / dark theme toggle). No build step.

## Files

| File | Purpose |
|---|---|
| `index.html` | The page: About, Experience, Projects, Skills, Contact |
| `styles.css` | Styles, light and dark themes |
| `script.js` | Theme toggle (the site follows the system theme without it) |
| `404.html` | Not found page |
| `favicon.svg`, `og-image.png` | Tab icon and social preview image |
| `robots.txt`, `sitemap.xml` | Search engine basics |
| `resume.pdf` | Not yet added. The site links to `/resume.pdf` |
| `lychee.toml` | Link checker settings |
| `.htmlvalidate.json` | HTML validator settings |
| `.github/workflows/site.yml` | Checks and deployment |

## Checks and deployment

`.github/workflows/site.yml` runs on every pull request, every push to `main`, and weekly:

- **HTML validity**: html-validate and the W3C Nu HTML Checker, plus a check that no file contains an em dash.
- **Broken links**: lychee checks every link on the page. LinkedIn is skipped because it blocks automated requests.

On a push to `main`, if both checks pass, the site is deployed to GitHub Pages.

## Adding the resume

Add `resume.pdf` to the repository root, then delete the `'resume\.pdf$',` line from `lychee.toml` so the link is checked.

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
