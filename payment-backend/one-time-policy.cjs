'use strict';
const {verifyBinding}=require('./checkout-binding.cjs');
const TXN=/^txn_[a-z0-9]{26}$/;
const PRICE=/^pri_[a-z0-9]{26}$/;
const PRODUCT=/^pro_[a-z0-9]{26}$/;
const VALID_DAYS=new Set([30,90,365]);
// All transaction and adjustment fields must be fetched from Paddle server-side.
function evaluateOneTime({transaction,adjustments,adjustmentsComplete,authenticatedUserId,bindingKey,environment,oneTimeDays,productId,now=Date.now()}){
  const deny=reason=>({allowed:false,reason});
  if(!transaction||!TXN.test(transaction.id||'')||typeof authenticatedUserId!=='string'||adjustmentsComplete!==true||!Array.isArray(adjustments)||!PRODUCT.test(productId||'')||!oneTimeDays||typeof oneTimeDays!=='object'||!Number.isFinite(now))return deny('invalid_or_incomplete_data');
  const claim=verifyBinding(transaction.custom_data?.anastomosis_binding,bindingKey,environment);
  if(!claim||claim.userId!==authenticatedUserId||claim.autoRenew!==false||!PRICE.test(claim.priceId)||!Object.hasOwn(oneTimeDays,claim.priceId)||!VALID_DAYS.has(oneTimeDays[claim.priceId]))return deny('unverified_account_binding');
  if(transaction.status!=='completed'||transaction.subscription_id!==null||!['web','api'].includes(transaction.origin)||!Array.isArray(transaction.items)||transaction.items.length!==1)return deny('transaction_not_eligible');
  const item=transaction.items[0];
  if(item.quantity!==1||item.price?.id!==claim.priceId||item.price?.product_id!==productId||item.price?.billing_cycle!==null)return deny('price_not_eligible');
  if(!Array.isArray(transaction.payments))return deny('payment_not_captured');
  const times=transaction.payments.filter(p=>p?.status==='captured').map(p=>Date.parse(p.captured_at)).filter(Number.isFinite);
  if(!times.length)return deny('payment_not_captured');
  const start=Math.max(...times),end=start+oneTimeDays[claim.priceId]*86400000;
  if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||now<start||now>=end)return deny('outside_paid_period');
  for(const a of adjustments){
    if(!a||a.transaction_id!==transaction.id||!['pending_approval','approved','rejected','reversed'].includes(a.status)||!['refund','credit','chargeback','chargeback_reverse','chargeback_warning','chargeback_warning_reverse','credit_reverse'].includes(a.action))return deny('invalid_adjustment');
    if(a.status==='approved'&&['refund','credit','chargeback'].includes(a.action))return deny('adjustment_requires_review');
  }
  return{allowed:true,reason:'active',expiresAt:new Date(end).toISOString()};
}
module.exports={evaluateOneTime};
