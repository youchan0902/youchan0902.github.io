const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('.nav-links');
if (menuButton && menu) {
  menuButton.addEventListener('click', () => {
    const opened = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(opened));
    menu.classList.toggle('is-open', opened);
    menuButton.textContent = opened ? '닫기 −' : '메뉴 +';
  });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menu.classList.remove('is-open');
    menuButton.textContent = '메뉴 +';
  }));
}
const images = [...document.querySelectorAll('[data-lightbox]')];
const dialog = document.querySelector('.lightbox');
if (dialog && images.length) {
  let current = 0;
  let sourceButton;
  const show = index => {
    current = (index + images.length) % images.length;
    const button = images[current];
    const image = dialog.querySelector('.lightbox-body img');
    image.src = button.dataset.lightbox;
    dialog.querySelector('.lightbox-original').href = button.dataset.lightbox;
    image.alt = button.querySelector('img').alt;
    dialog.querySelector('.lightbox-caption').textContent = button.closest('figure').querySelector('figcaption').textContent;
    dialog.querySelector('.lightbox-count').textContent = `${String(current + 1).padStart(2, '0')} / ${String(images.length).padStart(2, '0')}`;
  };
  images.forEach((button, index) => button.addEventListener('click', () => {
    sourceButton = button;
    show(index);
    dialog.showModal();
    document.body.classList.add('modal-open');
    dialog.querySelector('.close-lightbox').focus();
  }));
  dialog.querySelector('.close-lightbox').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('click', e => {
    const r = dialog.getBoundingClientRect();
    if (e.target === dialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) dialog.close();
  });
  dialog.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1); }
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    sourceButton?.focus();
  });
}
