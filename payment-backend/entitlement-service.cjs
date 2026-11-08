'use strict';
const {evaluateSubscription}=require('./entitlement-policy.cjs');
const {evaluateOneTime}=require('./one-time-policy.cjs');
// userId must come from verified Appwrite JWT; never trust a client ID.
function createEntitlementService({mappings,paddle,bindingKey,environment,allowedRecurringPriceIds,oneTimeDays,productId}){
  if(!mappings||typeof mappings.listByUser!=='function'||!paddle||typeof paddle.getSubscription!=='function'||typeof paddle.getTransaction!=='function'||typeof paddle.listAdjustments!=='function'||!Buffer.isBuffer(bindingKey)||bindingKey.length<32||!['sandbox','live'].includes(environment)||!Array.isArray(allowedRecurringPriceIds)||!allowedRecurringPriceIds.length||!oneTimeDays||typeof oneTimeDays!=='object'||!/^pro_[a-z0-9]{26}$/.test(productId||''))throw Error('Entitlement service not configured');
  return async function check(userId){
    try{
      const rows=await mappings.listByUser(userId);let best=null;
      for(const row of rows){
        let decision;
        if(/^sub_[a-z0-9]{26}$/.test(row.$id||'')){
          const subscription=await paddle.getSubscription(row.$id),adjustments=await paddle.listAdjustments(row.$id);
          decision=evaluateSubscription({subscription,adjustments,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,allowedPriceIds:allowedRecurringPriceIds});
        }else if(/^txn_[a-z0-9]{26}$/.test(row.$id||'')){
          const transaction=await paddle.getTransaction(row.$id),adjustments=await paddle.listAdjustments(row.$id);
          decision=evaluateOneTime({transaction,adjustments,adjustmentsComplete:true,authenticatedUserId:userId,bindingKey,environment,oneTimeDays,productId});
        }else throw Error('Invalid mapping');
        if(decision.allowed&&(!best||Date.parse(decision.expiresAt)>Date.parse(best.expiresAt)))best=decision;
      }
      return{status:200,body:{subscribed:!!best,...(best?{expiresAt:best.expiresAt}:{})}};
    }catch(_){return{status:503,body:{error:'Subscription service unavailable'}};}
  };
}
module.exports={createEntitlementService};
