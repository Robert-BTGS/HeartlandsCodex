(function () {
  async function getRandomPage() {
    try {
      const res = await fetch('search/search_index.json');
      if (!res.ok) throw new Error('Failed to load search index');
      const data = await res.json();
      if (!data || !Array.isArray(data.docs)) throw new Error('Invalid search index');

      // Filter out index-like pages and keep only content pages
      const pages = data.docs.filter(d => {
        if (!d || !d.location) return false;
        if (d.location.endsWith('/')) return false;
        const loc = d.location.toLowerCase();
        return !(
          loc.endsWith('index.html') ||
          loc.includes('/indexes/') ||
          loc.includes('/tags/') ||
          loc.includes('/templates/')
        );
      });

      if (!pages.length) return null;
      const pick = pages[Math.floor(Math.random() * pages.length)];
      return pick.location;
    } catch (err) {
      console.error(err);
      return null;
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('random-page-button');
    if (!btn) return;

    btn.addEventListener('click', async function (e) {
      e.preventDefault();
      btn.setAttribute('aria-busy', 'true');
      const loc = await getRandomPage();
      btn.setAttribute('aria-busy', 'false');
      if (loc) {
        window.location.href = loc;
      }
    });
  });
})();
