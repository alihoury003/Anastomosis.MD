'use strict';
const {evaluateSubscription}=require('./entitlement-policy.cjs');
const {evaluateOneTime}=require('./one-time-policy.cjs');
const {subscriptionReviewAllowed,oneTimeReviewAllowed}=require('./review-policy.cjs');
const {resolveAdjustments}=require('./resolve-adjustments.cjs');
// userId must come from verified Appwrite JWT; never trust a client ID.
function createEntitlementService({mappings,paddle,bindingKey,environment,allowedRecurringPriceIds,oneTimeDays,productId,reviews,clock=()=>Date.now()}){
  if(!mappings||typeof mappings.listByUser!=='function'||!reviews||typeof reviews.getDecision!=='function'||!paddle||typeof paddle.getSubscription!=='function'||typeof paddle.getTransaction!=='function'||typeof paddle.listAdjustments!=='function'||!Buffer.isBuffer(bindingKey)||bindingKey.length<32||!['sandbox','live'].includes(environment)||!Array.isArray(allowedRecurringPriceIds)||!allowedRecurringPriceIds.length||!oneTimeDays||typeof oneTimeDays!=='object'||!/^pro_[a-z0-9]{26}$/.test(productId||'')||typeof clock!=='function')throw Error('Entitlement service not configured');
  return async function check(userId){
    try{
      const now=clock();if(!Number.isSafeInteger(now)||now<0)throw Error('Invalid clock');
      const rows=await mappings.listByUser(userId);let best=null,reviewPending=false;const activeBillingIds=[],reviewableBillingIds=[];
      for(const row of rows){
        let decision,reviewAllowed;
        if(/^sub_[a-z0-9]{26}$/.test(row.$id||'')){
          const subscription=await paddle.getSubscription(row.$id),adjustments=await paddle.listAdjustments(row.$id);
          const resolved=await resolveAdjustments({adjustments,billingId:row.$id,userId,reviews});reviewPending ||= resolved.reviewPending;
          decision=evaluateSubscription({subscription,adjustments:resolved.effective,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,allowedPriceIds:allowedRecurringPriceIds,now});
          reviewAllowed=subscriptionReviewAllowed({subscription,adjustments:resolved.effective,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,allowedRecurringPriceIds,productId,now});
        }else if(/^txn_[a-z0-9]{26}$/.test(row.$id||'')){
          const transaction=await paddle.getTransaction(row.$id),adjustments=await paddle.listAdjustments(row.$id);
          const resolved=await resolveAdjustments({adjustments,billingId:row.$id,userId,reviews});reviewPending ||= resolved.reviewPending;
          const params={transaction,adjustments:resolved.effective,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,oneTimeDays,productId,now};
          decision=evaluateOneTime(params);reviewAllowed=oneTimeReviewAllowed(params);
        }else throw Error('Invalid mapping');
        if(reviewAllowed)reviewableBillingIds.push(row.$id);
        // Active grants must have the same verified ownership/review basis.
        if(decision.allowed&&reviewAllowed){activeBillingIds.push(row.$id);if(!best||Date.parse(decision.expiresAt)>Date.parse(best.expiresAt))best=decision;}
      }
      return{status:200,body:{subscribed:!!best,...(best?{expiresAt:best.expiresAt}:{}),activeBillingIds,reviewableBillingIds,reviewPending}};
    }catch(_){return{status:503,body:{error:'Subscription service unavailable'}};}
  };
}
module.exports={createEntitlementService};
