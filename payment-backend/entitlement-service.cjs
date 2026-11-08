'use strict';
const {evaluateSubscription}=require('./entitlement-policy.cjs');
// `userId` must come from verified Appwrite JWT. Mappings and Paddle data are
// fetched server-side; a client-provided subscription ID is never trusted.
function createEntitlementService({mappings,paddle,bindingKey,environment,allowedPriceIds}) {
  if(!mappings||typeof mappings.listByUser!=='function'||!paddle||typeof paddle.getSubscription!=='function'||typeof paddle.listAdjustments!=='function'||!Buffer.isBuffer(bindingKey)||bindingKey.length<32||!['sandbox','live'].includes(environment)||!Array.isArray(allowedPriceIds)||!allowedPriceIds.length)throw Error('Entitlement service not configured');
  return async function check(userId) {
    try {
      const rows=await mappings.listByUser(userId);let best=null;
      for(const row of rows) {
        const subscription=await paddle.getSubscription(row.$id);
        const adjustments=await paddle.listAdjustments(row.$id);
        const decision=evaluateSubscription({subscription,adjustments,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,allowedPriceIds});
        if(decision.allowed&&(!best||Date.parse(decision.expiresAt)>Date.parse(best.expiresAt)))best=decision;
      }
      return {status:200,body:{subscribed:!!best,...(best?{expiresAt:best.expiresAt}:{})}};
    } catch (_) {return {status:503,body:{error:'Subscription service unavailable'}};}
  };
}
module.exports={createEntitlementService};
