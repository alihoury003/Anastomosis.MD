import checkoutModule from '../checkout-session.cjs';
import paddleModule from '../paddle-client.cjs';
import catalogModule from '../catalog-config.cjs';
// Staged only: checkout cannot be enabled until the complete backend,
// no-default-renewal enforcement and question delivery are tested end-to-end.
export default async ({req,res}) => {
  if(process.env.CHECKOUT_SESSION_ENABLED!=='true') return res.json({error:'Not enabled'},503);
  if(req.method!=='POST') return res.json({error:'Method not allowed'},405);
  let input, service;
  try {
    if(typeof req.bodyText!=='string'||Buffer.byteLength(req.bodyText,'utf8')>2048) throw Error('Bad request');
    input=JSON.parse(req.bodyText);
    if(!input || typeof input!=='object' || Array.isArray(input)) throw Error('Bad request');
  } catch (_) {return res.json({error:'Invalid request'},400);}
  try {
    const encoded=process.env.CHECKOUT_BINDING_KEY_BASE64;
    if(typeof encoded!=='string'||!/^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(encoded)) throw Error('Invalid binding key');
    const bindingKey=Buffer.from(encoded,'base64');if(bindingKey.length<32||bindingKey.toString('base64')!==encoded) throw Error('Invalid binding key');
    const environment=process.env.PADDLE_ENVIRONMENT;
    const paddle=paddleModule.createPaddleClient({environment,apiKey:process.env.PADDLE_API_KEY});
    const {productId,priceIds}=catalogModule.catalogConfig(process.env);
    service=checkoutModule.checkoutSessionService({
      endpoint:process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId:process.env.APPWRITE_FUNCTION_PROJECT_ID,
      environment,bindingKey,paddle,productId,priceIds
    });
  } catch (_) {return res.json({error:'Not configured'},503);}
  const result=await service({jwt:req.headers?.['x-appwrite-user-jwt'],plan:input.plan,autoRenew:input.autoRenew});
  return res.json(result.body,result.status);
};
