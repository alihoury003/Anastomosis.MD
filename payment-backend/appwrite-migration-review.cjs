'use strict';
const crypto=require('node:crypto');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const REASONS=new Set(['invalid_legacy_data','unknown_questions','invalid_blocks','trial_cap','existing_state_conflict']);
// Private operator queue only. No user ID or preference data belongs in logs.
function createMigrationReviewStore({tables,databaseId,tableId}){
  if(!tables||typeof tables.createRow!=='function'||typeof tables.getRow!=='function'||!ID.test(databaseId||'')||!ID.test(tableId||''))throw Error('Review store not configured');
  return{save:async({snapshotId,userId,reason})=>{
    if(!ID.test(snapshotId||'')||!ID.test(userId||'')||!REASONS.has(reason))throw Error('Invalid review item');
    const rowId='mr_'+crypto.createHash('sha256').update(JSON.stringify([snapshotId,userId,reason])).digest('hex').slice(0,32);
    const data={snapshotId,userId,reason,status:'open'};
    try{await tables.createRow({databaseId,tableId,rowId,data,permissions:[]});return'stored';}
    catch(e){if(e?.code!==409||!['row_already_exists','document_already_exists'].includes(e.type))throw Error('Review write failed');
      try{const current=await tables.getRow({databaseId,tableId,rowId});if(current?.$id!==rowId||current.snapshotId!==snapshotId||current.userId!==userId||current.reason!==reason)throw Error('Review conflict');return'duplicate';}catch(_){throw Error('Review verification failed');}}
  }};
}
module.exports={createMigrationReviewStore};
