document.addEventListener('DOMContentLoaded', () => {
  // Animate stats counters
  const counters = document.querySelectorAll('.stat-number');

  function formatValue(val, target) {
    // If target >= 1000, show as K+ rounded
    if (target >= 1000) {
      const k = Math.round(val / 1000);
      return `${k}K+`;
    }
    return Math.round(val).toString();
  }

  counters.forEach((el, idx) => {
    const target = parseInt(el.dataset.target || el.textContent.replace(/[^0-9]/g, ''), 10) || 0;
    el.textContent = '0';
    // We'll animate when element becomes visible
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // duration and start time
          const duration = 1400 + idx * 200; // stagger
          const start = performance.now();
          function step(now) {
            const progress = Math.min((now - start) / duration, 1);
            const value = Math.floor(progress * target);
            el.textContent = formatValue(value, target);
            if (progress < 1) {
              requestAnimationFrame(step);
            } else {
              // final value
              el.textContent = formatValue(target, target);
              // pop animation
              el.classList.add('pop');
              setTimeout(() => el.classList.remove('pop'), 600);
            }
          }
          requestAnimationFrame(step);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.2 });
    io.observe(el);
  });

  // Animate entrance for .animate-up elements with small stagger
  const animEls = Array.from(document.querySelectorAll('.animate-up'));
  const animObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        el.classList.add('visible');
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.12 });

  animEls.forEach((el, i) => {
    // small stagger when visible: delay via setTimeout after visible class
    animObserver.observe(el);
  });

});
