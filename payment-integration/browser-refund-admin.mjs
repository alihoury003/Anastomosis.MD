// Staged, server-authorized refund review client; never holds server secrets.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/,ADJ=/^adj_[a-z0-9]{26}$/;
export class RefundReviewError extends Error{constructor(status){super('Unable to complete the review. Please refresh or contact support.');this.name='RefundReviewError';this.status=status;}}
export function createRefundAdminClient({account,functions,functionId}){
  if(!account||typeof account.createJWT!=='function'||!functions||typeof functions.createExecution!=='function'||typeof functionId!=='string'||!ID.test(functionId))throw Error('Review client not configured');
  async function call(path,method,body){
    let execution;try{const token=await account.createJWT();if(typeof token?.jwt!=='string'||token.jwt.length<20)throw Error('No session');execution=await functions.createExecution(functionId,body===undefined?'':JSON.stringify(body),false,path,method,{'content-type':'application/json','x-appwrite-user-jwt':token.jwt});}catch(_){throw new RefundReviewError(503);}
    if(execution?.status!=='completed'||!Number.isInteger(execution.responseStatusCode)||typeof execution.responseBody!=='string')throw new RefundReviewError(503);
    let value;try{value=JSON.parse(execution.responseBody);}catch(_){throw new RefundReviewError(503);}
    if(execution.responseStatusCode<200||execution.responseStatusCode>=300)throw new RefundReviewError(execution.responseStatusCode);
    if(!value||typeof value!=='object'||Array.isArray(value))throw new RefundReviewError(503);return value;
  }
  async function list(){const value=await call('/reviews','GET');if(!Array.isArray(value.reviews)||value.reviews.length>25)throw new RefundReviewError(503);return value.reviews.map(x=>{if(!x||!ADJ.test(x.adjustmentId||'')||typeof x.updatedAt!=='string'||!Number.isFinite(Date.parse(x.updatedAt)))throw new RefundReviewError(503);return{adjustmentId:x.adjustmentId,updatedAt:x.updatedAt,userId:String(x.userId||''),billingId:String(x.billingId||''),action:String(x.action||''),adjustmentType:String(x.adjustmentType||''),paddleStatus:String(x.paddleStatus||'')};});}
  async function decide({adjustmentId,expectedUpdatedAt,decision}){if(!ADJ.test(adjustmentId||'')||typeof expectedUpdatedAt!=='string'||!Number.isFinite(Date.parse(expectedUpdatedAt))||!['allow','restrict'].includes(decision))throw new RefundReviewError(400);const value=await call('/decision','POST',{adjustmentId,expectedUpdatedAt,decision});if(!['decided','unchanged'].includes(value.status))throw new RefundReviewError(503);return value;}
  return{list,decide};
}
