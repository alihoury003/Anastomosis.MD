'use strict';
const {buildLegacyMigrationPlan}=require('./legacy-migration.cjs');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
// Server/operator only. Maintenance, owner approval, trusted immutable bank
// snapshot and private review queue are mandatory. Never expose to clients.
async function migrateLegacyBatch({snapshotId,snapshots,users,writer,reviewer,checkpoints,maintenanceConfirmed=false,grandfatheringApproved=false,clock=()=>Date.now(),limit=10}){
  if(maintenanceConfirmed!==true||grandfatheringApproved!==true)return{status:'approval_required',processed:0};
  if(!ID.test(snapshotId||'')||!snapshots||typeof snapshots.load!=='function'||!users||typeof users.listBefore!=='function'||typeof users.getPrefs!=='function'||typeof writer!=='function'||!reviewer||typeof reviewer.save!=='function'||!checkpoints||typeof checkpoints.read!=='function'||typeof checkpoints.advance!=='function'||typeof clock!=='function'||!Number.isInteger(limit)||limit<1||limit>25)throw Error('Migration not configured');
  const snapshot=await snapshots.load(snapshotId);let now=clock();
  if(!snapshot||snapshot.snapshotId!==snapshotId||!Number.isSafeInteger(now)||now<snapshot.capturedAt||now>snapshot.cutoffAt||!Array.isArray(snapshot.questionIds)||!Array.isArray(snapshot.localQuestionIds))return{status:'cutoff_or_snapshot_invalid',processed:0};
  const checkpoint=await checkpoints.read();let cursor=checkpoint?.after??null,processed=0;
  if(checkpoint&&(!Number.isSafeInteger(checkpoint.lastSuccessMs)||checkpoint.lastSuccessMs>now))return{status:'clock_error',processed};
  const page=await users.listBefore({after:cursor,cutoffMs:snapshot.cutoffAt,limit});
  if(!page||!Array.isArray(page.users)||typeof page.hasMore!=='boolean'||page.users.length>limit||(page.hasMore&&!page.users.length))throw Error('Invalid user page');
  let previous=cursor;
  for(const user of page.users){
    now=clock();if(!Number.isSafeInteger(now)||now>snapshot.cutoffAt)return{status:'cutoff_elapsed',processed};
    const created=Date.parse(user?.$createdAt);
    if(!ID.test(user?.$id||'')||!Number.isFinite(created)||created>now||(previous&&user.$id<=previous))throw Error('Invalid user page');
    // API outages are retried, not mistaken for corrupt user preferences.
    let prefs;try{prefs=await users.getPrefs(user.$id);}catch(_){throw Error('User source unavailable');}
    now=clock();if(!Number.isSafeInteger(now)||now>snapshot.cutoffAt)return{status:'cutoff_elapsed',processed};
    const flag=async reason=>{await reviewer.save({snapshotId,userId:user.$id,reason});return{status:'manual_review',processed};};
    let plan;
    try{plan=buildLegacyMigrationPlan({userId:user.$id,accountCreatedAt:created,snapshotAt:now,cutoffAt:snapshot.cutoffAt,prefs,allowedQuestionIds:snapshot.questionIds,localQuestionIds:snapshot.localQuestionIds,allowUnverifiedGrandfathering:true});}
    catch(_){return flag('invalid_legacy_data');}
    if(plan.unknownQuestionReferences)return flag('unknown_questions');
    if(plan.skippedLegacyBlocks)return flag('invalid_blocks');
    if(plan.trialEndCapped)return flag('trial_cap');
    const result=await writer(plan);if(result==='conflict_needs_review')return flag('existing_state_conflict');if(!['stored','already_exists'].includes(result))throw Error('Migration write failed');
    now=clock();if(!Number.isSafeInteger(now)||now>snapshot.cutoffAt)return{status:'cutoff_elapsed',processed};
    if(!await checkpoints.advance(cursor,user.$id,now))return{status:'concurrent',processed};
    cursor=user.$id;previous=user.$id;processed++;
  }
  return{status:page.hasMore?'more':'complete',processed};
}
module.exports={migrateLegacyBatch};
