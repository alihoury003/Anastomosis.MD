// Browser-side bridge for Appwrite Web SDK v16. Staged, not imported by the
// live dashboard. No API key or Paddle webhook secret belongs in this file.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const PRICE=/^pri_[a-z0-9]{26}$/;
export class GatewayError extends Error {
  constructor(status,message='Unable to complete the request. Please try again.') {super(message);this.name='GatewayError';this.status=status;}
}
export function createGateway({account,functions,questionFunctionId,checkoutFunctionId,accessFunctionId,priceIds}) {
  if(!account||typeof account.createJWT!=='function'||!functions||typeof functions.createExecution!=='function'||
    ![questionFunctionId,checkoutFunctionId,accessFunctionId].every(x=>typeof x==='string'&&ID.test(x))||
    !priceIds||!['monthly','threeMonth','annual'].every(k=>priceIds[k]&&['oneTime','recurring'].every(mode=>typeof priceIds[k][mode]==='string'&&PRICE.test(priceIds[k][mode]))))throw Error('Gateway is not configured');
  if(new Set(['monthly','threeMonth','annual'].flatMap(k=>[priceIds[k].oneTime,priceIds[k].recurring])).size!==6)throw Error('Gateway is not configured');
  function validUsage(u){return !!u&&Number.isInteger(u.freeRemaining)&&u.freeRemaining>=0&&u.freeRemaining<=40&&typeof u.firstFreeDay==='boolean'&&typeof u.legacyMigrationComplete==='boolean'&&typeof u.trialStarted==='boolean'&&typeof u.trialActive==='boolean'&&Number.isInteger(u.trialUsed)&&u.trialUsed>=0&&u.trialUsed<=150&&(u.trialEndsAt===null||Number.isSafeInteger(u.trialEndsAt));}
  async function call(functionId,path,method,body){
    let token,execution;
    try{token=await account.createJWT();if(typeof token?.jwt!=='string'||token.jwt.length<20)throw Error('No session');
      execution=await functions.createExecution(functionId,body===undefined?'':JSON.stringify(body),false,path,method,{'content-type':'application/json','x-appwrite-user-jwt':token.jwt});
    }catch(_){throw new GatewayError(503);}
    if(execution?.status!=='completed'||!Number.isInteger(execution.responseStatusCode)||typeof execution.responseBody!=='string')throw new GatewayError(503);
    let value;try{value=JSON.parse(execution.responseBody);}catch(_){throw new GatewayError(503);}
    if(execution.responseStatusCode<200||execution.responseStatusCode>=300)throw new GatewayError(execution.responseStatusCode);
    if(!value||typeof value!=='object'||Array.isArray(value))throw new GatewayError(503);
    return value;
  }
  async function catalog(){
    const body=await call(questionFunctionId,'/catalog','GET');
    if(!Array.isArray(body.questions)||body.questions.length>10000)throw new GatewayError(503);
    const seen=new Set();return body.questions.map(q=>{if(!q||!ID.test(q.id||'')||seen.has(q.id))throw new GatewayError(503);seen.add(q.id);return{id:q.id,subject:typeof q.subject==='string'?q.subject:'',system:typeof q.system==='string'?q.system:'',topic:typeof q.topic==='string'?q.topic:'',difficulty:Number.isFinite(q.difficulty)?q.difficulty:null};});
  }
  async function fetchQuestions(ids,path){
    if(!Array.isArray(ids)||ids.length<1||ids.length>20||ids.some(id=>typeof id!=='string'||!ID.test(id))||new Set(ids).size!==ids.length)throw new GatewayError(400);
    const body=await call(questionFunctionId,path,'POST',{questionIds:ids});
    if(!Array.isArray(body.results)||typeof body.exhausted!=='boolean'||body.results.length>ids.length||('billingUnavailable' in body&&typeof body.billingUnavailable!=='boolean')||('usage' in body&&!validUsage(body.usage)))throw new GatewayError(503);
    const seen=new Set();for(const result of body.results){const id=result?.question?.$id;if(!ids.includes(id)||seen.has(id)||!['paid','trial','free','review'].includes(result.source))throw new GatewayError(503);seen.add(id);}
    return body;
  }
  async function questions(ids){return fetchQuestions(ids,'/questions');}
  async function review(ids){return fetchQuestions(ids,'/review');}
  async function questionStatus(){const body=await call(questionFunctionId,'/status','GET');if(typeof body.subscribed!=='boolean'||typeof body.reviewPending!=='boolean'||typeof body.billingUnavailable!=='boolean'||typeof body.migrationRequired!=='boolean'||!validUsage(body.usage))throw new GatewayError(503);return body;}
  async function startTrial(){const body=await call(questionFunctionId,'/trial','POST',{});if(!validUsage(body.usage))throw new GatewayError(503);return body;}
  async function paidAccess(){const body=await call(accessFunctionId,'/','GET');if(typeof body.subscribed!=='boolean')throw new GatewayError(503);return body;}
  async function checkout(plan,autoRenew){
    if(!['monthly','threeMonth','annual'].includes(plan)||typeof autoRenew!=='boolean')throw new GatewayError(400);
    const body=await call(checkoutFunctionId,'/','POST',{plan,autoRenew});
    if(body.priceId!==priceIds[plan][autoRenew?'recurring':'oneTime']||typeof body.customData?.anastomosis_binding!=='string'||body.customData.anastomosis_binding.length>1024)throw new GatewayError(503);
    return {priceId:body.priceId,customData:{anastomosis_binding:body.customData.anastomosis_binding}};
  }
  return {catalog,questions,review,questionStatus,startTrial,paidAccess,checkout};
}
