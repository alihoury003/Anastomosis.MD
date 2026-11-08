import {Client,TablesDB} from 'node-appwrite';
import paddleModule from '../paddle-client.cjs';
import archiveModule from '../appwrite-event-store.cjs';
import checkpointModule from '../appwrite-checkpoint-store.cjs';
import reconcileModule from '../reconcile-events.cjs';
// Staged only. Configure execute access to NO client role, run on a schedule,
// and do not enable until backfill, schema, monitoring and sandbox tests pass.
export default async ({req,res,log,error})=>{
  if(req.headers?.['x-appwrite-trigger']!=='schedule'||process.env.PAYMENT_RECONCILER_ENABLED!=='true')return res.text('Not enabled',503);
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,databaseId=process.env.PAYMENT_EVENT_DATABASE,apiKey=process.env.PAYMENT_EVENT_API_KEY,environment=process.env.PADDLE_ENVIRONMENT;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!apiKey||!['sandbox','live'].includes(environment))throw Error('Not configured');
    const tables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey));
    const paddle=paddleModule.createPaddleClient({environment,apiKey:process.env.PADDLE_API_KEY});
    const archive=archiveModule.createEventArchive({endpoint,projectId,databaseId,collectionId:process.env.PAYMENT_EVENT_COLLECTION,apiKey});
    const checkpoints=checkpointModule.createCheckpointStore({tables,databaseId,tableId:process.env.PAYMENT_CHECKPOINT_TABLE,rowId:`paddle-${environment}`});
    const result=await reconcileModule.reconcileEvents({paddle,archive,checkpoints,initialBackfillApproved:process.env.PAYMENT_RECONCILE_BASELINE_APPROVED==='true',maxPages:1,pageSize:10});
    // No event IDs, payloads, customer information, credentials or links in logs.
    if(['caught_up','more','concurrent'].includes(result.status)){log?.(`Payment event reconciliation: ${result.status}; ${result.archived} events processed.`);return res.text(result.status,200);}
    error?.(`Payment event reconciliation requires attention: ${result.status}.`);return res.text('Attention required',503);
  }catch(_){error?.('Payment event reconciliation failed; retry and review required.');return res.text('Retry required',503);}
};
