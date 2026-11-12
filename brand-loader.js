/* Runs immediately after the loader markup, before the rest of the page is parsed. */
(() => {
  const root = document.querySelector('.brand-loader');
  if (!root) return;
  const mode = root.dataset.mode || 'entry';
  const status = root.querySelector('.brand-loader-status');
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  let closed = false;
  let sequenceDone = false;
  let pageReady = document.readyState === 'complete';
  let dashboardReady = false;

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
  function maybeFinish() {
    if (!sequenceDone) return;
    if (mode === 'entry' ? pageReady : dashboardReady) finish();
  }
  function completeSequence() {
    sequenceDone = true;
    root.classList.add('complete');
    maybeFinish();
  }

  root.classList.add('is-running');

  // Both pages use the same loader copy, animation, and timing.
  window.setTimeout(() => setStatus('Joining the two sides'), 900);
  window.setTimeout(() => setStatus('The connection is sealed'), 2050);
  window.setTimeout(() => setStatus('Perfusion restored'), 2850);
  window.setTimeout(completeSequence, reduced ? 250 : 4100);

  if (mode === 'entry') {
    if (!pageReady) {
      window.addEventListener('load', () => { pageReady = true; maybeFinish(); }, { once: true });
    }
    root.addEventListener('click', finish, { once: true });
  } else {
    // Dashboard calls this only after auth, user/question data, and initial rendering.
    window.brandLoaderDismiss = () => {
      dashboardReady = true;
      maybeFinish();
    };
  }

  // Never trap a visitor if the browser or a network request stalls.
  window.setTimeout(finish, 12000);
  if (reduced) root.classList.add('complete');
})();
