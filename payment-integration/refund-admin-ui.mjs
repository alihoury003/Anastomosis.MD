import {Client,Account,Functions} from 'https://cdn.jsdelivr.net/npm/appwrite@16/+esm';
import {SECURE_CONFIG} from './secure-config.mjs';
import {createRefundAdminClient} from './browser-refund-admin.mjs';
import {createCatalogPreflightClient} from './browser-catalog-preflight.mjs';
const message=document.getElementById('message'),list=document.getElementById('reviews'),refresh=document.getElementById('refresh'),catalogButton=document.getElementById('checkCatalog'),catalogReport=document.getElementById('catalogReport');
let reviewClient=null,catalogCheck=null,busy=false;
function show(text){message.textContent=text;}
function addDetail(container,label,value){const row=document.createElement('div');const name=document.createElement('strong');name.textContent=label+': ';row.append(name,document.createTextNode(value||'—'));container.append(row);}
async function load(){
  if(!reviewClient||busy)return;busy=true;refresh.disabled=true;show('Loading reviews…');list.replaceChildren();
  try{
    const records=await reviewClient.list();if(!records.length){show('No pending payment reviews.');return;}
    show(records.length===25?'Showing up to 25 pending reviews. Resolve and refresh to see more.':`${records.length} pending review${records.length===1?'':'s'}.`);
    for(const record of records){
      const card=document.createElement('article');card.className='case';const heading=document.createElement('h2');heading.textContent=record.action+' · '+(record.adjustmentType||'adjustment');card.append(heading);
      const details=document.createElement('div');details.className='details';addDetail(details,'Adjustment',record.adjustmentId);addDetail(details,'Billing source',record.billingId);addDetail(details,'Account ID',record.userId);addDetail(details,'Paddle status',record.paddleStatus);addDetail(details,'Updated',record.updatedAt);card.append(details);
      const actions=document.createElement('div');actions.className='actions';
      for(const [decision,label] of [['allow','Allow this billing source'],['restrict','Restrict this billing source']]){
        const button=document.createElement('button');button.type='button';button.textContent=label;if(decision==='restrict')button.className='secondary';
        button.addEventListener('click',async()=>{if(busy||!window.confirm(`${label}? This changes access only, not the Paddle refund.`))return;busy=true;refresh.disabled=true;for(const b of actions.querySelectorAll('button'))b.disabled=true;show('Saving the access decision…');try{await reviewClient.decide({adjustmentId:record.adjustmentId,expectedUpdatedAt:record.updatedAt,decision});busy=false;await load();}catch(error){busy=false;refresh.disabled=false;for(const b of actions.querySelectorAll('button'))b.disabled=false;show(error?.status===409?'This adjustment changed. Wait for Paddle to sync, then refresh.':'Could not save the decision. Please try again.');}});
        actions.append(button);
      }
      card.append(actions);list.append(card);
    }
  }catch(error){show(error?.status===403?'This account is not authorized to review payments.':'Could not load reviews. Please try again.');}
  finally{busy=false;refresh.disabled=false;}
}
async function checkCatalog(){
  if(!catalogCheck)return;catalogButton.disabled=true;catalogReport.replaceChildren();catalogReport.textContent='Checking catalog…';
  try{const report=await catalogCheck();catalogReport.replaceChildren();const heading=document.createElement('p');heading.textContent=report.catalogReady?'Price configuration passed. Checkout and launch still require full testing.':'Price configuration is incomplete or mismatched.';catalogReport.append(heading);
    for(const row of report.plans){const line=document.createElement('p'),d=row.discount;line.textContent=`${row.plan}: one-time ${row.oneTime?'OK':'needs attention'}, recurring ${row.recurring?'OK':'needs attention'}; discount ${!d?'not verified':!d.configurationMatches?'configuration mismatch':d.expired?'expired':d.exhausted?'exhausted':!d.oneTime||!d.recurring?'not valid for both prices':d.alsoAppliesToOtherPlans?'valid but also applies to other plans':'OK'}.`;catalogReport.append(line);}
  }catch(_){catalogReport.textContent='Could not check catalog. Try again or check permissions.';}finally{catalogButton.disabled=false;}
}
if(!SECURE_CONFIG.enabled||!SECURE_CONFIG.refundAdminFunctionId){show('Payment reviews are not configured.');}
else{
  try{const client=new Client().setEndpoint('https://nyc.cloud.appwrite.io/v1').setProject('6a427cd000140ae72eb1'),account=new Account(client);await account.get();const functions=new Functions(client);reviewClient=createRefundAdminClient({account,functions,functionId:SECURE_CONFIG.refundAdminFunctionId});if(SECURE_CONFIG.catalogPreflightFunctionId){catalogCheck=createCatalogPreflightClient({account,functions,functionId:SECURE_CONFIG.catalogPreflightFunctionId});catalogButton.disabled=false;catalogButton.addEventListener('click',checkCatalog);}refresh.addEventListener('click',load);await load();}
  catch(_){show('Sign in with the authorized admin account, then reload this page.');}
}
