'use strict';
const {classifyAdjustment}=require('./adjustment-policy.cjs');
// Run only on complete, authenticated Paddle adjustment responses. A private
// operator decision overrides the default only for the exact Paddle version.
async function resolveAdjustments({adjustments,billingId,userId,reviews}){
  if(!Array.isArray(adjustments)||!reviews||typeof reviews.getDecision!=='function')throw Error('Adjustment review unavailable');
  const effective=[];let reviewPending=false;
  for(const adjustment of adjustments){
    const classification=classifyAdjustment(adjustment,billingId);if(!classification.valid)throw Error('Invalid adjustment');
    if(!classification.needsReview){effective.push(adjustment);continue;}
    const decision=await reviews.getDecision({adjustment,billingId,userId});
    if(![null,'allow','restrict'].includes(decision))throw Error('Invalid review decision');
    if(decision===null)reviewPending=true;
    const restricted=decision==='restrict'||(decision===null&&classification.defaultRestriction);
    if(restricted)effective.push(adjustment);
  }
  return{effective,reviewPending};
}
module.exports={resolveAdjustments};
