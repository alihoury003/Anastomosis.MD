'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {createBinding, verifyBinding} = require('../payment-backend/checkout-binding.cjs');
const key = Buffer.alloc(32, 7), args = {userId:'test_user', priceId:'pri_0123456789abcdefghijklmnop', environment:'sandbox'};
test('authenticated session identity and price survive signing', () => {
  const token = createBinding(args,key); const result = verifyBinding(token,key,'sandbox');
  assert.equal(result.userId,args.userId); assert.equal(result.priceId,args.priceId);
  assert.equal(result.environment,'sandbox'); assert.match(result.nonce,/^[A-Za-z0-9_-]{32}$/);
});
test('nonce is fresh for independent checkouts', () => {
  const a = verifyBinding(createBinding(args,key),key,'sandbox');
  const b = verifyBinding(createBinding(args,key),key,'sandbox');
  assert.notEqual(a.nonce,b.nonce);
});
test('rejects forged payloads, wrong keys and environment', () => {
  const token = createBinding(args,key), [payload, mac] = token.split('.');
  const object = JSON.parse(Buffer.from(payload,'base64url')); object.userId='attacker';
  const changed = Buffer.from(JSON.stringify(object)).toString('base64url')+'.'+mac;
  assert.equal(verifyBinding(changed,key,'sandbox'),null);
  assert.equal(verifyBinding(token,Buffer.alloc(32,8),'sandbox'),null);
  assert.equal(verifyBinding(token,key,'live'),null);
});
test('fails closed on malformed input, weak or missing keys', () => {
  for (const bad of [null, '', 'a.b.c', 'a.!', 'a.'.concat('A'.repeat(43)), 'x'.repeat(1025)]) assert.equal(verifyBinding(bad,key,'sandbox'),null);
  assert.throws(()=>createBinding(args,Buffer.alloc(31)));
  assert.throws(()=>createBinding({...args,userId:'../../bad'},key));
  assert.throws(()=>createBinding({...args,priceId:'not-a-price'},key));
  assert.throws(()=>createBinding({...args,environment:'production'},key));
});
