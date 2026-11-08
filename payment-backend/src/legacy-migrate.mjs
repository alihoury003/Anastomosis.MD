import {Client,TablesDB,Users,Query} from 'node-appwrite';
import snapshotModule from '../legacy-snapshot-store.cjs';
import usersModule from '../appwrite-legacy-users.cjs';
import writerModule from '../legacy-migration.cjs';
import reviewModule from '../appwrite-migration-review.cjs';
import checkpointModule from '../appwrite-checkpoint-store.cjs';
import runnerModule from '../legacy-migration-runner.cjs';
// Operator-only staged function. Never expose to browser execution roles.
export default async({req,res,log,error})=>{
  if(req.headers?.['x-appwrite-trigger']!=='schedule'||process.env.LEGACY_MIGRATION_ENABLED!=='true'||process.env.MIGRATION_MAINTENANCE_CONFIRMED!=='true'||process.env.MIGRATION_GRANDFATHERING_APPROVED!=='true')return res.text('Not enabled',503);
  try{
    const endpoint=process.env.APPWRITE_FUNCTION_API_ENDPOINT,projectId=process.env.APPWRITE_FUNCTION_PROJECT_ID,apiKey=process.env.MIGRATION_ADMIN_API_KEY,databaseId=process.env.USAGE_DATABASE,snapshotId=process.env.LEGACY_SNAPSHOT_ID,cutoffRaw=process.env.LEGACY_MIGRATION_CUTOFF_MS;
    if(endpoint!=='https://nyc.cloud.appwrite.io/v1'||!apiKey||typeof cutoffRaw!=='string'||!/^\d{1,16}$/.test(cutoffRaw)||!Number.isSafeInteger(Number(cutoffRaw))||typeof snapshotId!=='string'||snapshotId.length>25)throw Error('Not configured');
    const client=new Client().setEndpoint(endpoint).setProject(projectId).setKey(apiKey),tables=new TablesDB(client),users=usersModule.createLegacyUserSource({users:new Users(client),query:Query});
    const snapshots=snapshotModule.createLegacySnapshotStore({tables,databaseId,tableId:process.env.MIGRATION_SNAPSHOT_TABLE});
    const snapshot=await snapshots.load(snapshotId);if(snapshot.cutoffAt!==Number(cutoffRaw))throw Error('Cutoff mismatch');
    // The snapshot is immutable and hash-verified; avoid fetching every chunk twice per batch.
    const verifiedSnapshot={load:async requested=>{if(requested!==snapshotId)throw Error('Snapshot mismatch');return snapshot;}};
    const writer=writerModule.createLegacyMigrationWriter({tables,databaseId,tableId:process.env.USAGE_TABLE});
    const reviewer=reviewModule.createMigrationReviewStore({tables,databaseId,tableId:process.env.MIGRATION_REVIEW_TABLE});
    const checkpoints=checkpointModule.createCheckpointStore({tables,databaseId,tableId:process.env.MIGRATION_CHECKPOINT_TABLE,rowId:`migration-${snapshotId}`,cursorKind:'user'});
    const result=await runnerModule.migrateLegacyBatch({snapshotId,snapshots:verifiedSnapshot,users,writer,reviewer,checkpoints,maintenanceConfirmed:true,grandfatheringApproved:true,limit:10});
    if(['complete','more','concurrent'].includes(result.status)){log?.(`Legacy migration: ${result.status}; ${result.processed} accounts processed.`);return res.text(result.status,200);}
    error?.(`Legacy migration requires attention: ${result.status}.`);return res.text('Attention required',503);
  }catch(_){error?.('Legacy migration failed; review required.');return res.text('Migration failed',503);}
};
