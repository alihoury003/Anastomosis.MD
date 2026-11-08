'use strict';
// Exercises our adapter with the actual pinned node-appwrite SDK request
// construction but a fake client transport, not a real Appwrite server.
const {test}=require('node:test');const assert=require('node:assert/strict');
const {Client,TablesDB,Query}=require('../payment-backend/node_modules/node-appwrite');
const {createUsageStore}=require('../payment-backend/appwrite-usage-store.cjs');const {createQuestionRepository}=require('../payment-backend/appwrite-questions.cjs');
test('pinned SDK sends transaction IDs and private row permissions as expected',async()=>{
  const client=new Client().setEndpoint('https://nyc.cloud.appwrite.io/v1').setProject('p').setKey('test'),calls=[];let staged;
  client.call=async(method,url,headers,payload)=>{calls.push({method,path:url.pathname,payload});if(url.pathname==='/v1/tablesdb/transactions'&&method==='post')return{$id:'tx1'};if(url.pathname.endsWith('/rows/user1')&&method==='get')throw{code:404,type:'row_not_found'};if(url.pathname.endsWith('/rows/user1')&&method==='put'){staged=payload;return{};}if(url.pathname.endsWith('/transactions/tx1')&&method==='patch')return{};throw Error('unexpected SDK request')};
  const usage=createUsageStore({tables:new TablesDB(client),databaseId:'d',tableId:'usage'});const result=await usage.transact('user1',async()=>({state:{value:1},result:'committed'}));
  assert.equal(result,'committed');assert.equal(calls[1].payload.transactionId,'tx1');assert.equal(staged.transactionId,'tx1');assert.deepEqual(staged.permissions,[]);assert.equal(JSON.parse(staged.data.stateJson).value,1);assert.equal(calls.at(-1).payload.commit,true);
});
test('pinned SDK uses cursor pagination and server-side field selection for metadata',async()=>{
  const client=new Client().setEndpoint('https://nyc.cloud.appwrite.io/v1').setProject('p').setKey('test');let request;
  client.call=async(method,url,headers,payload)=>{request={method,path:url.pathname,payload};return{rows:[{$id:'q1',subject:'A',system:'S',content:'{"topic":"T"}'}]}};
  const repo=createQuestionRepository({tables:new TablesDB(client),query:Query,databaseId:'d',tableId:'questions'});const rows=await repo.listMetadata();assert.equal(rows[0].topic,'T');assert.equal(request.method,'get');assert.match(request.path,/\/rows$/);assert.ok(request.payload.queries.some(q=>q.includes('select')));
});
test('pinned server SDK constructs authenticated user list and preference calls',async()=>{const {Users}=require('../payment-backend/node_modules/node-appwrite');const client=new Client().setEndpoint('https://nyc.cloud.appwrite.io/v1').setProject('p').setKey('test');let calls=[];client.call=async(method,url,headers,payload)=>{calls.push({method,path:url.pathname,payload});return url.pathname.endsWith('/prefs')?{tests:'[]'}:{users:[]}};const users=new Users(client);await users.list({queries:[Query.limit(10),Query.orderAsc('$id'),Query.lessThanEqual('$createdAt','2026-10-22T12:00:00Z')]});await users.getPrefs({userId:'u1'});assert.match(calls[0].path,/\/users$/);assert.ok(calls[0].payload.queries.some(x=>x.includes('$createdAt')));assert.match(calls[1].path,/\/users\/u1\/prefs$/);});
