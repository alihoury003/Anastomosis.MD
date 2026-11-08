import webhook from '../paddle-webhook.cjs';
import store from '../appwrite-event-store.cjs';

// Staged only. A real, monitored processor is required before this endpoint
// may acknowledge webhooks. Never enable the queue flag until the entire
// purchase, access and retry flow has been reviewed and tested.
export default async ({ req, res }) => {
  if (process.env.PAYMENT_QUEUE_ENABLED !== 'true') return res.text('Not enabled', 503);
  let archive;
  try {
    archive = store.createEventArchive({
      endpoint: process.env.APPWRITE_FUNCTION_API_ENDPOINT,
      projectId: process.env.APPWRITE_FUNCTION_PROJECT_ID,
      databaseId: process.env.PAYMENT_EVENT_DATABASE,
      collectionId: process.env.PAYMENT_EVENT_COLLECTION,
      apiKey: process.env.PAYMENT_EVENT_API_KEY
    });
  } catch (_) { return res.text('Not configured', 503); }
  const binary = req.bodyBinary;
  const rawBody = Buffer.isBuffer(binary) ? binary : binary instanceof Uint8Array ? Buffer.from(binary) : binary instanceof ArrayBuffer ? Buffer.from(binary) : null;
  const result = await webhook.handleWebhook({
    method:req.method, rawBody, signature:req.headers?.['paddle-signature'],
    secret:process.env.PADDLE_WEBHOOK_SECRET, archive
  });
  return res.text(result.body, result.status);
};
