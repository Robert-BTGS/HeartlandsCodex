(function () {
  function titleize(segment) {
    return segment
      .replace(/_/g, ' ')
      .replace(/-/g, ' ')
      .replace(/\b\w/g, function (c) { return c.toUpperCase(); })
      .trim();
  }

  function prettyLabel(segment) {
    if (segment === 'Heartlands_TheArena') return 'Heartlands: The Arena';
    if (segment === 'Heartlands_TLC') return 'Heartlands: The Lost Colony';
    if (segment === 'Heartlands') return 'Heartlands';
    if (segment === 'SiteDesignReference') return 'Site Design Reference';
    return titleize(segment);
  }

  function buildBreadcrumbs() {
    var path = window.location.pathname;
    if (!path) return null;

    // Strip query/hash and trailing index
    path = path.split('?')[0].split('#')[0];
    path = path.replace(/index\.html?$/i, '');
    if (path.endsWith('/')) path = path.slice(0, -1);

    var parts = path.split('/').filter(Boolean);
    if (!parts.length) return null;

    // Remove site base (e.g., HeartlandsCodex) from breadcrumbs if present
    var basePrefix = '';
    if (parts[0].toLowerCase() === 'heartlandscodex') {
      basePrefix = '/HeartlandsCodex';
      parts = parts.slice(1);
    }

    if (!parts.length) return null;

    var crumbs = [];
    var accum = basePrefix;
    for (var i = 0; i < parts.length; i++) {
      var seg = parts[i];
      accum += '/' + seg;
      var label = prettyLabel(seg);
      var isLast = i === parts.length - 1;
      crumbs.push({ label: label, href: isLast ? null : accum + '/' });
    }

    // Always include Home
    crumbs.unshift({ label: 'Home', href: (basePrefix || '') + '/' });

    var nav = document.createElement('nav');
    nav.className = 'hl-breadcrumbs';
    nav.setAttribute('aria-label', 'Breadcrumb');

    var ol = document.createElement('ol');
    nav.appendChild(ol);

    crumbs.forEach(function (c, idx) {
      var li = document.createElement('li');
      if (c.href) {
        var a = document.createElement('a');
        a.href = c.href;
        a.textContent = c.label;
        li.appendChild(a);
      } else {
        var span = document.createElement('span');
        span.textContent = c.label;
        li.appendChild(span);
      }
      ol.appendChild(li);
    });

    return nav;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var target = document.querySelector('.md-content__inner') || document.querySelector('main') || document.body;
    if (!target) return;
    var existing = document.querySelector('.hl-breadcrumbs');
    if (existing) return;

    var crumbs = buildBreadcrumbs();
    if (!crumbs) return;

    // Insert before first H1 if present
    var h1 = target.querySelector('h1');
    if (h1) {
      target.insertBefore(crumbs, h1);
    } else {
      target.insertBefore(crumbs, target.firstChild);
    }
  });
})();
