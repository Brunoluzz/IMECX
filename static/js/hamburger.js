const navbar   = document.querySelector('.navbar');
const toggle   = document.getElementById('menuToggle');
const menu     = document.getElementById('mobileMenu');
const backdrop = document.getElementById('navBackdrop');

// ── Scroll ──────────────────────────────────────────────
const handleScroll = () => {
  navbar.classList.toggle('navbar--scrolled', window.scrollY > 20);
};
window.addEventListener('scroll', handleScroll, { passive: true });
handleScroll();

// ── Menu ─────────────────────────────────────────────────
function openMenu() {
  menu.classList.remove('is-closing');
  menu.classList.add('is-open');
  toggle.classList.add('is-open');
  toggle.setAttribute('aria-expanded', 'true');
  menu.setAttribute('aria-hidden', 'false');
  backdrop.classList.add('is-open');
  document.body.classList.add('menu-lock');
}

function closeMenu() {
  menu.classList.add('is-closing');
  menu.addEventListener('animationend', () => {
    menu.classList.remove('is-open', 'is-closing');
  }, { once: true });
  toggle.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
  menu.setAttribute('aria-hidden', 'true');
  backdrop.classList.remove('is-open');
  document.body.classList.remove('menu-lock');
}

toggle.addEventListener('click', () => {
  menu.classList.contains('is-open') ? closeMenu() : openMenu();
});

menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
backdrop.addEventListener('click', closeMenu);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menu.classList.contains('is-open')) closeMenu();
});