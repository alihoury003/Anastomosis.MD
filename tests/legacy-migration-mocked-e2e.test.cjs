'use strict';
// Mock-only migration simulation. Input snapshot data is user-editable and its
// grandfathering must be explicitly approved before any production use.
const {test}=require('node:test');const assert=require('node:assert/strict');
const {buildLegacyMigrationPlan,createLegacyMigrationWriter}=require('../payment-backend/legacy-migration.cjs');
const {createQuestionAccess,publicMetadata}=require('../payment-backend/question-access.cjs');const {createQuestionRoutes}=require('../payment-backend/question-routes.cjs');
test('legacy account is blocked before private one-time migration, then can review its snapshot references',async()=>{
  const now=Date.parse('2026-10-22T12:00:00Z'),cutoff=now,rows=new Map();
  const tables={createRow:async({rowId,data})=>{if(rows.has(rowId))throw{code:409,type:'row_already_exists'};rows.set(rowId,JSON.parse(data.stateJson));},getRow:async({rowId})=>({$id:rowId,stateJson:JSON.stringify(rows.get(rowId))})};
  const usage={read:async id=>rows.get(id)||null,transact:async(id,fn)=>{const out=await fn(rows.get(id)||null);rows.set(id,structuredClone(out.state));return out.result;}};
  const docs=new Map(['q1','q2','q3'].map(id=>[id,{$id:id,subject:'A',system:'S',stem:'private '+id,correct:'A',content:'{"topic":"T"}'}]));
  const questions={get:async id=>docs.get(id)||null,listMetadata:async()=>[...docs.values()].map(publicMetadata)},entitlements={check:async()=>({status:200,body:{subscribed:false}})};
  const access=createQuestionAccess({questions,usage,entitlements,clock:()=>now}),authenticate=async()=>({status:200,userId:'user1',createdAt:now-86400000});
  const route=createQuestionRoutes({authenticate,access,questions,migrationCutoffMs:cutoff}),request=(path,method,body)=>({path,method,headers:{'x-appwrite-user-jwt':'mock'},bodyText:JSON.stringify(body||{})});
  assert.equal((await route(request('/status','GET'))).body.migrationRequired,true);assert.equal(rows.size,0);
  assert.equal((await route(request('/questions','POST',{questionIds:['q1']}))).status,423);
  const prefs={used:'["q1"]',tests:'[{"id":"t1","qIds":["q1","q2"],"score":1,"total":2}]',notebook:'[]'};
  const plan=buildLegacyMigrationPlan({userId:'user1',accountCreatedAt:now-86400000,snapshotAt:now,cutoffAt:cutoff,prefs,allowedQuestionIds:[...docs.keys()],allowUnverifiedGrandfathering:true});
  const write=createLegacyMigrationWriter({tables,databaseId:'d',tableId:'usage'});assert.equal(await write(plan),'stored');
  assert.equal((await route(request('/status','GET'))).body.migrationRequired,false);
  const review=await route(request('/review','POST',{questionIds:['q1','q2','q3']}));assert.equal(review.status,200);assert.deepEqual(review.body.results.map(x=>x.question.$id),['q1','q2']);assert.equal(review.body.exhausted,true);
  assert.equal(rows.get('user1').freeUsedToday,0);assert.equal(await write(plan),'already_exists');
});
