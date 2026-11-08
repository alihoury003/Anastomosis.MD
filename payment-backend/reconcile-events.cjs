'use strict';
const {parseEvent}=require('./event-fingerprint.cjs');
const RETENTION_WARNING_MS=89*86400000;
// Scheduled server-only work: Paddle's authenticated Events API is the
// authority here. The checkpoint adapter must be private and atomic. It does
// not replace a full historical backfill or manual review of unmatched sales.
async function reconcileEvents({paddle,archive,checkpoints,now=Date.now(),initialBackfillApproved=false,maxPages=1,pageSize=10}){
  if(!paddle||typeof paddle.listEventPage!=='function'||typeof archive!=='function'||!checkpoints||typeof checkpoints.read!=='function'||typeof checkpoints.advance!=='function'||!Number.isSafeInteger(now)||now<0||!Number.isInteger(maxPages)||maxPages<1||maxPages>5||!Number.isInteger(pageSize)||pageSize<1||pageSize>50)throw Error('Reconciler not configured');
  const checkpoint=await checkpoints.read();
  if(!checkpoint&&!initialBackfillApproved)return{status:'baseline_required',archived:0};
  if(checkpoint&&(!Number.isSafeInteger(checkpoint.lastSuccessMs)||checkpoint.lastSuccessMs>now))return{status:'clock_error',archived:0};
  if(checkpoint&&now-checkpoint.lastSuccessMs>=RETENTION_WARNING_MS)return{status:'retention_risk',archived:0};
  let cursor=checkpoint?.after??null,archived=0;
  for(let pageNo=0;pageNo<maxPages;pageNo++){
    const page=await paddle.listEventPage({after:cursor,limit:pageSize});
    if(!page||!Array.isArray(page.events)||typeof page.hasMore!=='boolean'||page.events.length>pageSize)throw Error('Invalid reconciliation page');
    // A live backlog near Paddle's retention boundary needs manual backfill;
    // stopping avoids reporting a healthy catch-up after events may be lost.
    for(const event of page.events){const occurred=Date.parse(event?.occurred_at);if(!Number.isFinite(occurred))throw Error('Invalid event time');if(now-occurred>=RETENTION_WARNING_MS)return{status:'retention_risk',archived};}
    let latest=cursor;
    for(const event of page.events){
      const rawBody=Buffer.from(JSON.stringify(event),'utf8'),parsed=parseEvent(rawBody).event;
      if(latest&&parsed.event_id<=latest)throw Error('Unordered reconciliation page');
      const result=await archive({id:parsed.event_id,type:parsed.event_type,rawBody});
      if(!['stored','duplicate'].includes(result))throw Error('Event archive failed');
      latest=parsed.event_id;archived++;
    }
    if(page.hasMore&&!page.events.length)throw Error('Invalid reconciliation page');
    if(!await checkpoints.advance(cursor,latest,now))return{status:'concurrent',archived};
    cursor=latest;
    if(!page.hasMore)return{status:'caught_up',archived};
  }
  return{status:'more',archived};
}
module.exports={reconcileEvents,RETENTION_WARNING_MS};
