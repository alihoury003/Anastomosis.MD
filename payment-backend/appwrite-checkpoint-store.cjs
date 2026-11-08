'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/,EVENT=/^evt_[a-z0-9]{26}$/;
// Private, server-only row with `after` (string, empty means null) and
// `lastSuccessMs` (64-bit integer). Appwrite's actual isolation must be tested.
function createCheckpointStore({tables,databaseId,tableId,rowId,retries=3,cursorKind='event'}){
  if(!['event','user'].includes(cursorKind))throw Error('Invalid cursor kind');
  const CURSOR=cursorKind==='event'?EVENT:ID;
  if(!tables||!['createTransaction','getRow','upsertRow','updateTransaction'].every(k=>typeof tables[k]==='function')||![databaseId,tableId,rowId].every(x=>typeof x==='string'&&ID.test(x))||!Number.isInteger(retries)||retries<1||retries>10)throw Error('Checkpoint not configured');
  async function readRow(transactionId){
    try{const params={databaseId,tableId,rowId,...(transactionId?{transactionId}:{})},row=await tables.getRow(params);if(!row||row.$id!==rowId||typeof row.after!=='string'||(row.after!==''&&!CURSOR.test(row.after))||!Number.isSafeInteger(row.lastSuccessMs)||row.lastSuccessMs<0)throw Error('Invalid checkpoint');return{after:row.after||null,lastSuccessMs:row.lastSuccessMs};}
    catch(e){if(e?.code===404&&['row_not_found','document_not_found'].includes(e.type))return null;throw Error('Checkpoint read failed');}
  }
  async function advance(expectedAfter,newAfter,now){
    if((expectedAfter!==null&&!CURSOR.test(expectedAfter||''))||(newAfter!==null&&!CURSOR.test(newAfter||''))||!Number.isSafeInteger(now)||now<0||(expectedAfter&&(!newAfter||newAfter<expectedAfter)))throw Error('Invalid checkpoint update');
    for(let attempt=0;attempt<retries;attempt++){
      let tx;try{
        tx=await tables.createTransaction({ttl:60});if(!tx||!ID.test(tx.$id||''))throw Error('Invalid transaction');
        const current=await readRow(tx.$id);
        if((current?.after??null)!==expectedAfter||current&&current.lastSuccessMs>now){await tables.updateTransaction({transactionId:tx.$id,rollback:true});return false;}
        await tables.upsertRow({databaseId,tableId,rowId,data:{after:newAfter||'',lastSuccessMs:now},permissions:[],transactionId:tx.$id});
        await tables.updateTransaction({transactionId:tx.$id,commit:true});return true;
      }catch(e){if(tx?.$id){try{await tables.updateTransaction({transactionId:tx.$id,rollback:true});}catch(_){}}if(e?.code===409&&attempt+1<retries)continue;throw Error('Checkpoint update failed');}
    }
    throw Error('Checkpoint update failed');
  }
  return{read:()=>readRow(),advance};
}
module.exports={createCheckpointStore};
