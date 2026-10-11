# Updating the site

A step-by-step guide for editing this site by hand, on github.com or in VS Code.

The site is plain HTML and CSS. There is no build step. Whatever is on the `main` branch is what goes live, after the checks pass.

**Contents**

1. [Change text on the home page](#1-change-text-on-the-home-page)
2. [Add a new project](#2-add-a-new-project)
3. [Add and convert images](#3-add-and-convert-images)
4. [Replace the resume](#4-replace-the-resume)
5. [The CI checks and how to fix failures](#5-the-ci-checks-and-how-to-fix-failures)
6. [Preview the site locally](#6-preview-the-site-locally)

**Two ways to edit**

- **On github.com:** open the file, click the pencil icon (Edit), make the change, then click **Commit changes**. For anything more than a typo, choose **Create a new branch** and open a pull request. The checks then run before anything goes live.
- **In VS Code:** clone the repo, edit, commit, and push. Use **Find in Files** (Ctrl+Shift+F, or Cmd+Shift+F on a Mac) to search the whole repo.

---

## 1. Change text on the home page

All home page text is in **`index.html`**, at the repo root.

1. Open `index.html`.
2. Search (Ctrl+F) for a few words of the text you want to change.
3. Edit only the words between the tags. Leave the `<...>` tags and `class="..."` alone.
4. Commit.

Where each part lives (search for these strings):

| Part of the page | Search for |
|---|---|
| Tagline under your name | `class="lede"` |
| Resume, GitHub, LinkedIn, Email buttons | `class="actions"` |
| Experience | `id="experience"` |
| Projects (cards) | `id="projects"` |
| Achievements | `id="achievements"` |
| Education | `id="education"` |
| Skills | `id="skills"` |
| Contact | `id="contact"` |
| Text shown in Google results and link previews | `name="description"` and `og:description` near the top |

Tips:

- An ampersand must be written as `&amp;` (for example `Q&amp;A`). The dot between items is `&middot;`.
- **To add an experience bullet:** copy an existing `<li>...</li>` line inside the same `<ul class="bullets">` and change its text.
- **To add a whole job:** copy one complete `<li class="entry">` block, from `<li class="entry">` to its matching `</li>`, and paste it where it belongs. The list is newest first.

**Project detail pages** (`projects/*.html`) are generated from `scripts/dev/gen_projects.py`. To change text on a detail page, see [Editing an existing project page](#editing-an-existing-project-page).

---

## 2. Add a new project

A project has three parts:

1. a card in `index.html`,
2. a detail page in `projects/<slug>.html`,
3. a line in `sitemap.xml`.

Pick a short **slug** first, using lowercase letters and hyphens, for example `my-new-project`. The detail page will be `projects/my-new-project.html`.

### Step 1: Add the image (if any)

Follow [section 3](#3-add-and-convert-images) to put these files in `assets/projects/`:

- `my-new-project-figure.png` (the source)
- `my-new-project-figure.webp` (full size)
- `my-new-project-figure-thumb.webp` (640 pixels wide)

### Step 2: Add the card to the home page

1. Open `index.html` and search for `class="cards"`. Each project card is one `<li class="card">` block.
2. Copy a card that has an image, for example the **ML Model Service with Drift Monitoring** card. Copy from its `<li class="card">` to its matching `</li>`.
3. Paste it where the new project should appear. The order on the page is the order in the file.
4. In the pasted copy, change:
   - the `src`, `width`, `height`, and `alt` of the `<img>`, to match your thumbnail (see [section 3](#3-add-and-convert-images)),
   - the title inside `<h3>`,
   - the date inside `<span class="card-date">`,
   - the paragraph text,
   - the tags (one `<li>` per tag),
   - both links: `Details` points to `/projects/my-new-project.html`, and `GitHub` points to the repo.
5. In both links, also change the hidden text after the colon (`<span class="visually-hidden">: ...</span>`) to the new project name. Screen readers read it out.

### Step 3: Make the detail page

Choose one of the two options below. Don't mix them.

**Option A (recommended): use the generator.** You need Python 3, which you run in a terminal on your computer.

1. Open `scripts/dev/gen_projects.py`.
2. The `PROJECTS` list holds one `{ ... }` block per project, in page order. Copy a whole block, for example the one with `"slug": "ml-model-monitoring"`, and paste it where you want the new one.
3. Change the fields:
   - `"slug"`: your slug.
   - `"title"`: the page heading.
   - `"meta"`: the short line under the title, for example `"Oct 2026"`.
   - `"summary"`: one sentence. It's used as the intro and as the Google description.
   - `"problem"`: a list of paragraphs.
   - `"built"` and `"results"`: lists of bullets.
   - `"lesson"`: optional. Delete the line if you don't want a Lesson section.
   - `"stack"`: the list of tags.
   - `"links"`: pairs of (link text, address).
4. Give the page its top image. In the same file, find `def visual(slug):`. Inside `imgs = {`, add a line like this:

   ```python
   "my-new-project": ("/assets/projects/my-new-project-figure", "-thumb", 640, 1200, 600, "Alt text for the figure"),
   ```

   The values are: the image path without `.webp`, the thumbnail suffix, the thumbnail width, the full image width, the full image height, and the alt text. Every project needs either a line here or a diagram. Without one, the script stops with a `KeyError`.
5. In a terminal at the repo root, run:

   ```bash
   PYTHONPATH=scripts/dev python3 scripts/dev/gen_projects.py .
   ```

   It rewrites every file in `projects/`. Only the new page should show up as changed. In VS Code, check the **Source Control** panel. In a terminal, run `git status`.

**Option B: copy a page by hand.** No Python needed. This works on github.com too.

1. Open `projects/ml-model-monitoring.html` and copy everything in it.
2. Create `projects/my-new-project.html` and paste.
3. Change these, top to bottom:
   - `<title>`,
   - `name="description"`, `og:description`, and `og:title`,
   - `rel="canonical"` and `og:url`, which become `https://kadaru242003.github.io/projects/my-new-project.html`,
   - the `<h1>`, the `detail-meta` line, and the `lede` paragraph,
   - the links,
   - the top image: `src`, `srcset`, `width`, `height`, and `alt`,
   - the text in Problem, What I built, Results, Lesson, and Stack.
4. **Important:** a page made by hand is overwritten the next time anyone runs the generator. If you use Option B, also add the project to `scripts/dev/gen_projects.py` later, or never run the generator.

### Step 4: Add the page to the sitemap

Open `sitemap.xml` and add one line next to the other project lines:

```xml
  <url><loc>https://kadaru242003.github.io/projects/my-new-project.html</loc></url>
```

### Step 5: Commit and check

Commit everything, which is the image files, `index.html`, `projects/my-new-project.html`, `sitemap.xml`, and the generator if you used it. Then open a pull request and wait for the checks in [section 5](#5-the-ci-checks-and-how-to-fix-failures) to pass.

### Editing an existing project page

If you change text in a project, you may need to change it in two places:

1. **The detail page.** Edit the project's block in `scripts/dev/gen_projects.py`, then run the generator command from Step 3. If you can't run Python, edit `projects/<slug>.html` directly, but then make the same edit in the generator too, so it isn't lost later.
2. **The home page card.** The card text lives separately in `index.html`. Edit it there if it says the same thing.

---

## 3. Add and convert images

### Rules

- **Format:** the site serves **WebP**. Keep the original PNG or JPG in the repo as the source.
- **Not published:** the deploy step does not publish `.png` files from `assets/`. A PNG that is only referenced from a page shows as broken on the live site.
- **Size:** match the image to how it is shown.

| Use | Folder | File names | Width |
|---|---|---|---|
| Project figure, detail page | `assets/projects/` | `name.webp` | Original size, up to about 1600 px |
| Project figure, home page card | `assets/projects/` | `name-thumb.webp` | 640 px |
| Screenshot (lightbox) | `assets/` | `name.webp` and `name-thumb.webp` | 1600 px and 800 px |
| Education photo | `assets/` | `name.webp` | 800 px |

### Convert to WebP

Pick one of these ways.

- **No install:** go to https://squoosh.app, drop in the image, and pick **WebP** on the right. Set quality to about 80. Under **Resize**, set the width (for example 640 for a thumbnail). Download the result and upload it to the folder above.
- **Command line, with Google's `cwebp`:**

  ```bash
  cwebp -q 82 figure.png -o figure.webp
  cwebp -q 82 -resize 640 0 figure.png -o figure-thumb.webp
  ```

  Install it with `brew install webp` (Mac), `sudo apt install webp` (Linux), or from https://developers.google.com/speed/webp/download (Windows).

### Width and height

Every `<img>` needs `width` and `height` attributes set to the **real pixel size of that file**. They stop the page from jumping while it loads. The checks won't catch a missing or wrong size, so set them yourself.

To find the size:

- **Mac:** open the image in Preview and choose Tools > Show Inspector.
- **Windows:** right-click the file, choose Properties, then open the Details tab.
- **VS Code:** open the image. The size shows in the status bar.

Example for a 640 x 270 thumbnail:

```html
<img src="/assets/projects/name-thumb.webp" width="640" height="270" loading="lazy" alt="...">
```

### Alt text

- Describe what the image shows and why it matters, in one plain sentence. For example: `Monthly ROC AUC from October 2016 to August 2017`.
- Don't start with "Image of".
- Don't put numbers or claims in alt text that aren't also on the page.

Use `loading="lazy"` on images lower down the page. Leave it off the top image of a detail page.

---

## 4. Replace the resume

The file must be named exactly **`resume.pdf`** and sit at the repo root. All Resume links point to `/resume.pdf`.

1. **On github.com:** open the repo, click **Add file**, then **Upload files**, and drop in the new `resume.pdf`. Uploading a file with the same name replaces the old one. Commit.
2. **In VS Code:** copy the new file over `resume.pdf`, then commit and push.

The deploy publishes it automatically. Browsers may cache the old copy for a few minutes. To check, open https://kadaru242003.github.io/resume.pdf in a private window.

---

## 5. The CI checks and how to fix failures

The workflow is `.github/workflows/site.yml`. It runs:

- on every pull request,
- on every push to `main`,
- every Monday.

To see results, open the pull request and look at **Checks** near the bottom, or open the **Actions** tab. Click a red X, then the failing step, to read the error.

| Check | What it does |
|---|---|
| **HTML validity: html-validate** | Checks HTML rules and accessibility, such as images without `alt` and wrong nesting. |
| **HTML validity: W3C Nu HTML Checker** | The official HTML validator. |
| **HTML validity: No em dashes** | Fails if any text file contains an em dash. |
| **HTML validity: Local assets exist** | Fails if `og-image.png`, `favicon.svg`, or `resume.pdf` is missing. |
| **Broken links** | Uses lychee to open every link in `index.html`, `404.html`, and `projects/*.html`. LinkedIn is skipped because it blocks bots. Settings are in `lychee.toml`. |
| **Deploy to GitHub Pages** | Runs only on `main` after both checks pass. It copies the site into `_site/` and publishes it. |

Both validators check only the root pages (`index.html`, `404.html`) and `projects/*.html`. If you add a page anywhere else, also add its path to the html-validate, Nu checker, and lychee commands in `.github/workflows/site.yml`.

### Broken link

The log lists each bad link with its file and line, for example `[404] https://github.com/... (at 210:42)`. That means line 210, column 42.

- **Typo in a URL or path:** fix it in the file and line shown. Paths on this site start with `/` and are relative to the repo root, for example `/assets/projects/name.webp`.
- **The file isn't in the repo yet:** add it, or check the spelling and capitals. `Name.webp` and `name.webp` are different files.
- **An outside site was briefly down (for example a timeout):** re-run the failed job with **Re-run failed jobs** on the run page. If it fails again, the link is really broken.
- **A site that always blocks bots:** add a line to `exclude` in `lychee.toml`, the same way LinkedIn is excluded. Only do this if the link works in your browser.

### HTML validator error

Errors look like `index.html 212:15 error <message> (rule-name)`, which means line 212, column 15. Common causes:

| Message mentions | Fix |
|---|---|
| `alt` / `wcag/h37` | Add `alt="..."` to the `<img>`. |
| an unclosed, stray, or mismatched element | A tag was deleted or pasted twice. Compare with the block you copied from and keep every opening tag paired with its closing tag, the same way. |
| `&` / character reference | Write `&amp;` instead of `&`. |
| duplicate `id` | Two elements share an `id`. Make one of them unique. |

To run html-validate yourself (needs Node.js):

```bash
npx html-validate@9.7.1 *.html projects/*.html
```

### Dash check

- **What it means:** the text contains an em dash (the long dash). The site uses commas, colons, or "to" instead, for example `Jun 2026 to Aug 2026`.
- **Where to look:** the log shows the file and line.
- **Common cause:** text pasted from Word, Google Docs, or a resume often carries these dashes in. Replace each one, using a comma, a colon, a period, or "to".
- **En dashes:** the shorter en dash is not checked by CI, but the site doesn't use those either. Replace them the same way.

To find dashes in VS Code, open Find in Files, turn on regex (the `.*` button), and search for:

```
\u2014|\u2013
```

---

## 6. Preview the site locally

Preview before pushing anything bigger than a text fix.

**Option A: Python (built into Mac and Linux).** In a terminal at the repo root, run:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser. Press Ctrl+C in the terminal to stop.

**Option B: VS Code.** Install the **Live Server** extension. Open the repo folder itself, not a subfolder, then right-click `index.html` and choose **Open with Live Server**.

Opening `index.html` by double-clicking won't work properly. The site uses paths that start with `/`, which need a local server.

What to check in the preview:

- the page in both light and dark mode (the moon and sun button in the header),
- a narrow window (or the browser's phone view: F12, then the device icon),
- any new images and links,
- every page you changed, including `projects/<slug>.html`.

Then push, open a pull request, and wait for the checks. When they're green, merge. The site updates about a minute after the deploy job finishes.
