'use strict';
function createQuestionRoutes({authenticate,access,questions,migrationCutoffMs=null}) {
  if(typeof authenticate!=='function'||!access||typeof access.getQuestion!=='function'||typeof access.getQuestions!=='function'||typeof access.reviewQuestions!=='function'||typeof access.status!=='function'||typeof access.startTrial!=='function'||!questions||typeof questions.listMetadata!=='function')throw Error('Question routes not configured');
  if(migrationCutoffMs!==null&&(!Number.isSafeInteger(migrationCutoffMs)||migrationCutoffMs<0))throw Error('Invalid migration cutoff');
  return async function route(req){
    const account=await authenticate(req.headers?.['x-appwrite-user-jwt']);
    if(account.status!==200)return{status:account.status===401?401:503,body:{error:account.status===401?'Sign in required':'Authentication unavailable'}};
    if(migrationCutoffMs!==null&&(!Number.isSafeInteger(account.createdAt)||account.createdAt<0))return{status:503,body:{error:'Account verification unavailable'}};
    if(req.path==='/status'&&req.method==='GET'){
      const snapshot=await access.status(account.userId);if(snapshot.status!==200)return snapshot;
      return{status:200,body:{...snapshot.body,migrationRequired:migrationCutoffMs!==null&&account.createdAt<=migrationCutoffMs&&snapshot.body?.usage?.legacyMigrationComplete!==true}};
    }
    if(migrationCutoffMs!==null&&account.createdAt<=migrationCutoffMs){
      const snapshot=await access.status(account.userId);if(snapshot.status!==200)return snapshot;
      if(snapshot.body?.usage?.legacyMigrationComplete!==true)return{status:423,body:{error:'Study history migration required'}};
    }
    if(req.path==='/catalog'&&req.method==='GET'){
      try{return{status:200,body:{questions:await questions.listMetadata()}};}catch(_){return{status:503,body:{error:'Question catalogue unavailable'}};}
    }
    if(req.path==='/trial'&&req.method==='POST')return access.startTrial(account.userId);
    if((req.path==='/question'||req.path==='/questions'||req.path==='/review')&&req.method==='POST'){
      let input;try{if(typeof req.bodyText!=='string'||Buffer.byteLength(req.bodyText,'utf8')>2048)throw Error('Invalid request');input=JSON.parse(req.bodyText);if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Invalid request');}catch(_){return{status:400,body:{error:'Invalid request'}};}
      return req.path==='/question'?access.getQuestion(account.userId,input.questionId):req.path==='/review'?access.reviewQuestions(account.userId,input.questionIds):access.getQuestions(account.userId,input.questionIds);
    }
    return{status:404,body:{error:'Not found'}};
  };
}
module.exports={createQuestionRoutes};
