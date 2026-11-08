import {summarizeLegacyHistory} from './legacy-history.mjs';
// Staged orchestration only. The live dashboard does not import this module.
// No DOM manipulation or exam-screen styling lives here. Legacy prefs are for
// display only; they never authorize question access or paid subscriptions.
export function createDashboardController({gateway,bridge,checkoutUI,wait=ms=>new Promise(resolve=>setTimeout(resolve,ms))}) {
  if(!gateway||!['questionStatus','startTrial','paidAccess'].every(k=>typeof gateway[k]==='function')||!bridge||!['loadCatalog','loadBlock','loadReview'].every(k=>typeof bridge[k]==='function')||!checkoutUI||typeof checkoutUI.open!=='function'||typeof wait!=='function')throw Error('Dashboard is not configured');
  async function boot(legacyTests){
    const [status,catalog]=await Promise.all([gateway.questionStatus(),bridge.loadCatalog()]);
    let history;try{history=summarizeLegacyHistory(legacyTests||[]);}catch(_){history={records:[],skipped:0,authorizationGranted:false,unavailable:true};}
    return{status,catalog,legacyHistory:history};
  }
  async function beginBlock(ids){
    const block=await bridge.loadBlock(ids);
    // If the quota was reserved successfully, don't throw away the returned
    // questions just because a subsequent status refresh is unavailable.
    let status=null;try{status=await gateway.questionStatus();}catch(_){}
    return{...block,status};
  }
  async function review(ids){
    try{return{...(await bridge.loadReview(ids)),migrationRequired:false};}
    catch(err){if(err?.status===403)return{questions:[],limited:true,migrationRequired:true};throw err;}
  }
  async function startTrial(){const result=await gateway.startTrial();let status=null;try{status=await gateway.questionStatus();}catch(_){}return{result,status};}
  async function checkout(plan,options){return checkoutUI.open(plan,options);}
  async function verifyAfterCheckout({attempts=5,delayMs=3000}={}){
    if(!Number.isInteger(attempts)||attempts<1||attempts>10||!Number.isInteger(delayMs)||delayMs<0||delayMs>30000)throw Error('Invalid polling settings');
    for(let i=0;i<attempts;i++){
      try{const result=await gateway.paidAccess();if(result.subscribed===true)return{status:'active',expiresAt:result.expiresAt||null};}catch(_){}
      if(i+1<attempts)await wait(delayMs);
    }
    // Browser checkout completion is not payment confirmation; never grant here.
    return{status:'pending'};
  }
  return{boot,beginBlock,review,startTrial,checkout,verifyAfterCheckout};
}
