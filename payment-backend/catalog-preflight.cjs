'use strict';
const {catalogConfig}=require('./catalog-config.cjs');const {isValidPrice}=require('./price-policy.cjs');
const SPECS={monthly:{code:'ANASTOMOSIS10',amount:'10'},threeMonth:{code:'ANASTOMOSIS20',amount:'20'},annual:{code:'ANASTOMOSIS35',amount:'35'}};
const DISC=/^dsc_[a-z0-9]{26}$/;
// Read-only catalog audit; it does not certify checkout, entitlements or launch.
async function checkCatalog({env,paddle,discountIds,now=Date.now()}){
  if(!paddle||typeof paddle.getPrice!=='function'||typeof paddle.getDiscount!=='function'||!discountIds||typeof discountIds!=='object'||!Number.isFinite(now))throw Error('Catalog check not configured');
  let config;try{config=catalogConfig(env);}catch(_){return{catalogReady:false,plans:[],error:'catalog_configuration_incomplete'};}
  const plans=[];
  for(const [plan,spec] of Object.entries(SPECS)){
    const prices=config.priceIds[plan],row={plan,oneTime:false,recurring:false,discount:null,warnings:[]};
    for(const mode of ['oneTime','recurring']){
      try{const price=await paddle.getPrice(prices[mode]);row[mode]=price?.id===prices[mode]&&isValidPrice({price,plan,autoRenew:mode==='recurring',productId:config.productId});}catch(_){row.warnings.push(`${mode}_lookup_failed`);}
    }
    if(!DISC.test(discountIds[plan]||'')){row.warnings.push('discount_id_missing');plans.push(row);continue;}
    try{
      const discount=await paddle.getDiscount(discountIds[plan]);
      if(discount?.id!==discountIds[plan]||typeof discount.code!=='string'||!['active','archived'].includes(discount.status)||!['percentage','flat','flat_per_seat'].includes(discount.type)||typeof discount.enabled_for_checkout!=='boolean'||typeof discount.recur!=='boolean'||!Number.isSafeInteger(discount.times_used)||discount.times_used<0||(discount.usage_limit!==null&&(!Number.isSafeInteger(discount.usage_limit)||discount.usage_limit<1))||(discount.restrict_to!==null&&!Array.isArray(discount.restrict_to))||(discount.expires_at!==null&&(typeof discount.expires_at!=='string'||!Number.isFinite(Date.parse(discount.expires_at)))))throw Error('Invalid discount');
      const current=discount.status==='active'&&discount.enabled_for_checkout&&discount.code.toUpperCase()===spec.code&&discount.type==='percentage'&&Number(discount.amount)===Number(spec.amount)&&discount.recur===false;
      const exhausted=discount.usage_limit!==null&&discount.times_used>=discount.usage_limit,expired=discount.expires_at!==null&&Date.parse(discount.expires_at)<=now;
      const applicable=id=>discount.restrict_to===null||discount.restrict_to.includes(config.productId)||discount.restrict_to.includes(id);
      const otherIds=Object.entries(config.priceIds).filter(([name])=>name!==plan).flatMap(([,v])=>[v.oneTime,v.recurring]);
      row.discount={configurationMatches:current,exhausted,expired,oneTime:applicable(prices.oneTime),recurring:applicable(prices.recurring),alsoAppliesToOtherPlans:otherIds.some(applicable)};
    }catch(_){row.warnings.push('discount_lookup_or_validation_failed');}
    plans.push(row);
  }
  const catalogReady=plans.every(p=>p.oneTime&&p.recurring);
  return{catalogReady,plans};
}
module.exports={checkCatalog};
