(function () {
  function initGallery(root) {
    if (!root || typeof Swiper === 'undefined') return;

    var mainEl = root.querySelector('.swiper-main');
    var thumbsEl = root.querySelector('.swiper-thumbs');
    if (!mainEl || !thumbsEl) return;

    var thumbs = new Swiper(thumbsEl, {
      spaceBetween: 10,
      slidesPerView: 'auto',
      freeMode: true,
      watchSlidesProgress: true,
      slideToClickedSlide: true,
    });

    new Swiper(mainEl, {
      spaceBetween: 10,
      navigation: {
        nextEl: root.querySelector('.swiper-button-next'),
        prevEl: root.querySelector('.swiper-button-prev'),
      },
      thumbs: {
        swiper: thumbs,
      },
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.hl-gallery').forEach(initGallery);
  });
})();
