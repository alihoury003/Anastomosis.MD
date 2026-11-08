import {Client,TablesDB,Query} from 'node-appwrite';
import questionsModule from '../appwrite-questions.cjs';
import snapshotModule from '../legacy-snapshot-store.cjs';
// Operator-only staged function. Never enable while students are using the
// site, without approval, or without configuring private tables and backups.
export default async({req,res,log,error})=>{
  if(req.headers?.['x-appwrite-trigger']!=='schedule'||process.env.LEGACY_SNAPSHOT_ENABLED!=='true'||process.env.MIGRATION_MAINTENANCE_CONFIRMED!=='true'||process.env.MIGRATION_GRANDFATHERING_APPROVED!=='true')return res.text('Not enabled',503);
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,apiKey=process.env.MIGRATION_ADMIN_API_KEY,rawCutoff=process.env.LEGACY_MIGRATION_CUTOFF_MS;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!apiKey||typeof rawCutoff!=='string'||!/^\d{1,16}$/.test(rawCutoff)||!Number.isSafeInteger(Number(rawCutoff)))throw Error('Not configured');
    const tables=new TablesDB(new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey));
    const questions=questionsModule.createQuestionRepository({tables,query:Query,databaseId:process.env.QUESTION_DATABASE,tableId:process.env.QUESTION_TABLE});
    const snapshots=snapshotModule.createLegacySnapshotStore({tables,databaseId:process.env.USAGE_DATABASE,tableId:process.env.MIGRATION_SNAPSHOT_TABLE});
    const metadata=await questions.listMetadata(),capturedAt=Date.now(),cutoffAt=Number(rawCutoff);
    const result=await snapshots.write({snapshotId:process.env.LEGACY_SNAPSHOT_ID,questionIds:metadata.map(q=>q.id),localQuestionIds:['q1','q2','q3'],capturedAt,cutoffAt,maintenanceConfirmed:true,grandfatheringApproved:true});
    log?.(`Private migration snapshot saved: ${result.count} question IDs.`);return res.text('Snapshot saved',200);
  }catch(_){error?.('Migration snapshot failed; review required.');return res.text('Snapshot failed',503);}
};
