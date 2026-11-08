'use strict';
// This exercises the candidate functions together against an in-memory fake.
// It is NOT a real Paddle/Appwrite integration test or production certification.
const {test}=require('node:test');const assert=require('node:assert/strict');const crypto=require('node:crypto');const {pathToFileURL}=require('node:url');const path=require('node:path');
async function fn(name){return(await import(pathToFileURL(path.resolve(`payment-backend/src/${name}.mjs`)).href)).default;}
const price='pri_0123456789abcdefghijklmnop',sid='sub_0123456789abcdefghijklmnop',eid='evt_0123456789abcdefghijklmnop',key=Buffer.alloc(32,11),secret='simulated-webhook-secret';
const env={CHECKOUT_SESSION_ENABLED:'true',PAYMENT_QUEUE_ENABLED:'true',PAYMENT_PROCESSOR_ENABLED:'true',PAYMENT_ACCESS_ENABLED:'true',PADDLE_ALLOW_CANCELLATION:'true',CHECKOUT_BINDING_KEY_BASE64:key.toString('base64'),APPWRITE_FUNCTION_API_ENDPOINT:'https://nyc.cloud.appwrite.io/v1',APPWRITE_FUNCTION_PROJECT_ID:'project',PAYMENT_EVENT_DATABASE:'db',PAYMENT_EVENT_COLLECTION:'events',PAYMENT_MAPPING_COLLECTION:'mappings',PAYMENT_EVENT_API_KEY:'fake',PADDLE_ENVIRONMENT:'sandbox',PADDLE_API_KEY:'fake',PADDLE_WEBHOOK_SECRET:secret,PADDLE_MONTHLY_PRICE:price,PADDLE_THREE_MONTH_PRICE:price,PADDLE_ANNUAL_PRICE:price};
const res={text:(body,status)=>({body,status}),json:(body,status)=>({body,status})};function reply(status,data={}){return{status,ok:status>=200&&status<300,json:async()=>data};}
async function run(fn){const old=Object.fromEntries(Object.keys(env).map(k=>[k,process.env[k]])),oldFetch=globalThis.fetch;Object.assign(process.env,env);try{await fn();}finally{globalThis.fetch=oldFetch;for(const k in env){if(old[k]===undefined)delete process.env[k];else process.env[k]=old[k];}}}
test('mock purchase maps the authenticated user, schedules no-renewal, verifies paid access and revokes on cancellation',async()=>run(async()=>{
  const docs={events:new Map(),mappings:new Map()};let subscription, adjustments=[];
  globalThis.fetch=async(url,opts={})=>{
    const u=new URL(url),method=opts.method||'GET';
    if(u.origin==='https://nyc.cloud.appwrite.io' && u.pathname==='/v1/account')return reply(200,{$id:opts.headers['x-appwrite-jwt']==='other-user-jwt-value-123'?'other':'user1'});
    const m=u.pathname.match(/^\/v1\/databases\/db\/collections\/(events|mappings)\/documents(?:\/([^/]+))?$/);
    if(u.origin==='https://nyc.cloud.appwrite.io'&&m){const map=docs[m[1]];if(method==='POST'){const body=JSON.parse(opts.body);if(map.has(body.documentId))return reply(409,{type:'document_already_exists'});map.set(body.documentId,{$id:body.documentId,...body.data});return reply(201,{});}if(method==='PATCH'){const rec=map.get(m[2]);if(!rec)return reply(404);Object.assign(rec,JSON.parse(opts.body).data);return reply(200,rec);}if(method==='GET'&&m[2])return map.has(m[2])?reply(200,map.get(m[2])):reply(404);if(method==='GET'){const queries=u.searchParams.getAll('queries[]').map(JSON.parse),eq=queries.find(q=>q.method==='equal');const rows=[...map.values()].filter(r=>r[eq.attribute]===eq.values[0]);return reply(200,{total:rows.length,documents:rows});}}
    if(u.origin==='https://sandbox-api.paddle.com'&&u.pathname===`/subscriptions/${sid}`&&method==='GET')return reply(200,{data:subscription});
    if(u.origin==='https://sandbox-api.paddle.com'&&u.pathname===`/subscriptions/${sid}/cancel`&&method==='POST'){assert.equal(JSON.parse(opts.body).effective_from,'next_billing_period');subscription.scheduled_change={action:'cancel',effective_at:subscription.current_billing_period.ends_at};return reply(200,{data:subscription});}
    if(u.origin==='https://sandbox-api.paddle.com'&&u.pathname==='/adjustments')return reply(200,{data:adjustments,meta:{pagination:{has_more:false}}});
    throw Error('unexpected mock request');
  };
  const checkout=await fn('checkout'),webhook=await fn('main'),worker=await fn('worker'),access=await fn('access');const jwt='valid-test-jwt-value-for-user1';
  const created=await checkout({req:{method:'POST',headers:{'x-appwrite-user-jwt':jwt},bodyText:JSON.stringify({plan:'monthly',autoRenew:false})},res});assert.equal(created.status,200);
  subscription={id:sid,status:'active',first_billed_at:'2020-01-01T00:00:00Z',current_billing_period:{starts_at:'2020-01-01T00:00:00Z',ends_at:'2099-01-01T00:00:00Z'},scheduled_change:null,items:[{status:'active',price:{id:price}}],custom_data:created.body.customData};
  const event={event_id:eid,event_type:'subscription.created',occurred_at:'2026-10-22T12:00:00Z',data:{id:sid}},body=Buffer.from(JSON.stringify(event)),ts=Math.floor(Date.now()/1000),mac=crypto.createHmac('sha256',secret).update(`${ts}:`).update(body).digest('hex');
  const received=await webhook({req:{method:'POST',headers:{'paddle-signature':`ts=${ts};h1=${mac}`},bodyBinary:body},res});assert.equal(received.status,200);
  const processed=await worker({req:{headers:{'x-appwrite-trigger':'schedule'}},res,error:()=>{}});assert.equal(processed.status,200);assert.equal(subscription.scheduled_change.action,'cancel');assert.equal(docs.events.get(eid).processingStatus,'done');
  const accessRequest=(token)=>({req:{method:'GET',headers:{'x-appwrite-user-jwt':token}},res});
  assert.equal((await access(accessRequest(jwt))).body.subscribed,true);assert.equal((await access(accessRequest('other-user-jwt-value-123'))).body.subscribed,false);
  // Link the mocked payment access result to the mocked private question gate.
  const {createQuestionAccess}=require('../payment-backend/question-access.cjs');let state=null;
  const questionGate=createQuestionAccess({questions:{get:async id=>({$id:id,stem:'protected',correct:'A'})},usage:{transact:async(_user,fn)=>{const out=await fn(state);state=out.state;return out.result;}},entitlements:{check:async()=>access(accessRequest(jwt))}});
  assert.equal((await questionGate.getQuestion('user1','question1')).body.source,'paid');
  adjustments=[{subscription_id:sid,status:'approved',action:'refund'}];assert.equal((await access(accessRequest(jwt))).body.subscribed,false);
  assert.equal((await questionGate.getQuestion('user1','question2')).body.source,'free');
  adjustments=[];subscription.status='canceled';assert.equal((await access(accessRequest(jwt))).body.subscribed,false);
}));
