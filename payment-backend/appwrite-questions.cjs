'use strict';
const {publicMetadata}=require('./question-access.cjs');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
function createQuestionRepository({tables,query,databaseId,tableId}) {
  if(!tables||typeof tables.getRow!=='function'||typeof tables.listRows!=='function'||!query||!['limit','cursorAfter','orderAsc','select'].every(k=>typeof query[k]==='function')||!ID.test(databaseId||'')||!ID.test(tableId||''))throw Error('Question repository not configured');
  async function get(questionId){
    if(!ID.test(questionId||''))throw Error('Invalid question');
    try{return await tables.getRow({databaseId,tableId,rowId:questionId});}
    catch(e){if(e?.code===404&&['row_not_found','document_not_found'].includes(e.type))return null;throw Error('Question lookup failed');}
  }
  async function listMetadata(){
    const out=[],seen=new Set(),limit=100;let cursor=null;
    for(let page=0;page<100;page++){
      const queries=[query.limit(limit),query.orderAsc('$id'),query.select(['$id','subject','system','content'])];if(cursor)queries.push(query.cursorAfter(cursor));
      const res=await tables.listRows({databaseId,tableId,queries});
      if(!res||!Array.isArray(res.rows)||res.rows.length>limit)throw Error('Invalid question list');
      for(const row of res.rows){if(!ID.test(row?.$id||'')||seen.has(row.$id))throw Error('Invalid question list');seen.add(row.$id);out.push(publicMetadata(row));}
      if(res.rows.length<limit)return out;
      cursor=res.rows[res.rows.length-1].$id;
    }
    // Do not silently return an incomplete bank.
    throw Error('Question metadata limit reached');
  }
  return {get,listMetadata};
}
module.exports={createQuestionRepository};
