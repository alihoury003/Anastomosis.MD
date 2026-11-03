# Arcade 3 smoke test

The prototype is self-contained and needs no installation to play. To re-run the optional browser smoke test with Node 20+:

```sh
npm install --no-save --no-package-lock puppeteer-core @sparticuz/chromium
python3 -m http.server 8000
# In a second terminal:
node tests/arcade3-smoke.mjs
```

The test defaults to `http://127.0.0.1:8000/arcade3.html?debug`; set `ARCADE_URL` to another test URL with `?debug` if needed. Chromium requires its usual Linux shared libraries. The `?debug` hooks are solely for inspecting this local prototype, not secure rankings or production game state. The test exercises the eight screens and representative game paths; it does not certify clinical content, network multiplayer, production performance, or real QBank integration.
