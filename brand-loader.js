/* Runs immediately after the loader markup, before the rest of the page is parsed. */
(() => {
  const root = document.querySelector('.brand-loader');
  if (!root) return;
  const mode = root.dataset.mode || 'entry';
  const status = root.querySelector('.brand-loader-status');
  const started = performance.now();
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  const timers = [];
  let closed = false;
  let sequenceDone = false;
  let pageReady = document.readyState === 'complete';
  const later = (ms, fn) => timers.push(window.setTimeout(fn, ms));

  function finish() {
    if (closed) return;
    closed = true;
    root.classList.add('complete');
    window.setTimeout(() => root.classList.add('is-done'), 420);
    window.setTimeout(() => { root.style.display = 'none'; }, 1050);
  }
  function setStatus(text) {
    if (status && !closed) status.textContent = text;
  }

  root.classList.add('is-running');

  if (mode === 'entry') {
    const maybeFinish = () => { if (sequenceDone && pageReady) finish(); };
    window.addEventListener('load', () => { pageReady = true; maybeFinish(); }, { once: true });
    later(900, () => setStatus('Joining the two sides'));
    later(2050, () => setStatus('The connection is sealed'));
    later(2850, () => setStatus('Perfusion restored'));
    later(reduced ? 250 : 4100, () => { sequenceDone = true; root.classList.add('complete'); maybeFinish(); });
    root.addEventListener('click', finish, { once: true });
    // Never trap someone if the browser fails to finish loading a resource.
    later(12000, finish);
  } else {
    later(900, () => setStatus('Linking your study history'));
    later(1950, () => setStatus('Preparing your next step'));
    // Called by dashboard.html only after the user's workspace data is ready.
    window.brandLoaderDismiss = () => {
      const minimum = reduced ? 250 : 1850;
      later(Math.max(0, minimum - (performance.now() - started)), finish);
    };
    // Appwrite/network failure must never leave a permanent overlay.
    later(12000, finish);
  }

  if (reduced) root.classList.add('complete');
})();
