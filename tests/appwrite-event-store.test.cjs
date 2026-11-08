'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { createEventArchive, MAX_STORED_BYTES } = require('../payment-backend/appwrite-event-store.cjs');
const id='evt_0123456789abcdefghijklmnop', type='transaction.completed', rawBody=Buffer.from('{"sample":"α"}');
function archive(fetchImpl, extra={}) { return createEventArchive({endpoint:'https://nyc.cloud.appwrite.io/v1',projectId:'project',databaseId:'db',collectionId:'events',apiKey:'local-test-key',fetchImpl,...extra}); }
function response(status, value={}) { return {status,ok:status>=200&&status<300,json:async()=>value}; }

test('creates a private pending event using deterministic event ID', async()=>{
  let call; const fn=archive(async(url,opts)=>{call={url,opts};return response(201)});
  assert.equal(await fn({id,type,rawBody}),'stored'); const json=JSON.parse(call.opts.body);
  assert.equal(json.documentId,id); assert.deepEqual(json.permissions,[]); assert.equal(json.data.processingStatus,'pending');
  assert.equal(json.data.payloadBase64,rawBody.toString('base64')); assert.equal(json.data.payloadSha256,crypto.createHash('sha256').update(rawBody).digest('hex'));
  assert.doesNotMatch(call.url,/local-test-key/);
});
test('true duplicates are accepted only after existing record is verified', async()=>{
  let n=0;const hash=crypto.createHash('sha256').update(rawBody).digest('hex');
  const fn=archive(async()=>++n===1?response(409,{type:'document_already_exists'}):response(200,{$id:id,eventType:type,payloadSha256:hash}));
  assert.equal(await fn({id,type,rawBody}),'duplicate'); assert.equal(n,2);
});
test('collision or unverified conflict fails closed', async()=>{
  let n=0;const fn=archive(async()=>++n===1?response(409,{type:'document_already_exists'}):response(200,{$id:id,eventType:type,payloadSha256:'different'}));
  await assert.rejects(fn({id,type,rawBody}),/collision/);
  const other=archive(async()=>response(409,{type:'other_conflict'})); await assert.rejects(other({id,type,rawBody}),/conflict/);
});
test('unavailable store, malformed input and oversized events never return success',async()=>{
  const fail=archive(async()=>response(500)); await assert.rejects(fail({id,type,rawBody}),/failed/);
  await assert.rejects(fail({id:'../../bad',type,rawBody}),/Invalid/);
  await assert.rejects(fail({id,type,rawBody:Buffer.alloc(MAX_STORED_BYTES+1)}),/Invalid/);
  assert.throws(()=>archive(async()=>response(201),{endpoint:'https://evil.example/v1'}));
});
