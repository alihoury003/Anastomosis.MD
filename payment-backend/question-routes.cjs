'use strict';
function createQuestionRoutes({authenticate,access,questions}) {
  if(typeof authenticate!=='function'||!access||typeof access.getQuestion!=='function'||typeof access.getQuestions!=='function'||typeof access.reviewQuestions!=='function'||typeof access.startTrial!=='function'||!questions||typeof questions.listMetadata!=='function')throw Error('Question routes not configured');
  return async function route(req){
    const account=await authenticate(req.headers?.['x-appwrite-user-jwt']);
    if(account.status!==200)return{status:account.status===401?401:503,body:{error:account.status===401?'Sign in required':'Authentication unavailable'}};
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
