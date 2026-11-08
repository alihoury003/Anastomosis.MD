'use strict';
const crypto=require('node:crypto');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const SNAPSHOT=/^[A-Za-z0-9][A-Za-z0-9._-]{0,24}$/;
const CHUNK=250,MAX_IDS=10000;
function digest(ids){return crypto.createHash('sha256').update(JSON.stringify(ids),'utf8').digest('hex');}
function createLegacySnapshotStore({tables,databaseId,tableId}){
  if(!tables||!['createTransaction','createRow','getRow','updateTransaction'].every(k=>typeof tables[k]==='function')||!ID.test(databaseId||'')||!ID.test(tableId||''))throw Error('Snapshot store not configured');
  async function write({snapshotId,questionIds,localQuestionIds,capturedAt,cutoffAt,maintenanceConfirmed,grandfatheringApproved}){
    if(maintenanceConfirmed!==true||grandfatheringApproved!==true)throw Error('Explicit migration approval required');
    if(!SNAPSHOT.test(snapshotId||'')||!Array.isArray(questionIds)||questionIds.length>MAX_IDS||questionIds.some(x=>typeof x!=='string'||!ID.test(x))||new Set(questionIds).size!==questionIds.length||!Array.isArray(localQuestionIds)||localQuestionIds.length>100||localQuestionIds.some(x=>typeof x!=='string'||!ID.test(x))||new Set(localQuestionIds).size!==localQuestionIds.length||![capturedAt,cutoffAt].every(Number.isSafeInteger)||capturedAt<0||capturedAt>cutoffAt)throw Error('Invalid snapshot');
    const sorted=[...questionIds].sort(),local=[...localQuestionIds].sort(),chunks=[];for(let i=0;i<sorted.length;i+=CHUNK)chunks.push(sorted.slice(i,i+CHUNK));
    const manifest={version:1,snapshotId,capturedAt,cutoffAt,count:sorted.length,chunkCount:chunks.length,idsHash:digest(sorted),localQuestionIds:local};
    let tx;
    try{
      tx=await tables.createTransaction({ttl:60});if(!ID.test(tx?.$id||''))throw Error('Invalid transaction');
      for(let i=0;i<chunks.length;i++)await tables.createRow({databaseId,tableId,rowId:`${snapshotId}_${i}`,data:{snapshotJson:JSON.stringify(chunks[i])},permissions:[],transactionId:tx.$id});
      await tables.createRow({databaseId,tableId,rowId:snapshotId,data:{snapshotJson:JSON.stringify(manifest)},permissions:[],transactionId:tx.$id});
      await tables.updateTransaction({transactionId:tx.$id,commit:true});return{snapshotId,count:sorted.length};
    }catch(_){if(tx?.$id){try{await tables.updateTransaction({transactionId:tx.$id,rollback:true});}catch(_){}}throw Error('Snapshot write failed');}
  }
  async function load(snapshotId){
    if(!SNAPSHOT.test(snapshotId||''))throw Error('Invalid snapshot');
    try{
      const row=await tables.getRow({databaseId,tableId,rowId:snapshotId});if(row?.$id!==snapshotId||typeof row.snapshotJson!=='string'||row.snapshotJson.length>10000)throw Error('Invalid snapshot');
      const manifest=JSON.parse(row.snapshotJson);
      if(manifest.version!==1||manifest.snapshotId!==snapshotId||!Number.isSafeInteger(manifest.capturedAt)||!Number.isSafeInteger(manifest.cutoffAt)||manifest.capturedAt<0||manifest.capturedAt>manifest.cutoffAt||!Number.isInteger(manifest.count)||manifest.count<0||manifest.count>MAX_IDS||!Number.isInteger(manifest.chunkCount)||manifest.chunkCount!==Math.ceil(manifest.count/CHUNK)||!Array.isArray(manifest.localQuestionIds)||manifest.localQuestionIds.length>100||manifest.localQuestionIds.some(x=>typeof x!=='string'||!ID.test(x))||new Set(manifest.localQuestionIds).size!==manifest.localQuestionIds.length||!/^[a-f0-9]{64}$/.test(manifest.idsHash||''))throw Error('Invalid snapshot');
      const ids=[];for(let i=0;i<manifest.chunkCount;i++){
        const chunkId=`${snapshotId}_${i}`,chunk=await tables.getRow({databaseId,tableId,rowId:chunkId});
        if(chunk?.$id!==chunkId||typeof chunk.snapshotJson!=='string'||chunk.snapshotJson.length>12000)throw Error('Invalid snapshot');
        const data=JSON.parse(chunk.snapshotJson);if(!Array.isArray(data)||data.length<1||data.length>CHUNK||data.some(x=>typeof x!=='string'||!ID.test(x)))throw Error('Invalid snapshot');ids.push(...data);
      }
      if(ids.length!==manifest.count||new Set(ids).size!==ids.length||ids.some((id,i)=>i>0&&id<=ids[i-1])||digest(ids)!==manifest.idsHash)throw Error('Invalid snapshot');
      return{...manifest,questionIds:ids};
    }catch(_){throw Error('Snapshot read failed');}
  }
  return{write,load};
}
module.exports={createLegacySnapshotStore};
