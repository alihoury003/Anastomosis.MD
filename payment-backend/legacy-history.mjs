// Read-only compatibility helper for legacy dashboard preferences. These values
// are client-editable: they must NEVER grant access, a trial, or subscription.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const MAX_BYTES=2_000_000, MAX_RECORDS=5000, MAX_QUESTIONS=200, MAX_REFERENCES=100000;
function summarizeLegacyHistory(raw){
  let tests;
  if(typeof raw==='string'){
    if(new TextEncoder().encode(raw).length>MAX_BYTES)throw Error('Legacy history too large');
    try{tests=JSON.parse(raw);}catch(_){throw Error('Invalid legacy history');}
  }else tests=raw;
  if(!Array.isArray(tests)||tests.length>MAX_RECORDS)throw Error('Invalid legacy history');
  const records=[];let skipped=0,totalReferences=0;
  for(let i=0;i<tests.length;i++){
    const t=tests[i];
    if(!t||typeof t!=='object'||!Array.isArray(t.qIds)||t.qIds.length<1||t.qIds.length>MAX_QUESTIONS||t.qIds.some(id=>typeof id!=='string'||!ID.test(id))||new Set(t.qIds).size!==t.qIds.length){skipped++;continue;}
    totalReferences+=t.qIds.length;if(totalReferences>MAX_REFERENCES)throw Error('Legacy history too large');
    const suspended=t.status==='suspended',total=t.qIds.length;
    const score=Number.isInteger(t.score)&&t.score>=0&&t.score<=total&&t.total===total?t.score:null;
    // Never infer score from question data the user is no longer authorized to see.
    records.push({id:typeof t.id==='string'&&ID.test(t.id)?t.id:`legacy-${i}`,status:suspended?'suspended':'completed',title:typeof t.title==='string'?t.title.slice(0,120):'Block',dateLabel:typeof t.date==='string'?t.date.slice(0,80):null,finishedAt:typeof t.finishedAt==='string'&&Number.isFinite(Date.parse(t.finishedAt))?t.finishedAt:null,total,score:suspended?null:score,questionIds:[...t.qIds],source:'legacy-unverified'});
  }
  return{records,skipped,authorizationGranted:false};
}
export {summarizeLegacyHistory};
