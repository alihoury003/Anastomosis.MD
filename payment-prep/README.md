# Payment link preparation — not deployed

This is a candidate public Paddle default-payment-link page. It is **not production-ready and has not been tested with Paddle or deployed**. Do not set it as the live default link yet. It uses the same public live Paddle.js client-side token as the main dashboard; it does not contain a server API key or webhook secret.

Paddle documents that `_ptxn` is opened automatically after Paddle.js initialization: https://developer.paddle.com/build/transactions/default-payment-link/. This page does not require login, change the query string, or call `Checkout.open` with competing items. It does not provision access, validate payment, implement subscription changes or solve access control.

Before deployment or live default-link changes: review the page; test a sandbox-configured copy using a sandbox token and sandbox Paddle.js environment (never switch production in place); verify payment transaction and payment-method-update links, failures, expired links, close/reopen, both relevant hosts and mobile; check the intended path serves on the approved domain. Ensure signed webhook processing, durable user mapping, correct subscription lifecycle and protected question access. Fix the advertised optional-renewal mismatch. Consult Paddle where needed. Obtain explicit approval for production settings and a cautious live test; never take accidental real payments. The current live catalog, prices, default link and entitlements are unchanged.

Local mocks: `node --test tests/payment-link.test.cjs`. These don't load Paddle.js or prove real checkout behavior.
