import {Client,TablesDB,Query} from 'node-appwrite';
import authModule from '../appwrite-auth.cjs';
import mappingModule from '../appwrite-mapping-store.cjs';
import paddleModule from '../paddle-client.cjs';
import entitlementModule from '../entitlement-service.cjs';
import catalogModule from '../catalog-config.cjs';
import reviewModule from '../refund-review-store.cjs';
// Staged only. This endpoint reports subscription state; it does NOT protect
// the still-public questions table. Do not enable before complete migration.
export default async ({req,res}) => {
  if(process.env.PAYMENT_ACCESS_ENABLED!=='true')return res.json({error:'Not enabled'},503);
  if(req.method!=='GET')return res.json({error:'Method not allowed'},405);
  let authenticate,check;
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT, projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID;
    authenticate=authModule.createAppwriteAuthenticator({endpoint,projectId});
    const mappings=mappingModule.createMappingStore({endpoint,projectId,databaseId:process.env.PAYMENT_EVENT_DATABASE,collectionId:process.env.PAYMENT_MAPPING_COLLECTION,apiKey:process.env.PAYMENT_EVENT_API_KEY});
    const environment=process.env.PADDLE_ENVIRONMENT,paddle=paddleModule.createPaddleClient({environment,apiKey:process.env.PADDLE_API_KEY});
    const encoded=process.env.CHECKOUT_BINDING_KEY_BASE64;if(typeof encoded!=='string'||!/^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(encoded))throw Error('Invalid key');
    const bindingKey=Buffer.from(encoded,'base64');if(bindingKey.length<32||bindingKey.toString('base64')!==encoded)throw Error('Invalid key');
    const reviewTables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(process.env.PAYMENT_EVENT_API_KEY));
    const reviews=reviewModule.createRefundReviewStore({tables:reviewTables,query:Query,databaseId:process.env.PAYMENT_EVENT_DATABASE,tableId:process.env.REFUND_REVIEW_TABLE});
    const {allowedRecurringPriceIds,oneTimeDays,productId}=catalogModule.catalogConfig(process.env);
    check=entitlementModule.createEntitlementService({mappings,paddle,bindingKey,environment,allowedRecurringPriceIds,oneTimeDays,productId,reviews});
  }catch(_){return res.json({error:'Not configured'},503);}
  const account=await authenticate(req.headers?.['x-appwrite-user-jwt']);
  if(account.status!==200)return res.json({error:account.status===401?'Sign in required':'Authentication unavailable'},account.status);
  const result=await check(account.userId);
  if(result.status!==200)return res.json(result.body,result.status);
  const {subscribed,expiresAt,reviewPending}=result.body;return res.json({subscribed,reviewPending,...(expiresAt?{expiresAt}:{})},200);
};
