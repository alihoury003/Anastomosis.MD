import {Client,TablesDB,Query} from 'node-appwrite';
import queueModule from '../appwrite-queue-store.cjs';
import mappingModule from '../appwrite-mapping-store.cjs';
import paddleModule from '../paddle-client.cjs';
import workerModule from '../process-queue.cjs';
import catalogModule from '../catalog-config.cjs';
import refundReviewModule from '../refund-review-store.cjs';

// Staged only. Separate scheduled execution, never public HTTP. This remains
// disabled until question access, reconciliation and monitoring are built.
export default async ({req,res,error}) => {
  if (req.headers?.['x-appwrite-trigger'] !== 'schedule' || process.env.PAYMENT_PROCESSOR_ENABLED !== 'true') return res.text('Not enabled',503);
  const common={endpoint:process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId:process.env.APPWRITE_FUNCTION_PROJECT_ID,databaseId:process.env.PAYMENT_EVENT_DATABASE,apiKey:process.env.PAYMENT_EVENT_API_KEY};
  let queue,dependencies;
  try {
    queue=queueModule.createQueueStore({...common,collectionId:process.env.PAYMENT_EVENT_COLLECTION});
    const mappings=mappingModule.createMappingStore({...common,collectionId:process.env.PAYMENT_MAPPING_COLLECTION});
    const environment=process.env.PADDLE_ENVIRONMENT;
    const paddle=paddleModule.createPaddleClient({environment,apiKey:process.env.PADDLE_API_KEY});
    const encoded=process.env.CHECKOUT_BINDING_KEY_BASE64;
    if(typeof encoded!=='string'||!/^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(encoded)) throw Error('Invalid binding key');
    const bindingKey=Buffer.from(encoded,'base64');if(bindingKey.length<32||bindingKey.toString('base64')!==encoded) throw Error('Invalid binding key');
    const {allowedRecurringPriceIds,oneTimeDays,productId}=catalogModule.catalogConfig(process.env);
    const tables=new TablesDB(new Client().setEndpoint(common.endpoint).setProject(common.projectId).setKey(common.apiKey));
    const reviews=refundReviewModule.createRefundReviewStore({tables,query:Query,databaseId:common.databaseId,tableId:process.env.REFUND_REVIEW_TABLE});
    dependencies={paddle,mappings,reviews,bindingKey,environment,allowedRecurringPriceIds,oneTimeDays,productId};
  } catch (_) {return res.text('Not configured',503);}
  try {
    const records=await queue.listPending(3);let failures=0;
    for(const record of records){try{await workerModule.processQueuedRecord(record,{queue,dependencies});}catch(_){failures++;}}
    if(failures){error?.(`Payment worker failed to process ${failures} event(s); retry required.`);return res.text('Retry required',503);}
    return res.text('Processed',200);
  } catch (_) {error?.('Payment worker queue lookup failed.');return res.text('Retry required',503);}
};
