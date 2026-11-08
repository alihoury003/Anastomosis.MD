'use strict';
// Offline planning only. Never accept these arguments from a browser. The
// snapshot must be captured by a trusted operator before public read is removed.
// Legacy preferences are user-editable; granting review access from them is an
// explicit grandfathering/business decision, NOT proof of previous use or payment.
const {summarizeLegacyHistory}=require('./legacy-history.cjs');
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/,DAY=86400000,MAX_IDS=10000;
function parseArray(value){
  if(value===undefined||value===null||value==='')return[];
  if(typeof value==='string'){if(Buffer.byteLength(value,'utf8')>2_000_000)throw Error('Snapshot too large');try{value=JSON.parse(value);}catch(_){throw Error('Invalid snapshot');}}
  if(!Array.isArray(value)||value.length>MAX_IDS)throw Error('Invalid snapshot');return value;
}
function dayKey(value){
  const s=String(value||'');if(!/^\d{8}$/.test(s))return null;
  const y=Number(s.slice(0,4)),m=Number(s.slice(4,6)),d=Number(s.slice(6,8)),ms=Date.UTC(y,m-1,d),check=new Date(ms);
  if(check.getUTCFullYear()!==y||check.getUTCMonth()!==m-1||check.getUTCDate()!==d)return null;
  return Math.floor(ms/DAY);
}
function integer(value){if(typeof value==='number'&&Number.isSafeInteger(value))return value;if(typeof value==='string'&&/^\d{1,16}$/.test(value)&&Number.isSafeInteger(Number(value)))return Number(value);return 0;}
function buildLegacyMigrationPlan({userId,accountCreatedAt,snapshotAt,cutoffAt,prefs,allowedQuestionIds,localQuestionIds=[],allowUnverifiedGrandfathering=false}){
  if(!ID.test(userId||'')||![accountCreatedAt,snapshotAt,cutoffAt].every(v=>Number.isSafeInteger(v)&&v>=0)||accountCreatedAt>snapshotAt||snapshotAt>cutoffAt||!prefs||typeof prefs!=='object'||!Array.isArray(allowedQuestionIds)||allowedQuestionIds.length>MAX_IDS||allowedQuestionIds.some(x=>typeof x!=='string'||!ID.test(x))||!Array.isArray(localQuestionIds)||localQuestionIds.length>100||localQuestionIds.some(x=>typeof x!=='string'||!ID.test(x)))throw Error('Invalid trusted snapshot');
  if(allowUnverifiedGrandfathering!==true)return{status:'approval_required',authorizationGranted:false};
  const allowed=new Set(allowedQuestionIds),local=new Set(localQuestionIds),candidates=[];
  const used=parseArray(prefs.used);for(const x of used)if(typeof x==='string'&&ID.test(x))candidates.push(x);
  const notebook=parseArray(prefs.notebook);for(const x of notebook)if(x&&typeof x.qid==='string'&&ID.test(x.qid))candidates.push(x.qid);
  const history=summarizeLegacyHistory(prefs.tests||[]);for(const test of history.records)candidates.push(...test.questionIds);
  const grantedIds=[...new Set(candidates)].filter(id=>allowed.has(id));if(grantedIds.length>MAX_IDS)throw Error('Snapshot too large');
  const snapshotDay=Math.floor(snapshotAt/DAY),storedDay=dayKey(prefs.freeDayKey);
  const activeDates=history.records.map(x=>Date.parse(x.finishedAt)).filter(x=>Number.isFinite(x)&&x<=snapshotAt).map(x=>Math.floor(x/DAY));
  const activity=parseArray(prefs.activityDates);for(const value of activity){if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))continue;const ts=Date.parse(value+'T00:00:00Z');if(Number.isFinite(ts)&&ts<=snapshotAt)activeDates.push(Math.floor(ts/DAY));}
  const previouslyUsed=grantedIds.length>0||integer(prefs.blocksUsed)>0||integer(prefs.freeUsedToday)>0;
  let firstFreeDay=null,lastFreeDay=null,freeUsedToday=0;
  if(previouslyUsed){
    firstFreeDay=activeDates.length?Math.min(...activeDates):storedDay!==null&&storedDay<=snapshotDay?storedDay:Math.max(0,snapshotDay-1);
    firstFreeDay=Math.min(firstFreeDay,snapshotDay);lastFreeDay=snapshotDay;
    const limit=firstFreeDay===snapshotDay?40:10;
    freeUsedToday=storedDay===snapshotDay?Math.min(limit,Math.max(0,integer(prefs.freeUsedToday))):0;
  }
  const requestedEnd=integer(prefs.trialEndsAt),trialEndsAt=requestedEnd?Math.min(requestedEnd,snapshotAt+7*DAY):0;
  const trialStartedAt=trialEndsAt?Math.max(0,trialEndsAt-7*DAY):null;
  const trialUsed=trialStartedAt===null?0:Math.min(150,Math.max(0,integer(prefs.trialQuestionsUsed)));
  const state={version:1,legacyMigrationComplete:true,firstFreeDay,lastFreeDay,freeUsedToday,trialStartedAt,trialUsed,grantedIds};
  return{status:'approved_snapshot',userId,state,source:'legacy-unverified',unknownQuestionReferences:new Set(candidates.filter(id=>!allowed.has(id)&&!local.has(id))).size,skippedLegacyBlocks:history.skipped,trialEndCapped:requestedEnd>trialEndsAt&&trialEndsAt>0,authorizationGrantedFromPaidPrefs:false};
}
function createLegacyMigrationWriter({tables,databaseId,tableId}){
  if(!tables||typeof tables.createRow!=='function'||typeof tables.getRow!=='function'||!ID.test(databaseId||'')||!ID.test(tableId||''))throw Error('Migration store not configured');
  return async function write(plan){
    if(!plan||plan.status!=='approved_snapshot'||!ID.test(plan.userId||'')||plan.source!=='legacy-unverified'||!plan.state||plan.state.version!==1)throw Error('Invalid migration plan');
    const stateJson=JSON.stringify(plan.state);if(stateJson.length>700000)throw Error('Migration state too large');
    try{await tables.createRow({databaseId,tableId,rowId:plan.userId,data:{stateJson},permissions:[]});return'stored';}
    catch(e){
      if(e?.code!==409||!['row_already_exists','document_already_exists'].includes(e.type))throw Error('Migration write failed');
      try{const current=await tables.getRow({databaseId,tableId,rowId:plan.userId});if(!current||current.$id!==plan.userId||typeof current.stateJson!=='string')throw Error('Invalid existing state');const state=JSON.parse(current.stateJson);return state?.legacyMigrationComplete===true?'already_exists':'conflict_needs_review';}
      catch(_){throw Error('Migration verification failed');}
    }
  };
}
module.exports={buildLegacyMigrationPlan,createLegacyMigrationWriter};
