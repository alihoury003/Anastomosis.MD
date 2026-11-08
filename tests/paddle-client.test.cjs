'use strict';
const {test}=require('node:test');const assert=require('node:assert/strict');
const {createPaddleClient}=require('../payment-backend/paddle-client.cjs');
const id='sub_0123456789abcdefghijklmnop';
function response(status,data){return{ok:status>=200&&status<300,status,json:async()=>data};}
function client(fetchImpl,environment='sandbox'){return createPaddleClient({environment,apiKey:'test-only-key',fetchImpl});}
test('reads subscription using the selected environment and validates response ID',async()=>{
  let seen;const p=client(async(url,opts)=>{seen={url,opts};return response(200,{data:{id,status:'active'}})});
  assert.equal((await p.getSubscription(id)).status,'active');assert.match(seen.url,/^https:\/\/sandbox-api\.paddle\.com\/subscriptions\//);assert.equal(seen.opts.redirect,'error');assert.doesNotMatch(seen.url,/test-only-key/);
  await assert.rejects(p.getSubscription('../bad'),/Invalid subscription/);
  const mismatch=client(async()=>response(200,{data:{id:'different'}}));await assert.rejects(mismatch.getSubscription(id),/Invalid Paddle/);
});
test('reads all adjustment pages and preserves the subscription filter',async()=>{
  let n=0;const p=client(async(url)=>{n++;if(n===1)return response(200,{data:[{subscription_id:id}],meta:{pagination:{has_more:true,next:`https://sandbox-api.paddle.com/adjustments?subscription_id=${id}&per_page=50&after=adj_abc`}}});return response(200,{data:[{subscription_id:id}],meta:{pagination:{has_more:false}}});});
  assert.equal((await p.listAdjustments(id)).length,2);assert.equal(n,2);
});
test('rejects malicious or incomplete pagination without exposing the API key',async()=>{
  for(const next of ['https://evil.example/adjustments?after=abc','https://sandbox-api.paddle.com/adjustments?after=abc',`https://sandbox-api.paddle.com/adjustments?subscription_id=${id}`]){
    const p=client(async()=>response(200,{data:[],meta:{pagination:{has_more:true,next}}}));await assert.rejects(p.listAdjustments(id),/Invalid Paddle pagination/);
  }
  const bad=client(async()=>response(200,{data:[{subscription_id:'other'}],meta:{pagination:{has_more:false}}}));await assert.rejects(bad.listAdjustments(id),/Unexpected adjustment/);
  const noMeta=client(async()=>response(200,{data:[]}));await assert.rejects(noMeta.listAdjustments(id),/Invalid Paddle response/);
});
test('service failures fail closed and config is mandatory',async()=>{
  const p=client(async()=>response(403,{}),'live');await assert.rejects(p.getSubscription(id),/request failed/);
  assert.throws(()=>createPaddleClient({environment:'production',apiKey:'key'}));assert.throws(()=>createPaddleClient({environment:'live',apiKey:''}));
});
test('reads price and transaction only from the selected Paddle API',async()=>{const pid='pri_0123456789abcdefghijklmnop',tid='txn_0123456789abcdefghijklmnop';let calls=[];const p=client(async(url)=>{calls.push(url);return response(200,{data:{id:url.endsWith(pid)?pid:tid}})});assert.equal((await p.getPrice(pid)).id,pid);assert.equal((await p.getTransaction(tid)).id,tid);assert.ok(calls.every(x=>x.startsWith('https://sandbox-api.paddle.com/')));await assert.rejects(p.getPrice('../bad'));});
test('transaction adjustments are filtered by transaction ID',async()=>{const tid='txn_0123456789abcdefghijklmnop';let url;const p=client(async u=>{url=u;return response(200,{data:[{transaction_id:tid}],meta:{pagination:{has_more:false}}});});assert.equal((await p.listAdjustments(tid)).length,1);assert.equal(new URL(url).searchParams.get('transaction_id'),tid);});
