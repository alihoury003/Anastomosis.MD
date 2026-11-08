import authModule from '../appwrite-auth.cjs';
import paddleModule from '../paddle-client.cjs';
import preflightModule from '../catalog-preflight.cjs';
// Read-only, admin-only, disabled by default. It checks catalog configuration;
// it does not certify billing, question access, deployment or launch readiness.
export default async({req,res})=>{
  const finish=(body,status)=>res.json(body,status,{'cache-control':'no-store'});
  if(process.env.CATALOG_PREFLIGHT_ENABLED!=='true')return finish({error:'Not enabled'},503);
  if(req.method!=='GET')return finish({error:'Method not allowed'},405);
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,admin=process.env.REFUND_ADMIN_USER_ID;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!admin||!/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/.test(admin))throw Error('Not configured');
    const auth=authModule.createAppwriteAuthenticator({endpoint,projectId}),actor=await auth(req.headers?.['x-appwrite-user-jwt']);
    if(actor.status!==200)return finish({error:actor.status===401?'Sign in required':'Authentication unavailable'},actor.status);
    if(actor.userId!==admin)return finish({error:'Forbidden'},403);
    const paddle=paddleModule.createPaddleClient({environment:process.env.PADDLE_ENVIRONMENT,apiKey:process.env.PADDLE_API_KEY});
    const discountIds={monthly:process.env.PADDLE_MONTHLY_DISCOUNT,threeMonth:process.env.PADDLE_THREE_MONTH_DISCOUNT,annual:process.env.PADDLE_ANNUAL_DISCOUNT};
    const report=await preflightModule.checkCatalog({env:process.env,paddle,discountIds});return finish(report,200);
  }catch(_){return finish({error:'Catalog check unavailable'},503);}
};
