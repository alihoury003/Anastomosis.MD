'use strict';
const SUB=/^sub_[a-z0-9]{26}$/;
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const PRICE=/^pri_[a-z0-9]{26}$/;
const NONCE=/^[A-Za-z0-9_-]{32}$/;
function createMappingStore({endpoint,projectId,databaseId,collectionId,apiKey,fetchImpl=globalThis.fetch}) {
  if (endpoint!=='https://nyc.cloud.appwrite.io/v1' || ![projectId,databaseId,collectionId].every(v=>typeof v==='string' && ID.test(v)) || typeof apiKey!=='string' || !apiKey || typeof fetchImpl!=='function') throw Error('Mapping store not configured');
  const base=`${endpoint}/databases/${encodeURIComponent(databaseId)}/collections/${encodeURIComponent(collectionId)}/documents`;
  const headers={'content-type':'application/json','x-appwrite-project':projectId,'x-appwrite-key':apiKey};
  async function save(mapping) {
    const {subscriptionId,userId,priceId,environment,autoRenew,nonce}=mapping||{};
    if (!SUB.test(subscriptionId||'') || !ID.test(userId||'') || !PRICE.test(priceId||'') || !['sandbox','live'].includes(environment) || typeof autoRenew!=='boolean' || !NONCE.test(nonce||'')) throw Error('Invalid mapping');
    const data={userId,priceId,environment,autoRenew,nonce}; const signal=AbortSignal.timeout(4000);
    const response=await fetchImpl(base,{method:'POST',headers,body:JSON.stringify({documentId:subscriptionId,data,permissions:[]}),signal});
    if (response.ok) return 'stored';
    if (response.status!==409) throw Error('Mapping write failed');
    const conflict=await response.json().catch(()=>({}));if(conflict.type!=='document_already_exists') throw Error('Mapping conflict');
    const found=await fetchImpl(`${base}/${encodeURIComponent(subscriptionId)}`,{method:'GET',headers,signal});
    if (!found.ok) throw Error('Mapping lookup failed');const current=await found.json();
    if (current.$id!==subscriptionId || Object.entries(data).some(([key,value])=>current[key]!==value)) throw Error('Mapping conflict');
    return 'duplicate';
  }
  async function listByUser(userId) {
    if(typeof userId!=='string'||!ID.test(userId)) throw Error('Invalid user ID');
    const limit=100,seen=new Set(),results=[];
    for(let offset=0;offset<500;offset+=limit) {
      const url=new URL(base);url.searchParams.append('queries[]',JSON.stringify({method:'equal',attribute:'userId',values:[userId]}));url.searchParams.append('queries[]',JSON.stringify({method:'limit',values:[limit]}));url.searchParams.append('queries[]',JSON.stringify({method:'offset',values:[offset]}));
      const response=await fetchImpl(url.href,{method:'GET',headers,signal:AbortSignal.timeout(4000)});
      if(!response.ok) throw Error('Mapping lookup failed');const body=await response.json();
      if(!Array.isArray(body.documents)||!Number.isInteger(body.total)||body.total<0||body.total>500||body.documents.length>limit) throw Error('Invalid mapping response');
      for(const doc of body.documents){if(doc.userId!==userId||!SUB.test(doc.$id||'')||seen.has(doc.$id))throw Error('Invalid mapping response');seen.add(doc.$id);results.push(doc);}
      if(results.length>=body.total)return results;
      if(body.documents.length<limit) throw Error('Incomplete mapping response');
    }
    throw Error('Incomplete mapping response');
  }
  return {save,listByUser};
}
module.exports={createMappingStore};
