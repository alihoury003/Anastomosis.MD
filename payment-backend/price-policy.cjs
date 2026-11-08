'use strict';
const PRICE=/^pri_[a-z0-9]{26}$/;
const PRODUCT=/^pro_[a-z0-9]{26}$/;
const PLANS=Object.freeze({monthly:{amount:'1500',interval:'month',frequency:1,days:30},threeMonth:{amount:'3600',interval:'month',frequency:3,days:90},annual:{amount:'9900',interval:'year',frequency:1,days:365}});
// Price information must come from Paddle's authenticated API, not the client.
function isValidPrice({price,plan,autoRenew,productId}) {
  const spec=PLANS[plan];
  if(!spec||typeof autoRenew!=='boolean'||!PRODUCT.test(productId||'')||!price||!PRICE.test(price.id||'')||price.product_id!==productId||price.status!=='active'||price.unit_price?.currency_code!=='USD'||price.unit_price?.amount!==spec.amount||price.trial_period!==null)return false;
  if(!autoRenew)return price.billing_cycle===null;
  return !!price.billing_cycle&&price.billing_cycle.interval===spec.interval&&price.billing_cycle.frequency===spec.frequency;
}
module.exports={isValidPrice,PLANS};
