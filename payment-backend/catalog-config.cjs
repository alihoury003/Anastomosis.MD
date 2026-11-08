'use strict';
const PRICE=/^pri_[a-z0-9]{26}$/,PRODUCT=/^pro_[a-z0-9]{26}$/;
// One-time and recurring IDs must be distinct. Creating prices in Paddle is a
// separate, deliberate catalog action; this module never modifies the catalog.
function catalogConfig(env){
  const productId=env.PADDLE_PRODUCT_ID;
  const priceIds={monthly:{oneTime:env.PADDLE_ONE_TIME_MONTHLY_PRICE,recurring:env.PADDLE_MONTHLY_PRICE},threeMonth:{oneTime:env.PADDLE_ONE_TIME_THREE_MONTH_PRICE,recurring:env.PADDLE_THREE_MONTH_PRICE},annual:{oneTime:env.PADDLE_ONE_TIME_ANNUAL_PRICE,recurring:env.PADDLE_ANNUAL_PRICE}};
  const all=Object.values(priceIds).flatMap(p=>[p.oneTime,p.recurring]);
  if(!PRODUCT.test(productId||'')||!all.every(p=>PRICE.test(p||''))||new Set(all).size!==6)throw Error('Invalid catalog configuration');
  return{productId,priceIds,allowedRecurringPriceIds:[priceIds.monthly.recurring,priceIds.threeMonth.recurring,priceIds.annual.recurring],oneTimeDays:{[priceIds.monthly.oneTime]:30,[priceIds.threeMonth.oneTime]:90,[priceIds.annual.oneTime]:365}};
}
module.exports={catalogConfig};
