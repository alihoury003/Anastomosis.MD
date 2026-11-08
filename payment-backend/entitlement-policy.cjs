'use strict';
const { verifyBinding } = require('./checkout-binding.cjs');
const SUB_ID = /^sub_[a-z0-9]{26}$/;
const PRICE_ID = /^pri_[a-z0-9]{26}$/;

// A pure, conservative policy. Inputs must be current authoritative Paddle API
// responses, NOT frontend data or an untrusted webhook body. The caller must
// fetch every adjustment page and authenticate the requesting user separately.
// No value returned by this function is written to Appwrite or grants access.
function evaluateSubscription({subscription, adjustments, adjustmentsComplete, authenticatedUserId, bindingKey, environment, allowedPriceIds, now = Date.now()}) {
  const deny = reason => ({ allowed:false, reason });
  if (!subscription || typeof subscription !== 'object' || !SUB_ID.test(subscription.id || '') ||
      typeof authenticatedUserId !== 'string' || !Array.isArray(allowedPriceIds) ||
      adjustmentsComplete !== true || !Array.isArray(adjustments) || !Number.isFinite(now)) return deny('invalid_or_incomplete_data');
  const claim = verifyBinding(subscription.custom_data?.anastomosis_binding, bindingKey, environment);
  if (!claim || claim.autoRenew !== true || claim.userId !== authenticatedUserId || !PRICE_ID.test(claim.priceId) || !allowedPriceIds.includes(claim.priceId)) return deny('unverified_account_binding');
  if (!Array.isArray(subscription.items) || !subscription.items.some(item => item?.price?.id === claim.priceId && item.status === 'active')) return deny('price_not_active');
  const firstBilled = Date.parse(subscription.first_billed_at);
  if (subscription.status !== 'active' || !Number.isFinite(firstBilled) || firstBilled > now) return deny('subscription_not_active');
  const start = Date.parse(subscription.current_billing_period?.starts_at), end = Date.parse(subscription.current_billing_period?.ends_at);
  if (!Number.isFinite(start) || !Number.isFinite(end) || start >= end || now < start || now >= end) return deny('outside_paid_period');
  const change = subscription.scheduled_change;
  if (change && (!['cancel','pause','resume'].includes(change.action) || !Number.isFinite(Date.parse(change.effective_at)))) return deny('invalid_scheduled_change');
  if (change && ['cancel','pause'].includes(change.action) && now >= Date.parse(change.effective_at)) return deny('scheduled_change_effective');
  // Conservative policy: any approved refund/credit/chargeback goes to manual
  // review. This may restrict legitimate access after a partial/old adjustment.
  for (const a of adjustments) {
    if (!a || a.subscription_id !== subscription.id || !['pending_approval','approved','rejected','reversed'].includes(a.status) || !['refund','credit','chargeback','chargeback_reverse','chargeback_warning','chargeback_warning_reverse','credit_reverse'].includes(a.action)) return deny('invalid_adjustment');
    if (a.status === 'approved' && ['refund','credit','chargeback'].includes(a.action)) return deny('adjustment_requires_review');
  }
  const stopAt = change && ['cancel','pause'].includes(change.action) ? Math.min(end, Date.parse(change.effective_at)) : end;
  return {allowed:true, reason:'active', expiresAt:new Date(stopAt).toISOString()};
}
module.exports = { evaluateSubscription };
