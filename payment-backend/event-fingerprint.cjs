'use strict';
const crypto=require('node:crypto');
const decoder=new TextDecoder('utf-8',{fatal:true});
function canonical(value,depth=0){
  if(depth>60)throw Error('Payload too deeply nested');
  if(value===null||typeof value==='string'||typeof value==='boolean')return JSON.stringify(value);
  if(typeof value==='number'&&Number.isFinite(value))return JSON.stringify(value);
  if(Array.isArray(value))return '['+value.map(v=>canonical(v,depth+1)).join(',')+']';
  if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k],depth+1)).join(',')+'}';
  throw Error('Invalid payload value');
}
function parseEvent(rawBody){
  if(!Buffer.isBuffer(rawBody))throw Error('Raw body required');
  const event=JSON.parse(decoder.decode(rawBody));
  if(!event||typeof event!=='object'||Array.isArray(event)||typeof event.event_id!=='string'||!/^evt_[a-z0-9]{26}$/.test(event.event_id)||
     typeof event.event_type!=='string'||!/^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$/.test(event.event_type)||
     typeof event.occurred_at!=='string'||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(event.occurred_at)||!Number.isFinite(Date.parse(event.occurred_at))||
     !event.data||typeof event.data!=='object'||Array.isArray(event.data))throw Error('Invalid event');
  const canonicalEvent=canonical({event_id:event.event_id,event_type:event.event_type,occurred_at:event.occurred_at,data:event.data});
  return{event,fingerprint:crypto.createHash('sha256').update(canonicalEvent,'utf8').digest('hex')};
}
module.exports={parseEvent};
