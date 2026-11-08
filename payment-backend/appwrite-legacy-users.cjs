'use strict';
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
// Server-only adapter. Uses Appwrite Users API; never expose to clients.
function createLegacyUserSource({users,query}){
  if(!users||!['list','getPrefs'].every(k=>typeof users[k]==='function')||!query||!['limit','orderAsc','lessThanEqual','cursorAfter'].every(k=>typeof query[k]==='function'))throw Error('User source not configured');
  async function listBefore({after=null,cutoffMs,limit=10}){
    if((after!==null&&!ID.test(after||''))||!Number.isSafeInteger(cutoffMs)||cutoffMs<0||!Number.isInteger(limit)||limit<1||limit>25)throw Error('Invalid user page request');
    const queries=[query.limit(limit),query.orderAsc('$id'),query.lessThanEqual('$createdAt',new Date(cutoffMs).toISOString())];if(after)queries.push(query.cursorAfter(after));
    const result=await users.list({queries});if(!result||!Array.isArray(result.users)||result.users.length>limit)throw Error('Invalid user page');
    let prior=after;
    for(const user of result.users){const created=Date.parse(user?.$createdAt);if(!ID.test(user?.$id||'')||!Number.isFinite(created)||created>cutoffMs||(prior&&user.$id<=prior))throw Error('Invalid user page');prior=user.$id;}
    return{users:result.users,hasMore:result.users.length===limit};
  }
  async function getPrefs(userId){if(!ID.test(userId||''))throw Error('Invalid user');const prefs=await users.getPrefs({userId});if(!prefs||typeof prefs!=='object'||Array.isArray(prefs))throw Error('Invalid preferences');return prefs;}
  return{listBefore,getPrefs};
}
module.exports={createLegacyUserSource};
