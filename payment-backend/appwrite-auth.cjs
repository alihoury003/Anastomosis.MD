'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
function createAppwriteAuthenticator({endpoint,projectId,fetchImpl=globalThis.fetch}) {
  if(endpoint!=='https://nyc.cloud.appwrite.io/v1' || typeof projectId!=='string'||!ID.test(projectId)||typeof fetchImpl!=='function') throw Error('Authentication not configured');
  return async function authenticate(jwt) {
    if(typeof jwt!=='string'||jwt.length<20||jwt.length>10000) return {status:401};
    let response;try{response=await fetchImpl(`${endpoint}/account`,{method:'GET',headers:{'x-appwrite-project':projectId,'x-appwrite-jwt':jwt},signal:AbortSignal.timeout(4000)});}catch(_){return{status:503};}
    if(response.status===401||response.status===403)return{status:401};if(!response.ok)return{status:503};
    let account;try{account=await response.json();}catch(_){return{status:503};}
    if(typeof account?.$id!=='string'||!ID.test(account.$id))return{status:503};
    const createdAt=typeof account.$createdAt==='string'?Date.parse(account.$createdAt):NaN;
    return{status:200,userId:account.$id,createdAt:Number.isFinite(createdAt)?createdAt:null};
  };
}
module.exports={createAppwriteAuthenticator};
