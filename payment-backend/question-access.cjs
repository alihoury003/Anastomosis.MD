'use strict';
// Staged question-delivery policy. This file is not wired to production.
// userId must come from a JWT verified by Appwrite; paid status must be
// evaluated server-side. The usage store MUST provide per-user serializable
// transactions and persist privately before returning. See README.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
const BILLING=/^(?:sub|txn)_[a-z0-9]{26}$/;
const DAY_MS=86400000, TRIAL_MS=7*DAY_MS, TRIAL_LIMIT=150, FIRST_DAY=40, DAILY=10;
function utcDay(now){return Math.floor(now/DAY_MS);}
function freshState(){return{version:1,firstFreeDay:null,lastFreeDay:null,freeUsedToday:0,trialStartedAt:null,trialUsed:0,grantedIds:[],paidGrants:[]};}
function validState(s){
  if(!s||s.version!==1||(s.legacyMigrationComplete!==undefined&&typeof s.legacyMigrationComplete!=='boolean')||!Number.isSafeInteger(s.freeUsedToday)||s.freeUsedToday<0||!Number.isSafeInteger(s.trialUsed)||s.trialUsed<0||s.trialUsed>TRIAL_LIMIT||!Array.isArray(s.grantedIds)||s.grantedIds.length>10000||s.grantedIds.some(v=>typeof v!=='string'||!ID.test(v))||new Set(s.grantedIds).size!==s.grantedIds.length)return false;
  if(!Array.isArray(s.paidGrants)||s.paidGrants.length>10000)return false;
  const paidIds=new Set();for(const grant of s.paidGrants){if(!grant||typeof grant.questionId!=='string'||!ID.test(grant.questionId)||paidIds.has(grant.questionId)||!Array.isArray(grant.sources)||grant.sources.length<1||grant.sources.length>25||grant.sources.some(id=>typeof id!=='string'||!BILLING.test(id))||new Set(grant.sources).size!==grant.sources.length)return false;paidIds.add(grant.questionId);}
  if(s.trialStartedAt===null){if(s.trialUsed!==0)return false;}else if(!Number.isSafeInteger(s.trialStartedAt)||s.trialStartedAt<0)return false;
  if(s.firstFreeDay===null)return s.lastFreeDay===null&&s.freeUsedToday===0;
  if(!Number.isSafeInteger(s.firstFreeDay)||!Number.isSafeInteger(s.lastFreeDay)||s.firstFreeDay<0||s.lastFreeDay<s.firstFreeDay)return false;
  return s.freeUsedToday<=(s.lastFreeDay===s.firstFreeDay?FIRST_DAY:DAILY);
}
function summarizeUsage(state,now){
  const day=utcDay(now),effectiveDay=state.lastFreeDay===null?day:Math.max(day,state.lastFreeDay);
  const first=state.firstFreeDay===null,used=state.lastFreeDay===null||day>state.lastFreeDay?0:state.freeUsedToday;
  const max=first||effectiveDay===state.firstFreeDay?FIRST_DAY:DAILY;
  const trialStarted=state.trialStartedAt!==null;
  const trialEndsAt=trialStarted?state.trialStartedAt+TRIAL_MS:null;
  return{freeRemaining:Math.max(0,max-used),firstFreeDay:first||effectiveDay===state.firstFreeDay,legacyMigrationComplete:state.legacyMigrationComplete===true,trialStarted,trialActive:trialStarted&&now>=state.trialStartedAt&&now<trialEndsAt&&state.trialUsed<TRIAL_LIMIT,trialUsed:state.trialUsed,trialEndsAt};
}
function publicQuestion(doc){
  if(!doc||typeof doc!=='object'||!ID.test(doc.$id||''))throw Error('Invalid question');
  // Explicit fields only: never return permissions, backend metadata or secrets.
  const out={$id:doc.$id};for(const k of ['subject','system','stem','correct','objective','content'])if(Object.hasOwn(doc,k))out[k]=doc[k];return out;
}
function publicMetadata(doc){
  if(!doc||typeof doc!=='object'||!ID.test(doc.$id||''))throw Error('Invalid question');
  let content={};try{content=typeof doc.content==='string'?JSON.parse(doc.content||'{}'):(doc.content||{});}catch(_){content={};}
  const bounded=v=>typeof v==='string'?v.slice(0,200):'';
  return{id:doc.$id,subject:bounded(doc.subject),system:bounded(doc.system),topic:bounded(content.topic),difficulty:Number.isFinite(content.difficulty)?content.difficulty:null};
}
function createQuestionAccess({questions,usage,entitlements,clock=()=>Date.now()}) {
  if(!questions||typeof questions.get!=='function'||!usage||typeof usage.transact!=='function'||typeof usage.read!=='function'||!entitlements||typeof entitlements.check!=='function'||typeof clock!=='function')throw Error('Question access not configured');
  async function getEntitlement(userId){
    let result;try{result=await entitlements.check(userId);}catch(_){return{unavailable:true};}
    if(result?.status===503)return{unavailable:true};
    if(result?.status!==200||typeof result.body?.subscribed!=='boolean')throw Error('Invalid entitlement');
    return{unavailable:false,body:result.body};
  }
  async function status(userId){
    if(!ID.test(userId||''))return{status:401,body:{error:'Sign in required'}};
    const now=clock();if(!Number.isSafeInteger(now)||now<0)return{status:503,body:{error:'Service unavailable'}};
    let entitlement;try{entitlement=await getEntitlement(userId);}catch(_){return{status:503,body:{error:'Service unavailable'}};}
    try{const previous=await usage.read(userId);const state=previous===null?freshState():structuredClone(previous);if(!validState(state))throw Error('Invalid usage state');return{status:200,body:{subscribed:entitlement.unavailable?false:entitlement.body.subscribed,reviewPending:entitlement.unavailable?false:entitlement.body.reviewPending===true,billingUnavailable:entitlement.unavailable,usage:summarizeUsage(state,now)}};}catch(_){return{status:503,body:{error:'Service unavailable'}};}
  }
  async function startTrial(userId){
    if(!ID.test(userId||''))return{status:401,body:{error:'Sign in required'}};
    const now=clock();if(!Number.isSafeInteger(now)||now<0)return{status:503,body:{error:'Service unavailable'}};
    try{const entitlement=await getEntitlement(userId);if(entitlement.unavailable)return{status:503,body:{error:'Access verification unavailable'}};if(entitlement.body.subscribed)return{status:409,body:{error:'Already subscribed'}};}catch(_){return{status:503,body:{error:'Service unavailable'}};}
    try{return await usage.transact(userId,async previous=>{
      const state=previous===null?freshState():structuredClone(previous);if(!validState(state))throw Error('Invalid usage state');
      if(state.trialStartedAt!==null)return{state,result:{status:409,body:{error:'Trial already started'}}};
      state.trialStartedAt=now;return{state,result:{status:200,body:{trialEndsAt:now+TRIAL_MS,trialLimit:TRIAL_LIMIT,usage:summarizeUsage(state,now)}}};
    });}catch(_){return{status:503,body:{error:'Service unavailable'}};}
  }
  function hasReviewGrant(state,questionId,reviewable){
    if(state.grantedIds.includes(questionId))return true;
    const paid=state.paidGrants.find(g=>g.questionId===questionId);return !!paid&&paid.sources.some(id=>reviewable.has(id));
  }
  function issueOne(state, questionId, now, reviewable){
    if(hasReviewGrant(state,questionId,reviewable))return {source:'review'};
    if(state.grantedIds.length>=10000)throw Error('Usage state full');
    const trialActive=state.trialStartedAt!==null && now>=state.trialStartedAt && now<state.trialStartedAt+TRIAL_MS && state.trialUsed<TRIAL_LIMIT;
    if(trialActive){state.trialUsed++;state.grantedIds.push(questionId);return{source:'trial',trialUsed:state.trialUsed};}
    const day=utcDay(now);
    if(state.firstFreeDay===null){state.firstFreeDay=day;state.lastFreeDay=day;}
    if(day>state.lastFreeDay){state.lastFreeDay=day;state.freeUsedToday=0;}
    // Never reset quota if the server clock goes backwards.
    const max=state.lastFreeDay===state.firstFreeDay?FIRST_DAY:DAILY;
    if(state.freeUsedToday>=max)return null;
    state.freeUsedToday++;state.grantedIds.push(questionId);
    return{source:'free',remaining:max-state.freeUsedToday};
  }
  async function getQuestions(userId,questionIds,{reviewOnly=false}={}){
    if(!ID.test(userId||''))return{status:401,body:{error:'Sign in required'}};
    if(!Array.isArray(questionIds)||questionIds.length<1||questionIds.length>20||
       questionIds.some(id=>typeof id!=='string'||!ID.test(id))||new Set(questionIds).size!==questionIds.length)return{status:400,body:{error:'Invalid questions'}};
    const now=clock();if(!Number.isSafeInteger(now)||now<0)return{status:503,body:{error:'Service unavailable'}};
    let entitlement,docs;
    try{
      entitlement=await getEntitlement(userId);
      if(!entitlement.unavailable){
        if(entitlement.body.admin===true&&entitlement.body.subscribed!==true)throw Error('Invalid admin entitlement');
        if(entitlement.body.admin!==true){
          const active=entitlement.body.activeBillingIds,reviewable=entitlement.body.reviewableBillingIds;
          if(!Array.isArray(active)||!Array.isArray(reviewable)||active.length>500||reviewable.length>500||active.some(x=>typeof x!=='string'||!BILLING.test(x))||reviewable.some(x=>typeof x!=='string'||!BILLING.test(x))||new Set(active).size!==active.length||new Set(reviewable).size!==reviewable.length||active.some(x=>!reviewable.includes(x))||(entitlement.body.subscribed!== (active.length>0)))throw Error('Invalid entitlement sources');
        }
      }
      docs=await Promise.all(questionIds.map(id=>questions.get(id)));
      if(docs.some(doc=>!doc))return{status:404,body:{error:'Question not found'}};
      if(docs.some((doc,i)=>doc.$id!==questionIds[i]))throw Error('Question mismatch');
      docs=docs.map(publicQuestion);
    }catch(_){return{status:503,body:{error:'Service unavailable'}};}
    if(entitlement.unavailable){
      // Do not grant paid or new free content on an unknown billing state, and
      // do not consume a student's quota. Previously free/legacy-granted items
      // can still be reviewed without consulting the payment provider.
      try{const previous=await usage.read(userId),state=previous===null?freshState():structuredClone(previous);if(!validState(state))throw Error('Invalid usage state');
        const results=[];for(let i=0;i<questionIds.length;i++)if(state.grantedIds.includes(questionIds[i]))results.push({question:docs[i],source:'review'});
        if(!results.length)return{status:503,body:{error:'Access verification unavailable',billingUnavailable:true}};
        return{status:200,body:{results,exhausted:results.length<questionIds.length,billingUnavailable:true,usage:summarizeUsage(state,now)}};
      }catch(_){return{status:503,body:{error:'Service unavailable'}};}
    }
    if(entitlement.body.subscribed){
      if(entitlement.body.admin===true)return{status:200,body:{results:docs.map(question=>({question,source:'paid'})),exhausted:false}};
      try{return await usage.transact(userId,async previous=>{
        const state=previous===null?freshState():structuredClone(previous);if(!validState(state))throw Error('Invalid usage state');
        for(const id of questionIds){
          if(state.grantedIds.includes(id))continue; // Free/legacy review is independent of payments.
          let grant=state.paidGrants.find(g=>g.questionId===id);
          if(!grant){if(state.paidGrants.length>=10000)throw Error('Usage state full');grant={questionId:id,sources:[]};state.paidGrants.push(grant);}
          for(const source of entitlement.body.activeBillingIds)if(!grant.sources.includes(source)){if(grant.sources.length>=25)throw Error('Too many sources');grant.sources.push(source);}
        }
        return{state,result:{status:200,body:{results:docs.map(question=>({question,source:'paid'})),exhausted:false}}};
      });}catch(_){return{status:503,body:{error:'Service unavailable'}};}
    }
    try{return await usage.transact(userId,async previous=>{
      const state=previous===null?freshState():structuredClone(previous);if(!validState(state))throw Error('Invalid usage state');
      const results=[];let exhausted=false;const reviewable=new Set(entitlement.body.reviewableBillingIds);
      for(let i=0;i<questionIds.length;i++){
        const decision=reviewOnly?(hasReviewGrant(state,questionIds[i],reviewable)?{source:'review'}:null):issueOne(state,questionIds[i],now,reviewable);
        if(decision)results.push({question:docs[i],...decision});else exhausted=true;
      }
      if(!results.length)return{state,result:reviewOnly?{status:403,body:{error:'No previously granted questions'}}:{status:429,body:{error:'Daily free allowance reached'}}};
      return{state,result:{status:200,body:{results,exhausted,usage:summarizeUsage(state,now)}}};
    });}catch(_){return{status:503,body:{error:'Service unavailable'}};}
  }
  async function getQuestion(userId,questionId){
    const result=await getQuestions(userId,[questionId]);
    if(result.status!==200)return result;
    return{status:200,body:result.body.results[0]};
  }

  async function reviewQuestions(userId,questionIds){return getQuestions(userId,questionIds,{reviewOnly:true});}
  return{status,startTrial,getQuestion,getQuestions,reviewQuestions};
}
module.exports={createQuestionAccess,publicMetadata,publicQuestion,constants:{FIRST_DAY,DAILY,TRIAL_LIMIT,TRIAL_MS}};
