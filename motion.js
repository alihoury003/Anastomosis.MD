/* ============================================================
   MEDCHANIC.MD — motion layer
   Dependency-free, GPU-friendly, and accessibility-aware.

   Injected inline into the public pages by
   compliance/apply_site_changes.py, so it never depends on a
   server path (the Appwrite host serves index.html for every
   route, which would break an external <script src>).

   Usage
   -----
     <span data-count="2000" data-format="comma">2,000</span>   counter
     <div data-reveal>                                          fade up
     <div data-reveal="left">                                   fade in from left
     <div data-reveal="right">                                  fade in from right
     <div data-reveal="scale">                                  scale in
     <div data-draw>                                            rule draws in
     data-reveal-delay="120"                                    stagger, in ms
     data-duration="1600"                                       counter duration

   Everything is transform/opacity only, runs once, and is
   disabled outright when the visitor prefers reduced motion.
   ============================================================ */
(function () {
  'use strict';

  var motion = {
    reduced: false,
    booted: false
  };

  /* counters that have been snapped to their final value — their rAF loop
     must stop, otherwise the next frame overwrites the final figure */
  var cancelled = (typeof WeakSet !== 'undefined') ? new WeakSet() : null;

  try {
    motion.reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) { /* older browsers: animate anyway */ }

  /* ---------------------------------------------------------- easing */
  function easeOutExpo(t) {
    return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }

  /* ---------------------------------------------------------- formatting */
  function format(n, mode) {
    n = Math.round(n);
    if (mode === 'comma') return n.toLocaleString('en-US');
    return String(n);
  }

  /* ---------------------------------------------------------- counters */
  function runCounter(el) {
    var raw = el.getAttribute('data-count');
    if (raw === null) return;
    var target = parseFloat(raw);
    if (isNaN(target)) return;
    var mode = el.getAttribute('data-format') || 'plain';
    var dur = parseFloat(el.getAttribute('data-duration') || 1500);
    var delay = parseFloat(el.getAttribute('data-delay') || 0);

    if (motion.reduced) {
      el.textContent = format(target, mode);
      return;
    }

    setTimeout(function () {
      var start = null;
      function step(ts) {
        if (cancelled && cancelled.has(el)) return;
        if (start === null) start = ts;
        var p = dur <= 0 ? 1 : Math.min(1, (ts - start) / dur);
        el.textContent = format(target * easeOutExpo(p), mode);
        if (p < 1) {
          requestAnimationFrame(step);
        } else {
          el.textContent = format(target, mode);
        }
      }
      requestAnimationFrame(step);
    }, delay);
  }

  /* ---------------------------------------------------------- reveals */
  function revealAll() {
    var els = document.querySelectorAll('[data-reveal], [data-draw]');
    for (var i = 0; i < els.length; i++) {
      els[i].classList.add('is-in');
    }
  }

  /* Give each child of [data-stagger] its own reveal delay, so a group
     (hero copy, stat row, plan cards) cascades instead of popping at once. */
  function applyStaggers() {
    var groups = document.querySelectorAll('[data-stagger]');
    for (var g = 0; g < groups.length; g++) {
      var group = groups[g];
      var step = parseFloat(group.getAttribute('data-stagger')) || 80;
      var kids = group.children;
      for (var i = 0; i < kids.length; i++) {
        var k = kids[i];
        if (!k.hasAttribute('data-reveal') && !k.hasAttribute('data-draw')) {
          k.setAttribute('data-reveal', '');
        }
        if (!k.hasAttribute('data-reveal-delay')) {
          k.setAttribute('data-reveal-delay', String(i * step));
        }
      }
    }
  }

  function init() {
    applyStaggers();

    if (!('IntersectionObserver' in window)) {
      revealAll();
      runCountersIn(document);
      motion.booted = true;
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);
        var delay = parseFloat(el.getAttribute('data-reveal-delay'));
        if (!isNaN(delay) && delay > 0) {
          el.style.transitionDelay = delay + 'ms';
        }
        el.classList.add('is-in');
        if (el.hasAttribute('data-count')) runCounter(el);
        var inner = el.querySelectorAll('[data-count]');
        for (var i = 0; i < inner.length; i++) runCounter(inner[i]);
      });
    }, { threshold: 0.25, rootMargin: '0px 0px -8% 0px' });

    var targets = document.querySelectorAll('[data-reveal], [data-draw], [data-count]');
    for (var i = 0; i < targets.length; i++) io.observe(targets[i]);

    motion.booted = true;

    /* Safety net. If the motion layer ever failed to initialise, drop the
       .js class so the reveal CSS stops hiding content entirely — the page
       becomes fully visible instead of half-blank. This must NOT run on the
       happy path, or below-the-fold content would appear before you scroll
       to it and the scroll reveals would never be seen. */
    setTimeout(function () {
      if (!motion.booted) document.documentElement.classList.remove('js');
    }, 1800);
  }

  function runCountersIn(root) {
    var els = root.querySelectorAll('[data-count]');
    for (var i = 0; i < els.length; i++) runCounter(els[i]);
  }

  /* ---------------------------------------------------------- boot */
  function boot() {
    try {
      init();
    } catch (e) {
      revealAll();
      document.documentElement.classList.remove('js');
      if (window.console) console.warn('motion: fallback', e);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  /* Snap every counter to its final value and reveal everything.
     Used by the screenshot pipeline so marketing captures never show a
     half-counted number, and useful for anyone who wants to skip the show. */
  function finishAll() {
    var els = document.querySelectorAll('[data-count]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var target = parseFloat(el.getAttribute('data-count'));
      if (isNaN(target)) continue;
      if (cancelled) cancelled.add(el);
      el.textContent = format(target, el.getAttribute('data-format') || 'plain');
    }
    revealAll();
  }

  /* Expose for debugging / tests / tooling */
  window.MedchanicMotion = {
    revealAll: revealAll,
    runCounter: runCounter,
    finishAll: finishAll
  };
})();
