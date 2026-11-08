'use strict';
const {verifyBinding}=require('./checkout-binding.cjs');
const SUB=/^sub_[a-z0-9]{26}$/;
const EVENT=/^evt_[a-z0-9]{26}$/;
const SUB_TYPES=new Set(['subscription.created','subscription.updated','subscription.activated','subscription.canceled','subscription.paused','subscription.resumed','subscription.past_due']);
const ADJ_TYPES=new Set(['adjustment.created','adjustment.updated']);
function confirmedCancellation(subscription) {
  const end=Date.parse(subscription.current_billing_period?.ends_at);
  const effective=Date.parse(subscription.scheduled_change?.effective_at);
  return subscription.scheduled_change?.action==='cancel' && Number.isFinite(end) && Number.isFinite(effective) && effective<=end && effective>Date.now();
}

// Call ONLY for an authenticated event read from the private verified queue.
// `mappings.save` must atomically create an immutable sub->user mapping, and
// reject conflicts; `paddle` must use the server's authenticated Paddle API.
// A worker must retry failed events and reconcile periodically. This function
// does not process free-tier limits, grant labels or change table permissions.
async function processEvent(event, {paddle, mappings, bindingKey, environment, allowedPriceIds}) {
  if (!event || !EVENT.test(event.event_id || '') || typeof event.event_type !== 'string' || !event.data ||
      !paddle || typeof paddle.getSubscription!=='function' || typeof paddle.scheduleCancellation!=='function' ||
      !mappings || typeof mappings.save!=='function' || !Array.isArray(allowedPriceIds)) throw Error('Invalid event processing configuration');
  let subscriptionId;
  if (SUB_TYPES.has(event.event_type)) subscriptionId=event.data.id;
  else if (ADJ_TYPES.has(event.event_type)) subscriptionId=event.data.subscription_id;
  else return {status:'ignored'};
  if (!SUB.test(subscriptionId || '')) return {status:'manual_review'};
  const subscription=await paddle.getSubscription(subscriptionId);
  if (!subscription || subscription.id !== subscriptionId) throw Error('Subscription lookup failed');
  const binding=verifyBinding(subscription.custom_data?.anastomosis_binding,bindingKey,environment);
  if (!binding || !allowedPriceIds.includes(binding.priceId)) return {status:'manual_review'};
  if (!Array.isArray(subscription.items) || !subscription.items.some(item=>item?.price?.id === binding.priceId)) return {status:'manual_review'};
  const mapping={subscriptionId,userId:binding.userId,priceId:binding.priceId,environment,autoRenew:binding.autoRenew,nonce:binding.nonce};
  // The mapping is immutable so retries cannot reassign a customer account.
  await mappings.save(mapping);
  if (!binding.autoRenew && ['active','trialing','past_due'].includes(subscription.status)) {
    if (!confirmedCancellation(subscription)) {
      // Never ack this event as processed if Paddle fails; retry and alert.
      const updated=await paddle.scheduleCancellation(subscriptionId);
      if (!updated || updated.id!==subscriptionId || !confirmedCancellation(updated)) throw Error('Nonrenewal not confirmed');
    }
  }
  return {status:'mapped',subscriptionId};
}
module.exports={processEvent};
