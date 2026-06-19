(function () {
  var config = window.SITE_CONFIG;
  if (!config || !config.url) {
    return;
  }

  var base = config.url.replace(/\/$/, "");
  var preservePath = document.currentScript && document.currentScript.hasAttribute("data-preserve-path");
  var destination = preservePath
    ? base + window.location.pathname + window.location.search + window.location.hash
    : base;

  var meta = document.createElement("meta");
  meta.httpEquiv = "refresh";
  meta.content = "0; url=" + destination;
  document.head.appendChild(meta);

  if (!preservePath) {
    var canonical = document.createElement("link");
    canonical.rel = "canonical";
    canonical.href = base;
    document.head.appendChild(canonical);
  }

  var link = document.getElementById("redirect-link");
  if (link) {
    link.href = destination;
  }

  window.location.replace(destination);
})();
