import {Client,TablesDB,Query} from 'node-appwrite';
import authModule from '../appwrite-auth.cjs';
import paddleModule from '../paddle-client.cjs';
import reviewModule from '../refund-review-store.cjs';
import adminModule from '../refund-admin.cjs';
// Staged only. Default disabled. Give execute access only to authenticated
// users; authorization is additionally checked against the exact admin user ID.
export default async({req,res})=>{
  const finish=(body,status)=>res.json(body,status,{'cache-control':'no-store'});
  if(process.env.REFUND_ADMIN_ENABLED!=='true')return finish({error:'Not enabled'},503);
  let route;try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,apiKey=process.env.PAYMENT_EVENT_API_KEY;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!apiKey)throw Error('Not configured');
    const authenticate=authModule.createAppwriteAuthenticator({endpoint,projectId});
    const tables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey));
    const reviews=reviewModule.createRefundReviewStore({tables,query:Query,databaseId:process.env.PAYMENT_EVENT_DATABASE,tableId:process.env.REFUND_REVIEW_TABLE});
    const paddle=paddleModule.createPaddleClient({environment:process.env.PADDLE_ENVIRONMENT,apiKey:process.env.PADDLE_API_KEY});
    route=adminModule.createRefundAdmin({authenticate,adminUserId:process.env.REFUND_ADMIN_USER_ID,reviews,paddle});
  }catch(_){return finish({error:'Not configured'},503);}
  try{const result=await route(req);return finish(result.body,result.status);}catch(_){return finish({error:'Review service unavailable'},503);}
};
