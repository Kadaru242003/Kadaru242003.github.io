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
