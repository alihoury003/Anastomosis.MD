const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('payment-prep/payment-link.html', 'utf8');
const inline = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];

function page(search, sdk = {}) {
  const status = { textContent: '' };
  const location = { search };
  let calls = [];
  const Paddle = sdk.missing ? undefined : { Initialize(options) {
    calls.push(options);
    if (sdk.throws) throw Error('SDK unavailable');
  }};
  const ctx = vm.createContext({ window: { location, Paddle }, document: { getElementById: () => status }, URLSearchParams });
  vm.runInContext(inline, ctx);
  return { ctx, calls, status, location };
}
test('initializes Paddle for transaction links without changing URL', () => {
  const p = page('?_ptxn=txn_abc&other=keep'); p.ctx.startPaymentLink();
  assert.equal(p.calls.length, 1);
  assert.match(p.calls[0].token, /^live_/);
  assert.equal(p.calls[0].checkout.settings.displayMode, 'overlay');
  assert.equal(p.location.search, '?_ptxn=txn_abc&other=keep');
  assert.match(p.status.textContent, /Opening/);
  p.calls[0].eventCallback({name:'checkout.loaded'}); assert.match(p.status.textContent, /window is open/);
  p.calls[0].eventCallback({name:'checkout.closed'}); assert.match(p.status.textContent, /reopen your original link/);
  p.calls[0].eventCallback({name:'checkout.completed'}); assert.doesNotMatch(p.status.textContent, /access.*activat|payment confirmed/i);
});
test('no transaction link does not initialize Paddle', () => {
  const p = page(''); p.ctx.startPaymentLink();
  assert.equal(p.calls.length, 0); assert.match(p.status.textContent, /No payment link/);
});
test('missing SDK and SDK errors show safe help', () => {
  for (const sdk of [{missing:true}, {throws:true}]) {
    const p = page('?_ptxn=txn_abc', sdk); p.ctx.startPaymentLink();
    assert.match(p.status.textContent, /could not be loaded/);
  }
});
test('script load failure does not disclose a transaction value', () => {
  const p = page('?_ptxn=txn_secret'); p.ctx.paymentScriptFailed();
  assert.match(p.status.textContent, /could not be loaded/);
  assert.doesNotMatch(p.status.textContent, /txn_secret/);
});
test('loads Paddle.js and has no automatic redirect or Checkout.open', () => {
  assert.match(html, /https:\/\/cdn\.paddle\.com\/paddle\/v2\/paddle\.js/);
  assert.doesNotMatch(inline, /location\.(?:href|assign|replace)\s*(?:=|\()/);
  assert.doesNotMatch(inline, /Paddle\.Checkout\.open\s*\(/);
});
