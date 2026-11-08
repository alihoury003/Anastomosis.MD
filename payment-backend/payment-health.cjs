'use strict';
// Read-only operational summary. No customer IDs, event payloads, tokens or
// account data are returned. Logging this is NOT a substitute for alerting.
function createPaymentHealth({queue,checkpoints,clock=()=>Date.now(),maxPending=10,maxSilenceMs=3600000}){
  if(!queue||typeof queue.count!=='function'||!checkpoints||typeof checkpoints.read!=='function'||typeof clock!=='function'||!Number.isInteger(maxPending)||maxPending<0||!Number.isSafeInteger(maxSilenceMs)||maxSilenceMs<1)throw Error('Health not configured');
  return async function check(){
    try{
      const now=clock();if(!Number.isSafeInteger(now)||now<0)throw Error('Invalid clock');
      const [pending,manualReview,checkpoint]=await Promise.all([queue.count('pending'),queue.count('manual_review'),checkpoints.read()]);
      if(!Number.isSafeInteger(pending)||pending<0||!Number.isSafeInteger(manualReview)||manualReview<0)throw Error('Invalid counts');
      const ageMs=checkpoint&&Number.isSafeInteger(checkpoint.lastSuccessMs)&&checkpoint.lastSuccessMs<=now?now-checkpoint.lastSuccessMs:null;
      const reasons=[];if(ageMs===null)reasons.push('reconciliation_unconfirmed');else if(ageMs>maxSilenceMs)reasons.push('reconciliation_stale');if(pending>maxPending)reasons.push('event_backlog');if(manualReview>0)reasons.push('manual_review');
      return{ok:reasons.length===0,pending,manualReview,reconciliationAgeMs:ageMs,reasons};
    }catch(_){return{ok:false,reasons:['monitor_unavailable']};}
  };
}
module.exports={createPaymentHealth};
