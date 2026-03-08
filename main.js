/* ============================================
   YUMO — Portfolio Scripts
   Minimal, no dependencies
   ============================================ */

(function () {
  'use strict';

  // --- Year ---
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // --- Mobile Menu ---
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
      menuBtn.classList.toggle('active');
      mobileMenu.classList.toggle('active');
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menuBtn.classList.remove('active');
        mobileMenu.classList.remove('active');
      });
    });
  }

  // --- Smooth scroll for nav links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // --- Page load animation ---
  window.addEventListener('load', () => {
    document.body.classList.add('loaded');
  });

  // --- Typewriter effect for hero gradient text ---
  const typewriterEl = document.querySelector('.typewriter');
  if (typewriterEl) {
    const text = typewriterEl.getAttribute('data-text');
    typewriterEl.textContent = '';
    typewriterEl.style.borderRight = '2px solid var(--accent)';

    let i = 0;
    function typeChar() {
      if (i < text.length) {
        typewriterEl.textContent += text.charAt(i);
        i++;
        setTimeout(typeChar, 60 + Math.random() * 40);
      } else {
        // Blink cursor after typing completes
        typewriterEl.classList.add('typing-done');
      }
    }

    // Start typing after page load animation
    setTimeout(typeChar, 800);
  }

  // --- Staggered scroll-reveal animations ---
  const staggerGroups = [
    { parent: '.about-stats', children: '.stat-card' },
    { parent: '.projects-grid', children: '.project-card' },
    { parent: '.skills-grid', children: '.skill-group' },
    { parent: '.timeline-entries', children: '.timeline-entry' },
  ];

  staggerGroups.forEach(({ parent, children }) => {
    const parentEl = document.querySelector(parent);
    if (!parentEl) return;
    const items = parentEl.querySelectorAll(children);
    items.forEach((el, idx) => {
      el.classList.add('fade-in');
      el.style.transitionDelay = (idx * 0.1) + 's';
    });
  });

  // Single elements (no stagger)
  const singleAnimElements = document.querySelectorAll(
    '.section-label, .section-title, .about-content, ' +
    '.project-featured, .contact-block, .timeline-header'
  );
  singleAnimElements.forEach(el => el.classList.add('fade-in'));

  // Observe all fade-in elements
  const allFadeIns = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );
  allFadeIns.forEach(el => observer.observe(el));

  // --- Nav scroll effect ---
  const nav = document.getElementById('nav');

  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > 100) {
      nav.style.borderBottomColor = 'var(--border)';
    } else {
      nav.style.borderBottomColor = 'transparent';
    }
  }, { passive: true });

  // --- Active nav link highlighting ---
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 120;
      if (window.pageYOffset >= top) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.style.color = '';
      if (link.getAttribute('href') === '#' + current) {
        link.style.color = 'var(--text)';
      }
    });
  }, { passive: true });

  // --- Hero particle canvas ---
  const canvas = document.getElementById('hero-particles');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 50;

    function resize() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
    }

    function createParticles() {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          r: Math.random() * 1.5 + 0.5,
          dx: (Math.random() - 0.5) * 0.3,
          dy: (Math.random() - 0.5) * 0.3,
          opacity: Math.random() * 0.3 + 0.1,
        });
      }
    }

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(59, 130, 246, ${p.opacity})`;
        ctx.fill();

        p.x += p.dx;
        p.y += p.dy;

        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
      });
      requestAnimationFrame(drawParticles);
    }

    resize();
    createParticles();
    drawParticles();
    window.addEventListener('resize', () => { resize(); createParticles(); });
  }

})();
