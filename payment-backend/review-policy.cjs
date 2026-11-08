'use strict';
const {verifyBinding}=require('./checkout-binding.cjs');
const {evaluateOneTime}=require('./one-time-policy.cjs');
const SUB=/^sub_[a-z0-9]{26}$/;
const ACTIONS=['refund','credit','chargeback','chargeback_reverse','chargeback_warning','chargeback_warning_reverse','credit_reverse'];
const STATES=['pending_approval','approved','rejected','reversed'];
// These helpers only evaluate authenticated Paddle responses. They do not
// grant access or trust a browser-provided subscription/transaction object.
function subscriptionReviewAllowed({subscription,adjustments,adjustmentsComplete,authenticatedUserId,bindingKey,environment,allowedRecurringPriceIds,productId,now=Date.now()}){
  if(!subscription||!SUB.test(subscription.id||'')||adjustmentsComplete!==true||!Array.isArray(adjustments)||!Array.isArray(allowedRecurringPriceIds)||!/^pro_[a-z0-9]{26}$/.test(productId||'')||!Number.isFinite(now))return false;
  const claim=verifyBinding(subscription.custom_data?.anastomosis_binding,bindingKey,environment),billed=Date.parse(subscription.first_billed_at);
  if(!claim||claim.userId!==authenticatedUserId||claim.autoRenew!==true||!allowedRecurringPriceIds.includes(claim.priceId)||!Number.isFinite(billed)||billed>now||!['active','canceled','paused','past_due'].includes(subscription.status))return false;
  if(!Array.isArray(subscription.items)||!subscription.items.some(x=>x?.price?.id===claim.priceId&&x.price.product_id===productId))return false;
  for(const a of adjustments){if(!a||a.subscription_id!==subscription.id||!STATES.includes(a.status)||!ACTIONS.includes(a.action))return false;if(a.status==='approved'&&['refund','credit','chargeback'].includes(a.action))return false;}
  return true;
}
function oneTimeReviewAllowed(input){
  const tx=input?.transaction,now=input?.now??Date.now();
  if(!Number.isFinite(now)||!Array.isArray(tx?.payments))return false;
  const times=tx.payments.filter(x=>x?.status==='captured').map(x=>Date.parse(x.captured_at)).filter(Number.isFinite);
  if(!times.length)return false;const capturedAt=Math.max(...times);if(capturedAt>now)return false;
  // Validate the same purchase, identity, product and adjustments at capture;
  // expiry does not erase the right to revisit previously delivered items.
  return evaluateOneTime({...input,now:capturedAt}).allowed===true;
}
module.exports={subscriptionReviewAllowed,oneTimeReviewAllowed};
