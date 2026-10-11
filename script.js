// Light / dark theme toggle. Without JavaScript the site follows the system setting.
(function () {
  var root = document.documentElement;
  var button = document.querySelector(".theme-toggle");
  if (!button) return;

  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function current() {
    var forced = root.getAttribute("data-theme");
    if (forced === "light" || forced === "dark") return forced;
    return media.matches ? "dark" : "light";
  }

  function render() {
    var theme = current();
    var next = theme === "dark" ? "light" : "dark";
    button.setAttribute("data-current", theme);
    button.setAttribute("aria-label", "Switch to " + next + " theme");
  }

  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
    render();
  });

  if (media.addEventListener) media.addEventListener("change", render);

  button.hidden = false;
  render();
})();

// Click-to-enlarge screenshots. Without JavaScript the links open the image directly.
(function () {
  var links = document.querySelectorAll("a[data-lightbox]");
  if (!links.length || typeof HTMLDialogElement !== "function") return;

  var dialog = document.createElement("dialog");
  dialog.className = "lightbox";
  dialog.setAttribute("aria-label", "Enlarged screenshot");
  var close = document.createElement("button");
  close.type = "button";
  close.className = "lightbox-close";
  close.setAttribute("aria-label", "Close");
  close.textContent = "×";
  var img = document.createElement("img");
  var caption = document.createElement("p");
  dialog.appendChild(close);
  dialog.appendChild(img);
  dialog.appendChild(caption);
  document.body.appendChild(dialog);

  var opener = null;

  close.addEventListener("click", function () {
    dialog.close();
  });

  // Clicking the dark backdrop (outside the image) closes the dialog.
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });

  dialog.addEventListener("close", function () {
    img.removeAttribute("src");
    if (opener) opener.focus();
  });

  Array.prototype.forEach.call(links, function (link) {
    link.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      e.preventDefault();
      var thumb = link.querySelector("img");
      img.src = link.href;
      img.alt = thumb ? thumb.alt : "";
      caption.textContent = link.getAttribute("data-caption") || "";
      opener = link;
      dialog.showModal();
      close.focus();
    });
  });
})();

// Fade sections in as they scroll into view. CSS only hides them when the
// html element has the "js" class and the user allows motion, so the page
// is fully visible without JavaScript.
(function () {
  var items = document.querySelectorAll(".reveal");
  if (!items.length) return;
  if (!("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(items, function (el) { el.classList.add("is-visible"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
  Array.prototype.forEach.call(items, function (el) { io.observe(el); });
})();

// Highlight the nav link for the section currently in view (home page).
(function () {
  if (!("IntersectionObserver" in window)) return;
  var links = {};
  Array.prototype.forEach.call(document.querySelectorAll('.nav-links a[href^="#"]'), function (a) {
    links[a.getAttribute("href").slice(1)] = a;
  });
  var sections = Object.keys(links).map(function (id) { return document.getElementById(id); }).filter(Boolean);
  if (!sections.length) return;

  function setCurrent(id) {
    Object.keys(links).forEach(function (key) {
      if (key === id) links[key].setAttribute("aria-current", "true");
      else links[key].removeAttribute("aria-current");
    });
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) setCurrent(entry.target.id);
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  sections.forEach(function (s) { io.observe(s); });

  // Above the first section, nothing is current.
  window.addEventListener("scroll", function () {
    if (window.scrollY < sections[0].offsetTop - window.innerHeight * 0.4) setCurrent(null);
  }, { passive: true });
})();
