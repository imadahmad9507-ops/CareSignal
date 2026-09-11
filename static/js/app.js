document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  document.body.classList.add('page-ready');
  document.querySelectorAll('a:not([target="_blank"])').forEach((link) => {
    link.addEventListener('click', (event) => {
      const target = link.getAttribute('href');
      if (!target || target.startsWith('#') || target.startsWith('http')) return;
      event.preventDefault();
      document.body.classList.add('page-leaving');
      window.setTimeout(() => { window.location.href = target; }, 120);
    });
  });

  document.querySelectorAll('[data-loading-form]').forEach((form) => {
    form.addEventListener('submit', () => {
      const button = form.querySelector('[data-submit-button]');
      if (!button) return;
      button.disabled = true;
      button.classList.add('is-loading');
      button.textContent = 'Saving check-in...';
    });
  });
});
