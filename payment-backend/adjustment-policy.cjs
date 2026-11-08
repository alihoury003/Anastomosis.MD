'use strict';
const ADJ=/^adj_[a-z0-9]{26}$/;
const BILL=/^(?:sub|txn)_[a-z0-9]{26}$/;
const ACTIONS=new Set(['refund','credit','chargeback','chargeback_reverse','chargeback_warning','chargeback_warning_reverse','credit_reverse']);
const STATUSES=new Set(['pending_approval','approved','rejected','reversed']);
// Compare RFC3339 timestamps including sub-millisecond precision, avoiding
// stale decisions when Paddle sends multiple updates within one millisecond.
function timestamp(value){
  if(typeof value!=='string')return null;
  const m=value.match(/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})$/);if(!m)return null;
  const ms=Date.parse(m[1]+m[3]);if(!Number.isFinite(ms))return null;
  return BigInt(ms)*1000000n+BigInt((m[2]||'').padEnd(9,'0'));
}
function classifyAdjustment(adjustment,billingId){
  if(!adjustment||!ADJ.test(adjustment.id||'')||!BILL.test(billingId||'')||!ACTIONS.has(adjustment.action)||!STATUSES.has(adjustment.status)||timestamp(adjustment.updated_at)===null)return{valid:false};
  const property=billingId.startsWith('sub_')?'subscription_id':'transaction_id';if(adjustment[property]!==billingId)return{valid:false};
  if(adjustment.status!=='approved'||!['refund','credit','chargeback'].includes(adjustment.action))return{valid:true,needsReview:false,defaultRestriction:false};
  if(!['full','partial'].includes(adjustment.type)&&!(adjustment.action==='chargeback'&&adjustment.type===null))return{valid:false};
  // Partial refunds/credits do not automatically remove access while awaiting
  // review. Full refunds/credits and any chargeback are restricted by default.
  return{valid:true,needsReview:true,defaultRestriction:adjustment.action==='chargeback'||adjustment.type==='full'};
}
module.exports={timestamp,classifyAdjustment};
