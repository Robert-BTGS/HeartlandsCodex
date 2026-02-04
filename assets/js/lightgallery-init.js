(function () {
  function initGallery(root) {
    if (!root || typeof lightGallery === 'undefined') return;
    lightGallery(root, {
      selector: 'a',
      plugins: [lgThumbnail, lgZoom],
      thumbnail: true,
      zoom: true,
      download: false,
      speed: 300,
      thumbWidth: 90,
      thumbHeight: 60,
      thumbMargin: 8,
      mobileSettings: {
        controls: true,
        showCloseIcon: true,
        download: false,
      },
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.lg-gallery').forEach(initGallery);
  });
})();
