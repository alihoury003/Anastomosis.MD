// Staged adapter for the existing dashboard's questionBank. It is NOT imported
// by the live dashboard; it intentionally does not touch exam-page DOM/CSS.
// Historical-score migration, quota UX, loading state and actual dashboard
// wiring remain unresolved and must be completed before deployment.
const ID=/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;
export function createDashboardBridge({gateway,questionBank,unpackQuestion}) {
  if(!gateway||!['catalog','questions','review'].every(k=>typeof gateway[k]==='function')||!Array.isArray(questionBank)||typeof unpackQuestion!=='function')throw Error('Dashboard bridge not configured');
  function placeholder(meta){
    return{id:meta.id,subject:meta.subject||'Miscellaneous',system:meta.system||'Miscellaneous (Multisystem)',topic:meta.topic||'Miscellaneous',difficulty:meta.difficulty||2,stem:'',rawStem:'',question:'Question available in a block',correct:null,choices:[],cards:[],used:false,_remote:true,_loaded:false};
  }
  async function loadCatalog(){
    const metadata=await gateway.catalog();if(!Array.isArray(metadata)||metadata.length>10000)throw Error('Invalid catalogue');
    const known=new Set(questionBank.map(q=>q.id)),seen=new Set(),additions=[];
    for(const item of metadata){if(!item||!ID.test(item.id||'')||seen.has(item.id))throw Error('Invalid catalogue');seen.add(item.id);if(known.has(item.id))continue;additions.push(placeholder(item));known.add(item.id);}
    questionBank.push(...additions);return{added:additions.length};
  }
  async function hydrate(ids,reviewOnly){
    if(!Array.isArray(ids)||ids.length<1||ids.length>20||ids.some(id=>typeof id!=='string'||!ID.test(id))||new Set(ids).size!==ids.length)throw Error('Invalid question selection');
    const byId=new Map(questionBank.map(q=>[q.id,q]));if(ids.some(id=>!byId.has(id)))throw Error('Question not in catalogue');
    const remote=ids.filter(id=>byId.get(id)._remote===true);
    if(!remote.length)return{questions:ids.map(id=>byId.get(id)),limited:false};
    const response=await (reviewOnly?gateway.review(remote):gateway.questions(remote));
    if(!response||!Array.isArray(response.results)||typeof response.exhausted!=='boolean')throw Error('Invalid question response');
    const decoded=new Map();
    // Prepare everything before mutating questionBank; fail without partial edits.
    for(const item of response.results){const id=item?.question?.$id;if(!remote.includes(id)||decoded.has(id))throw Error('Invalid question response');const q=unpackQuestion(item.question);if(!q||q.id!==id)throw Error('Invalid question response');decoded.set(id,{...q,_remote:true,_loaded:true});}
    const replacements=[...decoded].map(([id,q])=>({index:questionBank.findIndex(old=>old.id===id),q}));
    if(replacements.some(r=>r.index<0))throw Error('Question catalogue changed');
    for(const item of replacements)questionBank[item.index]=item.q;
    const selected=ids.filter(id=>!byId.get(id)._remote||decoded.has(id)).map(id=>decoded.get(id)||byId.get(id));
    return{questions:selected,limited:response.exhausted||selected.length<ids.length,usage:response.usage||null};
  }
  return{loadCatalog,loadBlock:ids=>hydrate(ids,false),loadReview:ids=>hydrate(ids,true)};
}
