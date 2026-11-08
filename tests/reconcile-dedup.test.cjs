'use strict';const {test}=require('node:test');const assert=require('node:assert/strict');const {parseEvent}=require('../payment-backend/event-fingerprint.cjs');const {reconcileEvents}=require('../payment-backend/reconcile-events.cjs');
const id='evt_'+'1'.repeat(26),event={event_id:id,event_type:'transaction.completed',occurred_at:'2026-10-22T12:00:00Z',data:{id:'txn_'+'1'.repeat(26),status:'completed'}};
test('Paddle API replay and webhook delivery dedupe even with different notification IDs and key order',async()=>{
  const webhook=Buffer.from(JSON.stringify({...event,notification_id:'ntf_A'})),known=parseEvent(webhook).fingerprint;let after=null;
  const archive=async({rawBody})=>{assert.equal(parseEvent(rawBody).fingerprint,known);return'duplicate'};
  const checkpoints={read:async()=>null,advance:async(_expected,next)=>{after=next;return true}};
  const apiEvent={data:{status:'completed',id:'txn_'+'1'.repeat(26)},occurred_at:event.occurred_at,event_type:event.event_type,event_id:event.event_id};
  const result=await reconcileEvents({paddle:{listEventPage:async()=>({events:[apiEvent],hasMore:false})},archive,checkpoints,now:Date.parse('2026-10-22T12:01:00Z'),initialBackfillApproved:true});assert.equal(result.status,'caught_up');assert.equal(after,id);
});
test('semantically different events with the same ID have different fingerprints',()=>{const a=Buffer.from(JSON.stringify(event)),b=Buffer.from(JSON.stringify({...event,data:{...event.data,status:'canceled'}}));assert.notEqual(parseEvent(a).fingerprint,parseEvent(b).fingerprint);});
