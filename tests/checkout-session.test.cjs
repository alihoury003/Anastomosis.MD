'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {checkoutSessionService} = require('../payment-backend/checkout-session.cjs');
const {verifyBinding} = require('../payment-backend/checkout-binding.cjs');
const key=Buffer.alloc(32,1), price='pri_0123456789abcdefghijklmnop', jwt='example-test-jwt-value-only';
const options={endpoint:'https://nyc.cloud.appwrite.io/v1',projectId:'project',environment:'sandbox',priceIds:{monthly:price},bindingKey:key};
function response(status,value={}) {return {status,ok:status>=200&&status<300,json:async()=>value};}
function service(fetchImpl, other={}) {return checkoutSessionService({...options,fetchImpl,...other});}
test('server verifies session and binds the authenticated account, not client-supplied user',async()=>{
  let call; const s=service(async(url,opts)=>{call={url,opts};return response(200,{$id:'auth_user'});});
  const r=await s({jwt,plan:'monthly',autoRenew:false,userId:'attacker'});assert.equal(r.status,200);
  const b=verifyBinding(r.body.customData.anastomosis_binding,key,'sandbox');assert.equal(b.userId,'auth_user');assert.equal(b.autoRenew,false);assert.equal(b.priceId,price);
  assert.equal(call.opts.headers['x-appwrite-jwt'],jwt);assert.equal(call.opts.headers['x-appwrite-project'],'project');
});
test('renewal preference is signed and defaults are not inferred from input',async()=>{
  const s=service(async()=>response(200,{$id:'auth_user'}));
  const yes=await s({jwt,plan:'monthly',autoRenew:true});assert.equal(verifyBinding(yes.body.customData.anastomosis_binding,key,'sandbox').autoRenew,true);
  assert.equal((await s({jwt,plan:'monthly'})).status,400);
});
test('invalid auth, unknown plans and outages fail closed',async()=>{
  let calls=0;const s=service(async()=>{calls++;return response(401)});
  assert.equal((await s({jwt:'',plan:'monthly',autoRenew:false})).status,401);assert.equal(calls,0);
  assert.equal((await s({jwt,plan:'fake',autoRenew:false})).status,400);assert.equal(calls,0);
  assert.equal((await s({jwt,plan:'monthly',autoRenew:false})).status,401);assert.equal(calls,1);
  const down=service(async()=>{throw Error('network detail')});const r=await down({jwt,plan:'monthly',autoRenew:false});assert.equal(r.status,503);assert.doesNotMatch(JSON.stringify(r),/network detail/);
});
test('rejects unsafe config and invalid authenticated account IDs',async()=>{
  assert.throws(()=>service(async()=>response(200),{endpoint:'https://evil.example/v1'}));
  assert.throws(()=>service(async()=>response(200),{bindingKey:Buffer.alloc(4)}));
  const s=service(async()=>response(200,{$id:'../../bad'}));assert.equal((await s({jwt,plan:'monthly',autoRenew:false})).status,503);
});
