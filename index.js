document.addEventListener('DOMContentLoaded', () => {
  const counters = document.querySelectorAll('.stat-number[data-target], .kpi-val[data-target]');
  const animatedBlocks = document.querySelectorAll('.animate-up, .fade-in');
  const input = document.querySelector('#hero-search');
  const pills = document.querySelectorAll('.search-pill[data-fill]');
  const progressSpans = document.querySelectorAll('[data-target-width]');

  // ── Hero search form handler ──────────────────────────────────
  window.handleHeroSearch = function(e) {
    e.preventDefault();
    const q = (input ? input.value.trim() : '');
    if (!q) { input && input.focus(); return false; }
    window.location.href = 'User/Nav/search_result.html?q=' + encodeURIComponent(q);
    return false;
  };

  const formatValue = (value, target) => {
    if (target >= 1000) {
      return `${Math.round(value / 1000)} ${Math.round(value / 1000) !== Math.round(target / 1000) ? '' : '+'}`.trim() || `${Math.round(value / 1000)}K+`;
    }
    return Math.round(value).toString();
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  animatedBlocks.forEach((block) => revealObserver.observe(block));

  counters.forEach((counter, index) => {
    const target = Number(counter.dataset.target || 0);
    counter.textContent = '0';

    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const startedAt = performance.now();
        const duration = 1000 + index * 100;

        const tick = (now) => {
          const progress = Math.min((now - startedAt) / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3);
          const value = target * ease;
          counter.textContent = Math.round(value).toString();

          if (progress < 1) {
            requestAnimationFrame(tick);
            return;
          }

          counter.textContent = target.toString();
          counter.classList.add('pop');
          window.setTimeout(() => counter.classList.remove('pop'), 260);
        };

        requestAnimationFrame(tick);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.35 });

    counterObserver.observe(counter);
  });

  // Animate progress bars
  progressSpans.forEach((span) => {
    const targetW = Number(span.dataset.targetWidth || 0);
    span.style.width = '0%';
    span.style.transition = 'width 1.1s cubic-bezier(0.4, 0, 0.2, 1)';

    const barObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        // Small delay so the bar is visible before animating
        setTimeout(() => { span.style.width = targetW + '%'; }, 120);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.5 });

    barObserver.observe(span);
  });

  pills.forEach((pill) => {
    pill.addEventListener('click', () => {
      if (!input) {
        return;
      }

      input.value = pill.dataset.fill || '';
      input.focus();
    });
  });

  // Animated placeholder typewriter for hero search
  if (input) {
    const hints = [
      'ETB Pokémon 151',
      'Display Évolution Céleste',
      'Booster Prismatique',
      'Coffret Dresseur Élite',
      'Display Shiny Treasure ex',
      'Tripack japonais',
    ];

    let hintIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    const type = () => {
      if (document.activeElement === input) {
        setTimeout(type, 400);
        return;
      }
      const current = hints[hintIndex];

      if (!isDeleting) {
        input.placeholder = current.slice(0, charIndex + 1);
        charIndex++;
        if (charIndex === current.length) {
          isDeleting = true;
          setTimeout(type, 2200);
          return;
        }
        setTimeout(type, 80);
      } else {
        input.placeholder = current.slice(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          isDeleting = false;
          hintIndex = (hintIndex + 1) % hints.length;
        }
        setTimeout(type, 40);
      }
    };

    input.placeholder = '';
    setTimeout(type, 1200);
  }
});