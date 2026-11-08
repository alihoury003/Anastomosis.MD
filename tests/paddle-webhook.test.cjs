'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { verifySignature, handleWebhook, MAX_BODY_BYTES } = require('../payment-backend/paddle-webhook.cjs');
const secret = 'example-test-secret-not-a-real-credential';
const now = 1800000000000, ts = String(now / 1000);
const event = { event_id:'evt_0123456789abcdefghijklmnop', event_type:'transaction.completed', data:{ id:'txn_sample', text:'α' } };
const body = Buffer.from(JSON.stringify(event));
function sign(payload = body, timestamp = ts, key = secret) {
  return crypto.createHmac('sha256', key).update(timestamp + ':').update(payload).digest('hex');
}
function header(payload = body, timestamp = ts, key = secret) { return `ts=${timestamp};h1=${sign(payload, timestamp, key)}`; }
function request(overrides = {}) { return { method:'POST', rawBody:body, signature:header(), secret, now, archive:async ()=>'stored', ...overrides }; }

test('valid signature over exact UTF-8 raw bytes', () => assert.equal(verifySignature(body, header(), secret, now), true));
test('body mutation, wrong key, malformed signature and stale/future timestamps fail', () => {
  assert.equal(verifySignature(Buffer.from(body.toString()+' '), header(), secret, now), false);
  assert.equal(verifySignature(body, header(), 'wrong', now), false);
  assert.equal(verifySignature(body, `ts=${ts};h1=xyz`, secret, now), false);
  assert.equal(verifySignature(body, header(body, String(Number(ts)-10)), secret, now), false);
  assert.equal(verifySignature(body, header(body, String(Number(ts)+10)), secret, now), false);
  assert.equal(verifySignature(body, `ts=${ts};ts=${ts};h1=${sign()}`, secret, now), false);
});
test('supports multiple h1 signatures without accepting a bad one', () => {
  assert.equal(verifySignature(body, `ts=${ts};h1=${'0'.repeat(64)};h1=${sign()}`, secret, now), true);
  assert.equal(verifySignature(body, `ts=${ts};h1=${'0'.repeat(64)}`, secret, now), false);
});
test('invalid auth never reaches storage', async () => {
  let calls = 0;
  const result = await handleWebhook(request({signature:'broken', archive:async()=>{calls++;return 'stored';}}));
  assert.equal(result.status,401); assert.equal(calls,0);
});
test('accepted events are handed to durable idempotent archive and duplicates are accepted', async () => {
  for (const value of ['stored','duplicate']) {
    let saved;
    const result = await handleWebhook(request({archive:async record=>{saved=record;return value;}}));
    assert.equal(result.status,200); assert.equal(saved.id,event.event_id); assert.equal(saved.type,event.event_type); assert.deepEqual(saved.rawBody,body);
  }
});
test('archive failure or unexpected return triggers retry rather than false success', async () => {
  assert.equal((await handleWebhook(request({archive:async()=>{throw new Error('private detail');}}))).status,503);
  const bad = await handleWebhook(request({archive:async()=>undefined})); assert.equal(bad.status,503); assert.doesNotMatch(bad.body,/private/);
});
test('unsupported methods, missing config, oversized and non-raw bodies fail closed', async () => {
  assert.equal((await handleWebhook(request({method:'GET'}))).status,405);
  assert.equal((await handleWebhook(request({secret:''}))).status,503);
  assert.equal((await handleWebhook(request({rawBody:'string'}))).status,400);
  assert.equal((await handleWebhook(request({rawBody:Buffer.alloc(MAX_BODY_BYTES+1)}))).status,413);
});
test('signed invalid JSON and malformed events fail before storage', async () => {
  for (const b of [Buffer.from('{'),Buffer.from('{}'),Buffer.from(JSON.stringify({...event,event_id:'../bad'})),Buffer.from(JSON.stringify({...event,data:null}))]) {
    let count=0; const result=await handleWebhook(request({rawBody:b,signature:header(b),archive:async()=>{count++;return 'stored';}}));
    assert.equal(result.status,400); assert.equal(count,0);
  }
});
