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
