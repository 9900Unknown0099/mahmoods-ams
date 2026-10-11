/* Mahmoods AMS site — vanilla JS, no dependencies */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ---- Split headlines into animated words ---- */
  $$('.split').forEach(el => {
    const walk = (node, state) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = 'w';
            const s = document.createElement('span'); s.textContent = part; s.style.setProperty('--i', state.i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n, state);
      });
    };
    walk(el, { i: 0 });
  });

  /* ---- Reveal on scroll ---- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .14, rootMargin: '0px 0px -6% 0px' });
  $$('.rv, .rv-scale, .split, .engine-card').forEach(el => io.observe(el));

  /* ---- Nav: switch between dark/light glass based on section underneath ---- */
  const nav = $('.nav');
  const sections = $$('[data-nav]');
  const updateNav = () => {
    if (!nav || !sections.length) return;
    const y = nav.offsetHeight / 2;
    let theme = 'dark';
    sections.forEach(s => { const r = s.getBoundingClientRect(); if (r.top <= y && r.bottom >= y) theme = s.dataset.nav; });
    nav.classList.toggle('light', theme === 'light');
  };

  /* ---- Mobile menu ---- */
  const btn = $('.menu-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open);
      const dr = $('.drawer'); if (dr) dr.setAttribute('aria-hidden', String(!open));
      document.documentElement.style.overflow = open ? 'hidden' : '';
    });
    $$('.drawer a').forEach(a => a.addEventListener('click', () => { document.body.classList.remove('menu-open'); document.documentElement.style.overflow = ''; }));
  }

  /* ---- Count-up numbers ---- */
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target; countIO.unobserve(el);
      const to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
      const suffix = el.dataset.suffix || '';
      if (reduce) { el.textContent = to.toFixed(dec) + suffix; return; }
      const t0 = performance.now(), dur = 1700;
      const tick = (t) => {
        const p = clamp((t - t0) / dur, 0, 1), eased = 1 - Math.pow(1 - p, 4);
        el.textContent = (to * eased).toFixed(dec) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: .6 });
  $$('[data-count]').forEach(el => countIO.observe(el));

  /* ---- Pointer spotlight on cards ---- */
  $$('.card').forEach(card => {
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---- Hero parallax + mouse tilt ---- */
  const stage = $('.hero-stage');
  let mx = 0, my = 0;
  if (stage && !reduce) {
    const main = $('.p-main', stage), left = $('.p-left', stage), right = $('.p-right', stage);
    stage.addEventListener('pointermove', e => {
      const r = stage.getBoundingClientRect();
      mx = ((e.clientX - r.left) / r.width - .5) * 2; my = ((e.clientY - r.top) / r.height - .5) * 2;
    });
    stage.addEventListener('pointerleave', () => { mx = 0; my = 0; });
    const loop = () => {
      const sy = clamp(scrollY, 0, 1200);
      main.style.transform = `translateY(${-sy * .12}px) rotateY(${mx * 6}deg) rotateX(${-my * 4}deg)`;
      left.style.transform = `translateX(calc(var(--pw) * -1.02)) translateY(${60 - sy * .22}px) rotateY(${18 + mx * 5}deg) rotateZ(-2deg)`;
      right.style.transform = `translateX(calc(var(--pw) * 1.02)) translateY(${60 - sy * .22}px) rotateY(${-18 + mx * 5}deg) rotateZ(2deg)`;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---- Sticky showcase (scroll-driven steps) ---- */
  const sc = $('[data-showcase]');
  let lastIdx = -1;
  const updateShowcase = () => {
    if (!sc || innerWidth <= 860) return;
    const steps = $$('.step', sc), imgs = $$('.stage .screen img', sc), bars = $$('.progress i', sc);
    const r = sc.getBoundingClientRect();
    const total = sc.offsetHeight - innerHeight;
    const p = clamp(-r.top / total, 0, .9999);
    const idx = Math.floor(p * steps.length);
    if (idx === lastIdx) return; lastIdx = idx;
    [steps, imgs, bars].forEach(list => list.forEach((el, i) => el.classList.toggle('active', i === idx)));
  };

  /* ---- Copy checksum ---- */
  $$('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText($(b.dataset.copy).textContent.trim());
      const t = b.textContent; b.textContent = 'Copied'; setTimeout(() => (b.textContent = t), 1600);
    } catch { /* clipboard blocked: ignore */ }
  }));

  /* ---- Smooth page transitions ---- */
  $$('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:') || a.hasAttribute('download') || a.target === '_blank' || href.startsWith('downloads/')) return;
    a.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || reduce) return;
      e.preventDefault();
      document.body.classList.add('leaving');
      setTimeout(() => (location.href = href), 260);
    });
  });
  addEventListener('pageshow', e => { if (e.persisted) document.body.classList.remove('leaving'); });

  /* ---- Scroll handler ---- */
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => { updateNav(); updateShowcase(); ticking = false; });
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { lastIdx = -1; onScroll(); });
  updateNav(); updateShowcase();
  const first = $('.step', sc || document); if (first && sc && innerWidth > 860) { $$('.step', sc)[0].classList.add('active'); $$('.stage .screen img', sc)[0].classList.add('active'); $$('.progress i', sc)[0].classList.add('active'); }
})();
