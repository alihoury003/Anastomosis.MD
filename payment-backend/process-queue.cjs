'use strict';
const crypto=require('node:crypto');
const {processEvent}=require('./process-event.cjs');
// Process one previously verified, privately stored queue record. The store must
// never expose write access to clients. Marking success happens after processing;
// transient failures leave the record pending for retry. Monitoring and periodic
// reconciliation are still required and are NOT provided by this module.
async function processQueuedRecord(record,{dependencies,queue}) {
  if (!record || !/^evt_[a-z0-9]{26}$/.test(record.$id||'') || record.processingStatus!=='pending' ||
      typeof record.payloadBase64!=='string' || record.payloadBase64.length>44000 ||
      typeof record.payloadSha256!=='string' || !/^[a-f0-9]{64}$/.test(record.payloadSha256) ||
      !queue || typeof queue.complete!=='function') throw Error('Invalid queue record');
  const raw=Buffer.from(record.payloadBase64,'base64');
  if(raw.toString('base64')!==record.payloadBase64 || crypto.createHash('sha256').update(raw).digest('hex')!==record.payloadSha256) throw Error('Corrupt queue record');
  let event;try{event=JSON.parse(raw.toString('utf8'));}catch(_){throw Error('Invalid queue payload');}
  if(event?.event_id!==record.$id || event?.event_type!==record.eventType) throw Error('Queue event mismatch');
  const result=await processEvent(event,dependencies);
  // manual_review must be surfaced to an operator, not silently discarded.
  await queue.complete(record.$id,result.status==='manual_review'?'manual_review':'done');
  return result;
}
module.exports={processQueuedRecord};
