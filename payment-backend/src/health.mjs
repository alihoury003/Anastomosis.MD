import {Client,TablesDB} from 'node-appwrite';
import queueModule from '../appwrite-queue-store.cjs';
import checkpointModule from '../appwrite-checkpoint-store.cjs';
import healthModule from '../payment-health.cjs';
// Scheduled operator-only summary; logs are not an alerting system. Never
// expose this function to client execute roles or enable before review.
export default async({req,res,log,error})=>{
  if(req.headers?.['x-appwrite-trigger']!=='schedule'||process.env.PAYMENT_HEALTH_ENABLED!=='true')return res.text('Not enabled',503);
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,databaseId=process.env.PAYMENT_EVENT_DATABASE,apiKey=process.env.PAYMENT_EVENT_API_KEY,environment=process.env.PADDLE_ENVIRONMENT;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!apiKey||!['sandbox','live'].includes(environment))throw Error('Not configured');
    const tables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey));
    const queue=queueModule.createQueueStore({endpoint,projectId,databaseId,collectionId:process.env.PAYMENT_EVENT_COLLECTION,apiKey});
    const checkpoints=checkpointModule.createCheckpointStore({tables,databaseId,tableId:process.env.PAYMENT_CHECKPOINT_TABLE,rowId:`paddle-${environment}`});
    const result=await healthModule.createPaymentHealth({queue,checkpoints})();
    if(!result.ok){error?.(`Payment health needs attention: ${result.reasons.join(', ')}.`);return res.text('Attention required',503);}
    log?.(`Payment health: ${result.pending} pending, ${result.manualReview} review items.`);return res.text('Healthy',200);
  }catch(_){error?.('Payment health check failed.');return res.text('Attention required',503);}
};
