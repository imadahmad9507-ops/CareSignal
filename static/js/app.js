document.addEventListener('DOMContentLoaded', () => {
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
