(function () {
  var config = window.SITE_CONFIG;
  if (!config || !config.url) {
    return;
  }

  var base = config.url.replace(/\/$/, "");
  var preservePath = document.currentScript && document.currentScript.hasAttribute("data-preserve-path");

  function normalizeTrailingSlash(pathname) {
    if (!pathname || pathname === "/") {
      return "/";
    }
    return pathname.replace(/\/+$/, "");
  }

  function cleanContentPath(pathname, search, hash) {
    var path = normalizeTrailingSlash(pathname);
    var params = new URLSearchParams(search || "");
    var fragment = hash || "";

    if (path === "/pages/articles") {
      var article = params.get("article");
      if (article) {
        return "/articles/" + encodeURIComponent(article) + "/" + fragment;
      }
    }

    if (path === "/pages/blog") {
      var post = params.get("post");
      if (post) {
        return "/posts/" + encodeURIComponent(post) + "/" + fragment;
      }
    }

    if (path === "/pages/resources") {
      var resource = params.get("resource");
      if (resource) {
        return "/resources/" + encodeURIComponent(resource) + "/" + fragment;
      }
    }

    var articleMatch = path.match(/^\/articles\/([^/]+)$/);
    if (articleMatch) {
      return "/articles/" + encodeURIComponent(decodeURIComponent(articleMatch[1])) + "/" + fragment;
    }

    var postMatch = path.match(/^\/(?:posts|blog)\/([^/]+)$/);
    if (postMatch) {
      return "/posts/" + encodeURIComponent(decodeURIComponent(postMatch[1])) + "/" + fragment;
    }

    var resourceMatch = path.match(/^\/resources\/([^/]+)$/);
    if (resourceMatch) {
      return "/resources/" + encodeURIComponent(decodeURIComponent(resourceMatch[1])) + "/" + fragment;
    }

    return pathname + search + fragment;
  }

  var destination = preservePath
    ? base + cleanContentPath(window.location.pathname, window.location.search, window.location.hash)
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
