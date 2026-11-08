// Staged admin-only, read-only catalog check. No server credentials in browser.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
export function createCatalogPreflightClient({account,functions,functionId}){
  if(!account||typeof account.createJWT!=='function'||!functions||typeof functions.createExecution!=='function'||typeof functionId!=='string'||!ID.test(functionId))throw Error('Catalog check not configured');
  return async function check(){
    let execution;try{const token=await account.createJWT();if(typeof token?.jwt!=='string'||token.jwt.length<20)throw Error('No session');execution=await functions.createExecution(functionId,'',false,'/','GET',{'x-appwrite-user-jwt':token.jwt});}catch(_){throw Error('Catalog check unavailable');}
    if(execution?.status!=='completed'||execution.responseStatusCode!==200||typeof execution.responseBody!=='string')throw Error('Catalog check unavailable');
    let report;try{report=JSON.parse(execution.responseBody);}catch(_){throw Error('Catalog check unavailable');}
    if(!report||typeof report.catalogReady!=='boolean'||!Array.isArray(report.plans)||report.plans.length>3)throw Error('Catalog check unavailable');
    const plans=report.plans.map(p=>{if(!p||!['monthly','threeMonth','annual'].includes(p.plan)||typeof p.oneTime!=='boolean'||typeof p.recurring!=='boolean')throw Error('Catalog check unavailable');const d=p.discount;return{plan:p.plan,oneTime:p.oneTime,recurring:p.recurring,discount:d&&typeof d==='object'?{configurationMatches:d.configurationMatches===true,oneTime:d.oneTime===true,recurring:d.recurring===true,exhausted:d.exhausted===true,expired:d.expired===true,alsoAppliesToOtherPlans:d.alsoAppliesToOtherPlans===true}:null};});
    if(new Set(plans.map(p=>p.plan)).size!==plans.length||(report.catalogReady&&(plans.length!==3||plans.some(p=>!p.oneTime||!p.recurring))))throw Error('Catalog check unavailable');
    return{catalogReady:report.catalogReady,plans};
  };
}
