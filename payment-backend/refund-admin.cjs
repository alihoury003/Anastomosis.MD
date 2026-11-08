'use strict';
const {timestamp,classifyAdjustment}=require('./adjustment-policy.cjs');
const USER=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/,ADJ=/^adj_[a-z0-9]{26}$/;
// Operator decisions change only our private access policy, never Paddle funds.
// authenticate MUST verify the JWT server-side; never accept a client user ID.
function createRefundAdmin({authenticate,adminUserId,reviews,paddle,clock=()=>Date.now()}){
  if(typeof authenticate!=='function'||!USER.test(adminUserId||'')||!reviews||!['listPending','getForAdmin','decide'].every(k=>typeof reviews[k]==='function')||!paddle||typeof paddle.getAdjustment!=='function'||typeof clock!=='function')throw Error('Refund admin not configured');
  return async function route(req){
    const actor=await authenticate(req.headers?.['x-appwrite-user-jwt']);
    if(actor.status!==200)return{status:actor.status===401?401:503,body:{error:actor.status===401?'Sign in required':'Authentication unavailable'}};
    if(actor.userId!==adminUserId)return{status:403,body:{error:'Forbidden'}};
    if(req.method==='GET'&&req.path==='/reviews'){
      try{return{status:200,body:{reviews:await reviews.listPending(25)}};}catch(_){return{status:503,body:{error:'Review service unavailable'}};}
    }
    if(req.method==='POST'&&req.path==='/decision'){
      let input;try{if(typeof req.bodyText!=='string'||Buffer.byteLength(req.bodyText,'utf8')>2048)throw Error('Invalid');input=JSON.parse(req.bodyText);if(!input||typeof input!=='object'||Array.isArray(input)||!ADJ.test(input.adjustmentId||'')||timestamp(input.expectedUpdatedAt)===null||!['allow','restrict'].includes(input.decision))throw Error('Invalid');}catch(_){return{status:400,body:{error:'Invalid request'}};}
      try{
        const record=await reviews.getForAdmin(input.adjustmentId);if(!record)return{status:404,body:{error:'Review not found'}};
        const current=await paddle.getAdjustment(input.adjustmentId),classification=classifyAdjustment(current,record.billingId);
        if(!classification.valid||!classification.needsReview||timestamp(current.updated_at)!==timestamp(input.expectedUpdatedAt)||timestamp(record.updatedAt)!==timestamp(input.expectedUpdatedAt)||current.action!==record.action||(current.type??'')!==record.adjustmentType||current.status!==record.paddleStatus)return{status:409,body:{error:'Adjustment changed; refresh the review'}};
        const result=await reviews.decide({adjustmentId:input.adjustmentId,expectedUpdatedAt:input.expectedUpdatedAt,decision:input.decision,adminUserId:actor.userId,now:clock()});
        if(['stale','already_decided'].includes(result))return{status:409,body:{error:'Review changed; refresh the review'}};
        if(!['decided','unchanged'].includes(result))throw Error('Unexpected decision');
        return{status:200,body:{status:result}};
      }catch(_){return{status:503,body:{error:'Review service unavailable'}};}
    }
    return{status:404,body:{error:'Not found'}};
  };
}
module.exports={createRefundAdmin};
