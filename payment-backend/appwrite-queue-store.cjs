'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const EVENT=/^evt_[a-z0-9]{26}$/;
function createQueueStore({endpoint,projectId,databaseId,collectionId,apiKey,fetchImpl=globalThis.fetch}) {
  if (endpoint!=='https://nyc.cloud.appwrite.io/v1' || ![projectId,databaseId,collectionId].every(v=>typeof v==='string'&&ID.test(v)) || typeof apiKey!=='string'||!apiKey||typeof fetchImpl!=='function') throw Error('Queue not configured');
  const base=`${endpoint}/databases/${encodeURIComponent(databaseId)}/collections/${encodeURIComponent(collectionId)}/documents`;
  const headers={'content-type':'application/json','x-appwrite-project':projectId,'x-appwrite-key':apiKey};
  async function listPending(limit=3) {
    if(!Number.isInteger(limit)||limit<1||limit>10) throw Error('Invalid queue limit');
    const url=new URL(base);url.searchParams.append('queries[]',JSON.stringify({method:'equal',attribute:'processingStatus',values:['pending']}));url.searchParams.append('queries[]',JSON.stringify({method:'limit',values:[limit]}));
    const res=await fetchImpl(url.href,{method:'GET',headers,signal:AbortSignal.timeout(4000)});
    if(!res.ok) throw Error('Queue lookup failed');const data=await res.json();
    if(!Array.isArray(data.documents)||data.documents.length>limit) throw Error('Invalid queue response');
    return data.documents;
  }
  async function complete(id,status) {
    if(!EVENT.test(id||'') || !['done','manual_review'].includes(status)) throw Error('Invalid queue update');
    const res=await fetchImpl(`${base}/${encodeURIComponent(id)}`,{method:'PATCH',headers,body:JSON.stringify({data:{processingStatus:status}}),signal:AbortSignal.timeout(4000)});
    if(!res.ok) throw Error('Queue update failed');
  }
  async function count(status) {
    if(!['pending','manual_review','done'].includes(status))throw Error('Invalid queue status');
    const url=new URL(base);url.searchParams.append('queries[]',JSON.stringify({method:'equal',attribute:'processingStatus',values:[status]}));url.searchParams.append('queries[]',JSON.stringify({method:'limit',values:[1]}));url.searchParams.append('queries[]',JSON.stringify({method:'select',values:['$id']}));
    const res=await fetchImpl(url.href,{method:'GET',headers,signal:AbortSignal.timeout(4000)});if(!res.ok)throw Error('Queue count failed');const data=await res.json();if(!Number.isSafeInteger(data.total)||data.total<0)throw Error('Invalid queue count');return data.total;
  }
  return {listPending,complete,count};
}
module.exports={createQueueStore};
