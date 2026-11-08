'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const handlerPromise = import(pathToFileURL(path.resolve('payment-backend/src/main.mjs')).href).then(m=>m.default);
const secret='test-secret-never-real';
const event={event_id:'evt_0123456789abcdefghijklmnop',event_type:'subscription.updated',occurred_at:'2026-10-22T12:00:00Z',data:{id:'sub_example'}};
const body=Buffer.from(JSON.stringify(event));
function signed() { const ts=Math.floor(Date.now()/1000);const h=crypto.createHmac('sha256',secret).update(`${ts}:`).update(body).digest('hex');return `ts=${ts};h1=${h}`; }
const res={ text:(body,status)=>({body,status}) };
function req(signature=signed()){return {method:'POST',bodyBinary:body,headers:{'paddle-signature':signature}};}
function response(status,value={}) {return {status,ok:status>=200&&status<300,json:async()=>value};}
const keys=['PAYMENT_QUEUE_ENABLED','APPWRITE_FUNCTION_API_ENDPOINT','APPWRITE_FUNCTION_PROJECT_ID','PAYMENT_EVENT_DATABASE','PAYMENT_EVENT_COLLECTION','PAYMENT_EVENT_API_KEY','PADDLE_WEBHOOK_SECRET'];
async function withConfig(fn) {
  const old=Object.fromEntries(keys.map(k=>[k,process.env[k]]));const oldFetch=globalThis.fetch;
  Object.assign(process.env,{PAYMENT_QUEUE_ENABLED:'true',APPWRITE_FUNCTION_API_ENDPOINT:'https://nyc.cloud.appwrite.io/v1',APPWRITE_FUNCTION_PROJECT_ID:'project',PAYMENT_EVENT_DATABASE:'db',PAYMENT_EVENT_COLLECTION:'events',PAYMENT_EVENT_API_KEY:'dummy-api-key',PADDLE_WEBHOOK_SECRET:secret});
  try {await fn();} finally {globalThis.fetch=oldFetch;for (const k of keys) {if(old[k]===undefined) delete process.env[k]; else process.env[k]=old[k];}}
}
test('deployed receiver stays disabled unless explicitly enabled',async()=>withConfig(async()=>{
  process.env.PAYMENT_QUEUE_ENABLED='false';let count=0;globalThis.fetch=async()=>{count++;return response(201);};
  const out=await (await handlerPromise)({req:req(),res});assert.equal(out.status,503);assert.equal(count,0);
}));
test('signed Paddle notification reaches private archive',async()=>withConfig(async()=>{
  let writes=[];globalThis.fetch=async(url,options)=>{writes.push({url,options});return response(201);};
  const out=await (await handlerPromise)({req:req(),res});assert.equal(out.status,200);assert.equal(writes.length,1);
  const saved=JSON.parse(writes[0].options.body);assert.equal(saved.documentId,event.event_id);assert.deepEqual(saved.permissions,[]);assert.equal(saved.data.processingStatus,'pending');
}));
test('bad signature and storage failure do not acknowledge an event',async()=>withConfig(async()=>{
  let count=0;globalThis.fetch=async()=>{count++;return response(500);};const handler=await handlerPromise;
  assert.equal((await handler({req:req('ts=1;h1=bad'),res})).status,401);assert.equal(count,0);
  assert.equal((await handler({req:req(),res})).status,503);assert.equal(count,1);
}));
