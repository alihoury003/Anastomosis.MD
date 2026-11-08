'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
// The usage table is PRIVATE and has a mediumtext/longtext stateJson column.
// This adapter relies on Appwrite's transactional conflict detection. Real
// Appwrite concurrency, schema and SDK compatibility MUST be verified before use.
function createUsageStore({tables, databaseId, tableId, retries=5}) {
  if(!tables||!['createTransaction','getRow','upsertRow','updateTransaction'].every(k=>typeof tables[k]==='function') || !ID.test(databaseId||'') || !ID.test(tableId||'') || !Number.isInteger(retries)||retries<1||retries>10) throw Error('Usage store not configured');
  async function read(userId) {
    if(!ID.test(userId||''))throw Error('Invalid usage request');
    let row;try{row=await tables.getRow({databaseId,tableId,rowId:userId});}
    catch(e){if(e?.code===404&&['row_not_found','document_not_found'].includes(e.type))return null;throw Error('Usage read failed');}
    if(!row||row.$id!==userId||typeof row.stateJson!=='string'||row.stateJson.length>700000)throw Error('Invalid usage record');
    try{return JSON.parse(row.stateJson);}catch(_){throw Error('Invalid usage record');}
  }
  async function transact(userId, decide) {
    if(!ID.test(userId||'')||typeof decide!=='function')throw Error('Invalid usage request');
    for(let attempt=0;attempt<retries;attempt++) {
      let tx;
      try {
        tx=await tables.createTransaction({ttl:60});
        if(!tx||!ID.test(tx.$id||''))throw Error('Invalid transaction');
        let previous=null;
        try {
          const row=await tables.getRow({databaseId,tableId,rowId:userId,transactionId:tx.$id});
          if(!row||row.$id!==userId||typeof row.stateJson!=='string'||row.stateJson.length>700000)throw Error('Invalid usage record');
          previous=JSON.parse(row.stateJson);
        } catch(e) {
          if(!(e&&e.code===404&&['row_not_found','document_not_found'].includes(e.type)))throw e;
        }
        const outcome=await decide(previous);
        if(!outcome||!outcome.state||!outcome.result)throw Error('Invalid usage decision');
        const stateJson=JSON.stringify(outcome.state);
        if(stateJson.length>700000)throw Error('Usage record too large');
        await tables.upsertRow({databaseId,tableId,rowId:userId,data:{stateJson},permissions:[],transactionId:tx.$id});
        await tables.updateTransaction({transactionId:tx.$id,commit:true});
        return outcome.result;
      } catch(e) {
        if(tx?.$id){try{await tables.updateTransaction({transactionId:tx.$id,rollback:true});}catch(_) {}}
        if(e?.code===409&&attempt+1<retries)continue;
        throw Error('Usage transaction failed');
      }
    }
    throw Error('Usage transaction failed');
  }
  return {read,transact};
}
module.exports={createUsageStore};
