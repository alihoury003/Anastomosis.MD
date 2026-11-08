'use strict';
const {timestamp,classifyAdjustment}=require('./adjustment-policy.cjs');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/,ADJ=/^adj_[a-z0-9]{26}$/;
function createRefundReviewStore({tables,query,databaseId,tableId,retries=3}){
  if(!tables||!['createTransaction','getRow','upsertRow','updateTransaction','listRows'].every(k=>typeof tables[k]==='function')||!query||!['limit','equal','orderAsc'].every(k=>typeof query[k]==='function')||!ID.test(databaseId||'')||!ID.test(tableId||'')||!Number.isInteger(retries)||retries<1||retries>10)throw Error('Refund review store not configured');
  async function read(id,transactionId){
    if(!ADJ.test(id||''))throw Error('Invalid review ID');
    try{const row=await tables.getRow({databaseId,tableId,rowId:id,...(transactionId?{transactionId}:{})});if(!row||row.$id!==id||!ID.test(row.userId||'')||typeof row.billingId!=='string'||timestamp(row.updatedAt)===null||!['pending','allow','restrict','not_required'].includes(row.decision)||typeof row.historyJson!=='string'||row.historyJson.length>32000)throw Error('Invalid review record');let history;try{history=JSON.parse(row.historyJson)}catch(_){throw Error('Invalid review record')}if(!Array.isArray(history)||history.length>200)throw Error('Invalid review record');return{...row,history};}catch(e){if(e?.code===404&&['row_not_found','document_not_found'].includes(e.type))return null;throw Error('Review read failed');}
  }
  async function transaction(fn){
    for(let attempt=0;attempt<retries;attempt++){
      let tx;try{tx=await tables.createTransaction({ttl:60});if(!ID.test(tx?.$id||''))throw Error('Invalid transaction');const result=await fn(tx.$id);if(result.noWrite){await tables.updateTransaction({transactionId:tx.$id,rollback:true});return result.value;}await tables.upsertRow({databaseId,tableId,rowId:result.id,data:result.data,permissions:[],transactionId:tx.$id});await tables.updateTransaction({transactionId:tx.$id,commit:true});return result.value;}
      catch(e){if(tx?.$id){try{await tables.updateTransaction({transactionId:tx.$id,rollback:true});}catch(_){}}if(e?.code===409&&attempt+1<retries)continue;throw Error('Review transaction failed');}
    }
    throw Error('Review transaction failed');
  }
  async function sync({adjustment,billingId,userId}){
    const classification=classifyAdjustment(adjustment,billingId);if(!classification.valid||!ID.test(userId||''))throw Error('Invalid adjustment');
    return transaction(async tx=>{
      const existing=await read(adjustment.id,tx),version=timestamp(adjustment.updated_at);
      if(existing){
        if(existing.userId!==userId||existing.billingId!==billingId)throw Error('Review owner conflict');
        const current=timestamp(existing.updatedAt);if(version<current)return{noWrite:true,value:'stale'};
        if(version===current){if(existing.action!==adjustment.action||existing.adjustmentType!==(adjustment.type??'')||existing.paddleStatus!==adjustment.status)throw Error('Review version conflict');return{noWrite:true,value:'unchanged'};}
      }
      const history=existing?.history||[];
      const data={userId,billingId,action:adjustment.action,adjustmentType:adjustment.type??'',paddleStatus:adjustment.status,updatedAt:adjustment.updated_at,decision:classification.needsReview?'pending':'not_required',historyJson:JSON.stringify(history)};
      return{id:adjustment.id,data,value:existing?'updated':'created'};
    });
  }
  async function decide({adjustmentId,expectedUpdatedAt,decision,adminUserId,now=Date.now()}){
    if(!ADJ.test(adjustmentId||'')||timestamp(expectedUpdatedAt)===null||!['allow','restrict'].includes(decision)||!ID.test(adminUserId||'')||!Number.isSafeInteger(now)||now<0)throw Error('Invalid review decision');
    return transaction(async tx=>{
      const existing=await read(adjustmentId,tx);if(!existing)throw Error('Review not found');
      if(timestamp(existing.updatedAt)!==timestamp(expectedUpdatedAt))return{noWrite:true,value:'stale'};
      if(existing.decision===decision)return{noWrite:true,value:'unchanged'};
      if(existing.decision!=='pending')return{noWrite:true,value:'already_decided'};
      if(existing.history.length>=200)throw Error('Review history full');
      const history=[...existing.history,{updatedAt:existing.updatedAt,decision,adminUserId,decidedAt:new Date(now).toISOString()}],historyJson=JSON.stringify(history);
      if(historyJson.length>32000)throw Error('Review history full');
      const data={userId:existing.userId,billingId:existing.billingId,action:existing.action,adjustmentType:existing.adjustmentType,paddleStatus:existing.paddleStatus,updatedAt:existing.updatedAt,decision,historyJson};
      return{id:adjustmentId,data,value:'decided'};
    });
  }
  async function getDecision({adjustment,billingId,userId}){
    const classification=classifyAdjustment(adjustment,billingId);if(!classification.valid||!ID.test(userId||''))throw Error('Invalid adjustment');
    const existing=await read(adjustment.id);if(!existing)return null;
    if(existing.userId!==userId||existing.billingId!==billingId)throw Error('Review owner conflict');
    if(timestamp(existing.updatedAt)!==timestamp(adjustment.updated_at))return null;
    if(existing.action!==adjustment.action||existing.adjustmentType!==(adjustment.type??'')||existing.paddleStatus!==adjustment.status)throw Error('Review version conflict');
    return ['allow','restrict'].includes(existing.decision)?existing.decision:null;
  }
  async function getForAdmin(adjustmentId){
    const row=await read(adjustmentId);if(!row)return null;
    return{adjustmentId:row.$id,userId:row.userId,billingId:row.billingId,action:row.action,adjustmentType:row.adjustmentType,paddleStatus:row.paddleStatus,updatedAt:row.updatedAt,decision:row.decision};
  }
  async function listPending(limit=25){
    if(!Number.isInteger(limit)||limit<1||limit>25)throw Error('Invalid review limit');
    const result=await tables.listRows({databaseId,tableId,queries:[query.equal('decision','pending'),query.orderAsc('updatedAt'),query.limit(limit)]});
    if(!result||!Array.isArray(result.rows)||result.rows.length>limit)throw Error('Invalid review list');
    return result.rows.map(row=>({adjustmentId:row.$id,userId:row.userId,billingId:row.billingId,action:row.action,adjustmentType:row.adjustmentType,paddleStatus:row.paddleStatus,updatedAt:row.updatedAt}));
  }
  async function countPending(){
    const result=await tables.listRows({databaseId,tableId,queries:[query.equal('decision','pending'),query.limit(1)],total:true});
    if(!result||!Number.isSafeInteger(result.total)||result.total<0)throw Error('Invalid review count');
    return result.total;
  }
  return{sync,decide,getDecision,getForAdmin,listPending,countPending};
}
module.exports={createRefundReviewStore};
