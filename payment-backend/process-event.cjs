'use strict';
const {verifyBinding}=require('./checkout-binding.cjs');
const SUB=/^sub_[a-z0-9]{26}$/,TXN=/^txn_[a-z0-9]{26}$/,ADJ=/^adj_[a-z0-9]{26}$/,EVENT=/^evt_[a-z0-9]{26}$/,PRODUCT=/^pro_[a-z0-9]{26}$/;
const SUB_TYPES=new Set(['subscription.created','subscription.updated','subscription.activated','subscription.canceled','subscription.paused','subscription.resumed','subscription.past_due']);
const ADJ_TYPES=new Set(['adjustment.created','adjustment.updated']);
// Call ONLY for an authenticated event from the private verified queue.
// Fetch current entities from Paddle, never trust client event metadata alone.
// Mapping storage must be private, immutable, atomic and idempotent.
// No subscription is canceled by this worker: a nonrenewing purchase must use
// a one-time Paddle price, never a recurring price with a later cancellation.
async function processEvent(event,{paddle,mappings,reviews,bindingKey,environment,allowedRecurringPriceIds,oneTimeDays,productId}){
  if(!event||!EVENT.test(event.event_id||'')||typeof event.event_type!=='string'||!event.data||!paddle||typeof paddle.getSubscription!=='function'||typeof paddle.getTransaction!=='function'||!mappings||typeof mappings.save!=='function'||!Array.isArray(allowedRecurringPriceIds)||!oneTimeDays||typeof oneTimeDays!=='object'||!PRODUCT.test(productId||''))throw Error('Invalid event processing configuration');
  let subscriptionId=null,transactionId=null,adjustment=null;
  if(SUB_TYPES.has(event.event_type))subscriptionId=event.data.id;
  else if(event.event_type==='transaction.completed')transactionId=event.data.id;
  else if(ADJ_TYPES.has(event.event_type)){
    if(!ADJ.test(event.data.id||''))return{status:'manual_review'};
    if(typeof paddle.getAdjustment!=='function'||!reviews||typeof reviews.sync!=='function')throw Error('Refund review not configured');
    adjustment=await paddle.getAdjustment(event.data.id);
    if(!adjustment||adjustment.id!==event.data.id)throw Error('Adjustment lookup failed');
    subscriptionId=adjustment.subscription_id;transactionId=subscriptionId?null:adjustment.transaction_id;
  }
  else return{status:'ignored'};
  if(subscriptionId){
    if(!SUB.test(subscriptionId))return{status:'manual_review'};
    const subscription=await paddle.getSubscription(subscriptionId);
    if(!subscription||subscription.id!==subscriptionId)throw Error('Subscription lookup failed');
    const binding=verifyBinding(subscription.custom_data?.anastomosis_binding,bindingKey,environment);
    if(!binding||binding.autoRenew!==true||!allowedRecurringPriceIds.includes(binding.priceId))return{status:'manual_review'};
    if(!Array.isArray(subscription.items)||!subscription.items.some(item=>item?.price?.id===binding.priceId&&item.price.product_id===productId&&item.price.billing_cycle&&typeof item.price.billing_cycle==='object'))return{status:'manual_review'};
    await mappings.save({subscriptionId,userId:binding.userId,priceId:binding.priceId,environment,autoRenew:true,nonce:binding.nonce});
    if(adjustment)await reviews.sync({adjustment,billingId:subscriptionId,userId:binding.userId});
    return{status:'mapped',billingId:subscriptionId};
  }
  if(!TXN.test(transactionId||''))return{status:'manual_review'};
  const transaction=await paddle.getTransaction(transactionId);
  if(!transaction||transaction.id!==transactionId)throw Error('Transaction lookup failed');
  if(transaction.subscription_id!==null)return{status:adjustment?'manual_review':'ignored'};
  if(transaction.status!=='completed')throw Error('Transaction not completed');
  const binding=verifyBinding(transaction.custom_data?.anastomosis_binding,bindingKey,environment);
  if(!binding||binding.autoRenew!==false||!Object.hasOwn(oneTimeDays,binding.priceId)||![30,90,365].includes(oneTimeDays[binding.priceId]))return{status:'manual_review'};
  if(!['web','api'].includes(transaction.origin)||!Array.isArray(transaction.items)||transaction.items.length!==1)return{status:'manual_review'};
  const item=transaction.items[0];
  if(item.quantity!==1||item.price?.id!==binding.priceId||item.price.product_id!==productId||item.price.billing_cycle!==null)return{status:'manual_review'};
  if(!Array.isArray(transaction.payments)||!transaction.payments.some(p=>p?.status==='captured'&&Number.isFinite(Date.parse(p.captured_at))))return{status:'manual_review'};
  await mappings.save({transactionId,userId:binding.userId,priceId:binding.priceId,environment,autoRenew:false,nonce:binding.nonce});
  if(adjustment)await reviews.sync({adjustment,billingId:transactionId,userId:binding.userId});
  return{status:'mapped',billingId:transactionId};
}
module.exports={processEvent};
