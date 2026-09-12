document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();

  const presets = {
    normal: { oxygen: '98', temperature: '36.8', breathing_difficulty: 'none', pain_level: '1', confusion: 'no', medication_adherence: 'yes' },
    borderline: { oxygen: '92', temperature: '38.2', breathing_difficulty: 'mild', pain_level: '3', confusion: 'no', medication_adherence: 'yes' },
    urgent: { oxygen: '88', temperature: '39.6', breathing_difficulty: 'severe', pain_level: '7', confusion: 'no', medication_adherence: 'yes' }
  };

  document.querySelectorAll('[data-preset]').forEach((button) => {
    button.addEventListener('click', () => {
      const preset = presets[button.dataset.preset];
      if (!preset) return;
      Object.entries(preset).forEach(([field, value]) => {
        const input = document.querySelector(`[name="${field}"]`);
        if (input) input.value = value;
      });
      document.querySelectorAll('[data-preset]').forEach((item) => item.classList.remove('is-selected'));
      button.classList.add('is-selected');
    });
  });

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
