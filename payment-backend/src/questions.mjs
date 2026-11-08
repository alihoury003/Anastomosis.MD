import {Client,TablesDB,Query} from 'node-appwrite';
import authModule from '../appwrite-auth.cjs';
import questionModule from '../appwrite-questions.cjs';
import usageModule from '../appwrite-usage-store.cjs';
import accessModule from '../question-access.cjs';
import routesModule from '../question-routes.cjs';
import mappingModule from '../appwrite-mapping-store.cjs';
import paddleModule from '../paddle-client.cjs';
import entitlementModule from '../entitlement-service.cjs';
// Staged only. Never enable or remove public read before a tested migration,
// including importer access, existing user data and full dashboard integration.
export default async ({req,res})=>{
  const finish=(body,status)=>res.json(body,status,{'cache-control':'no-store'});
  if(process.env.QUESTION_ACCESS_ENABLED!=='true')return finish({error:'Not enabled'},503);
  let route;
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,apiKey=process.env.QUESTION_API_KEY;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||typeof apiKey!=='string'||!apiKey)throw Error('Bad configuration');
    const tables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey));
    const questions=questionModule.createQuestionRepository({tables,query:Query,databaseId:process.env.QUESTION_DATABASE,tableId:process.env.QUESTION_TABLE});
    const usage=usageModule.createUsageStore({tables,databaseId:process.env.USAGE_DATABASE,tableId:process.env.USAGE_TABLE});
    const mappings=mappingModule.createMappingStore({endpoint,projectId,databaseId:process.env.PAYMENT_EVENT_DATABASE,collectionId:process.env.PAYMENT_MAPPING_COLLECTION,apiKey:process.env.PAYMENT_EVENT_API_KEY});
    const environment=process.env.PADDLE_ENVIRONMENT,paddle=paddleModule.createPaddleClient({environment,apiKey:process.env.PADDLE_API_KEY});
    const encoded=process.env.CHECKOUT_BINDING_KEY_BASE64;if(typeof encoded!=='string'||!/^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(encoded))throw Error('Invalid key');
    const bindingKey=Buffer.from(encoded,'base64');if(bindingKey.length<32||bindingKey.toString('base64')!==encoded)throw Error('Invalid key');
    const allowedPriceIds=[process.env.PADDLE_MONTHLY_PRICE,process.env.PADDLE_THREE_MONTH_PRICE,process.env.PADDLE_ANNUAL_PRICE];if(!allowedPriceIds.every(id=>/^pri_[a-z0-9]{26}$/.test(id||'')))throw Error('Invalid prices');
    const lookup=entitlementModule.createEntitlementService({mappings,paddle,bindingKey,environment,allowedPriceIds});
    const adminId=process.env.QUESTION_ADMIN_USER_ID;
    if(adminId && !/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/.test(adminId))throw Error('Invalid admin');
    const entitlements={check:async userId=>adminId&&userId===adminId?{status:200,body:{subscribed:true}}:lookup(userId)};
    const access=accessModule.createQuestionAccess({questions,usage,entitlements});
    route=routesModule.createQuestionRoutes({authenticate:authModule.createAppwriteAuthenticator({endpoint,projectId}),access,questions});
  }catch(_){return finish({error:'Not configured'},503);}
  try{const result=await route(req);return finish(result.body,result.status);}catch(_){return finish({error:'Service unavailable'},503);}
};
