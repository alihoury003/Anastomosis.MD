#!/usr/bin/env python3
"""Build a DISABLED candidate from main's pinned dashboard. Never deploy as-is."""
from pathlib import Path
import subprocess
import shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
raw=subprocess.check_output(['git','show','2d8d0d0:dashboard.html'],cwd=ROOT).decode('utf-8')
text=raw

def once(old,new):
    global text
    count=text.count(old)
    if count!=1: raise RuntimeError(f'Expected one occurrence, got {count}: {old[:120]!r}')
    text=text.replace(old,new,1)

def between(start,end,replacement):
    global text
    a=text.find(start)
    if a<0 or text.find(start,a+1)>=0: raise RuntimeError(f'Bad start {start!r}')
    b=text.find(end,a)
    if b<0: raise RuntimeError(f'Bad end {end!r}')
    text=text[:a]+replacement+text[b:]

once('import { Client, Account, Databases, ID, Query, Functions } from "https://cdn.jsdelivr.net/npm/appwrite@16/+esm";', '''import { Client, Account, Databases, ID, Query, Functions } from "https://cdn.jsdelivr.net/npm/appwrite@16/+esm";
import {createGateway} from "./browser-gateway.mjs";
import {createDashboardBridge} from "./dashboard-bridge.mjs";
import {createCheckoutUI} from "./checkout-ui.mjs";
import {SECURE_CONFIG} from "./secure-config.mjs";''')
once('      <div class="trial-strip" id="trialStrip" style="display:none"></div>', '''      <div class="trial-strip" id="trialStrip" style="display:none"></div>
      <div id="secureAdjustmentNotice" role="status" hidden style="margin:10px 0;padding:10px 12px;border-left:3px solid #B5342A;color:#101418;font-size:13px">A payment adjustment is under review. If access looks incorrect, <a href="mailto:anastomosis.md@gmail.com">contact support</a>.</div>''')
once('    <button class="paywall-cta" id="subscribeBtn" onclick="handleSubscribeClick()">Subscribe with card</button>', '''    <label id="secureRenewalOption" hidden style="display:none;margin:10px 0;color:var(--ink-2);font-size:13px;line-height:1.45"><input id="secureAutoRenew" type="checkbox"> Auto-renew my access. Leave unchecked for one payment only.</label>
    <button class="paywall-cta" id="subscribeBtn" onclick="handleSubscribeClick()">Subscribe with card</button>''')
once("const _functions = new Functions(_client);", '''const _functions = new Functions(_client);
let secureGateway=null, secureBridge=null, secureUsage=null, secureCheckoutUI=null, secureStartPending=false, secureNavigationPending=false, secureReviewNoticeShown=false;
function initSecureIntegration() {
  if (!SECURE_CONFIG.enabled) return;
  secureGateway=createGateway({account:_account,functions:_functions,questionFunctionId:SECURE_CONFIG.questionFunctionId,checkoutFunctionId:SECURE_CONFIG.checkoutFunctionId,accessFunctionId:SECURE_CONFIG.accessFunctionId,priceIds:SECURE_CONFIG.priceIds});
  secureBridge=createDashboardBridge({gateway:secureGateway,questionBank,unpackQuestion});
  const option=$('secureRenewalOption'); if(option){option.hidden=false;option.style.display='block';}
  const check=$('secureAutoRenew'); if(check)check.addEventListener('change',()=>loadPaddlePrices());
}
function applySecureUsage(usage) {
  if(!usage || !Number.isInteger(usage.freeRemaining) || typeof usage.trialActive!=='boolean') throw Error('Usage unavailable');
  secureUsage=usage;trialEndsAt=usage.trialEndsAt||0;trialQuestionsUsed=usage.trialUsed||0;
}
async function refreshSecureStatus(){const snapshot=await secureGateway.questionStatus();isSubscribed=snapshot.subscribed;applySecureUsage(snapshot.usage);renderTrialStrip();const notice=$('secureAdjustmentNotice');if(notice)notice.hidden=!snapshot.reviewPending;if(snapshot.reviewPending&&!secureReviewNoticeShown){secureReviewNoticeShown=true;showToast('A payment adjustment is under review. Contact support if access looks incorrect.');}return snapshot;}
async function secureHydrate(ids,reviewOnly=false){
  const result=await (reviewOnly?secureBridge.loadReview(ids):secureBridge.loadBlock(ids));
  if(result.usage){isSubscribed=false;applySecureUsage(result.usage);renderTrialStrip();}
  if(result.limited)showToast(reviewOnly?'Some older questions need migration.':'The block was shortened to your available allowance.');
  if(!result.questions.length)throw Error('No questions available');
  return result;
}
async function secureReviewHistory(ids){
  const unique=[...new Set(ids)];const questions=[];
  for(let offset=0;offset<unique.length;offset+=20){const r=await secureBridge.loadReview(unique.slice(offset,offset+20));if(r.limited)throw Error('Historical question migration incomplete');questions.push(...r.questions);}
  return{questions,limited:false};
}
async function hydrateSavedHistory(){
  const refs=new Set();
  for(const t of pastTests)for(const id of (Array.isArray(t.qIds)?t.qIds:[]))if(t.answers?.[id]&&qById(id))refs.add(id);
  for(const item of notebookItems)if(qById(item?.qid))refs.add(item.qid);
  const required=[...refs];
  for(let offset=0;offset<required.length;offset+=20){
    const sub=$('bootSub');if(sub)sub.textContent=`Restoring study history: ${Math.min(offset+20,required.length)} of ${required.length}`;
    const result=await secureBridge.loadReview(required.slice(offset,offset+20));
    if(result.limited)throw Error('Historical question migration incomplete');
  }
  // Previously used but unanswered IDs may not have been opened. Retrieve only
  // those already granted, without allocating quota for omitted questions.
  const optional=[...usedQuestionIds].filter(id=>!refs.has(id)&&qById(id));
  for(let offset=0;offset<optional.length;offset+=20){
    try{await secureBridge.loadReview(optional.slice(offset,offset+20));}catch(err){if(err?.status!==403)throw err;}
  }
}''')
once("async function listAllQuestionDocs() {\n  const limit = 1000;", """async function listAllQuestionDocs() {
  if (SECURE_CONFIG.enabled) {
    if(!currentUser || currentUser.email.toLowerCase()!==ADMIN_EMAIL.toLowerCase())throw Error('Admin access required');
    const all=[];let offset=0;
    while(true){const result=await _databases.listDocuments(APPWRITE_DB_ID,APPWRITE_COL_ID,[Query.limit(1000),Query.offset(offset)]);all.push(...result.documents);if(!result.documents.length||result.documents.length<1000||all.length>=result.total)break;offset+=result.documents.length;}
    return all;
  }
  const limit = 1000;""")
once('async function loadDatabaseQuestions() {\n  try {', '''async function loadDatabaseQuestions() {
  if(SECURE_CONFIG.enabled){await secureBridge.loadCatalog();return;}
  try {''')
once("document.addEventListener('DOMContentLoaded', async () => {\n  try {", "document.addEventListener('DOMContentLoaded', async () => {\n  if(!SECURE_CONFIG.enabled){const sub=$('bootSub');if(sub)sub.textContent='Secure upgrade is not configured.';return;}\n  try {")
once('    await loadUserData();\n    await loadSubscriptionState();', '''    await loadUserData();
    if(SECURE_CONFIG.enabled){
      initSecureIntegration();
      const preflight=await secureGateway.questionStatus();
      if(preflight.migrationRequired){const sub=$('bootSub');if(sub)sub.textContent='Your previous study history needs a safe migration before the upgrade.';return;}
    }
    await loadSubscriptionState();
    if(SECURE_CONFIG.enabled){await loadDatabaseQuestions();await hydrateSavedHistory();}''')
once("    loadDatabaseQuestions().then(() => {", "    const refreshQuestionViews=() => {")
once("    });\n  } catch (err) {\n    const sub = $('bootSub');", "    };\n    if(SECURE_CONFIG.enabled)refreshQuestionViews();else loadDatabaseQuestions().then(refreshQuestionViews);\n  } catch (err) {\n    const sub = $('bootSub');")
once("    const sub = $('bootSub'); if (sub) sub.textContent = 'Redirecting to login';\n    window.location.href = 'login.html';", """    const sub = $('bootSub');
    if(currentUser&&SECURE_CONFIG.enabled){if(sub)sub.textContent='The secure upgrade is unavailable. Please contact support.';return;}
    if(sub)sub.textContent='Redirecting to login';window.location.href='login.html';""")
legacy_gate='  if (!isSubscribed && freeAccessExpired()) { showPaywall(); return; }'
if text.count(legacy_gate)!=2: raise RuntimeError('Unexpected block access gates')
text=text.replace(legacy_gate, '  if (!SECURE_CONFIG.enabled && !isSubscribed && freeAccessExpired()) { showPaywall(); return; }', 2)
once('function generateTest() {', 'async function generateTest() {')
once("  const chosen = [...pool].sort(() => Math.random() - 0.5).slice(0, n);", "  let chosen = [...pool].sort(() => Math.random() - 0.5).slice(0, n);")
once('  activeBlock = newBlock(chosen, `${subjLabel}${statusLabel}`);', '''  if(SECURE_CONFIG.enabled){if(secureStartPending)return;secureStartPending=true;try{chosen[0]=(await secureHydrate([chosen[0].id])).questions[0];}catch(err){if(err?.status===429)showPaywall();else showToast('Could not load this question.');return;}finally{secureStartPending=false;}}
  if(!chosen.length)return;
  activeBlock = newBlock(chosen, `${subjLabel}${statusLabel}`);''')
once("function startBlockFromIds(ids, title = 'Custom Review') {", "async function startBlockFromIds(ids, title = 'Custom Review') {")
once("  const chosen = [...new Set(ids)].map(id => qById(id)).filter(Boolean).sort(() => Math.random() - 0.5).slice(0, 20);\n  activeBlock = newBlock(chosen, title);", """  let chosen = [...new Set(ids)].map(id => qById(id)).filter(Boolean).sort(() => Math.random() - 0.5).slice(0, 20);
  if(SECURE_CONFIG.enabled){if(secureStartPending)return;secureStartPending=true;try{chosen[0]=(await secureHydrate([chosen[0].id])).questions[0];}catch(err){if(err?.status===429)showPaywall();else showToast('Could not load this question.');return;}finally{secureStartPending=false;}}
  if(!chosen.length)return;
  activeBlock = newBlock(chosen, title);""")
once("function reviewNotebookQuestion(qid) {\n  activeBlock", """async function reviewNotebookQuestion(qid) {
  if(SECURE_CONFIG.enabled){try{const r=await secureHydrate([qid],true);if(r.limited)return;}catch(_){showToast('This previous question needs migration.');return;}}
  activeBlock""")
once("function reviewTest(idx) { const t = pastTests[idx]; activeBlock", """async function reviewTest(idx) { const t = pastTests[idx]; if(SECURE_CONFIG.enabled){try{const answered=(t.qIds||[]).filter(id=>t.answers?.[id]);if(answered.length)await secureReviewHistory(answered);}catch(_){showToast('This previous block needs migration.');return;}} activeBlock""")
once("function resumeTest(idx) { const t = pastTests[idx]; activeBlock", """async function resumeTest(idx) { const t = pastTests[idx]; if(SECURE_CONFIG.enabled){try{const target=(t.qIds||[])[Math.min(t.current||0,(t.qIds||[]).length-1)];await secureHydrate([target]);}catch(err){if(err?.status===429)showPaywall();else showToast('Could not load this question.');return;}} activeBlock""")
once('  let usedChanged = false; activeBlock.qIds.forEach(qid => { if (!usedQuestionIds.has(qid)) { usedQuestionIds.add(qid); usedChanged = true; } }); if (usedChanged) saveUserUsed();', '  let usedChanged = false; activeBlock.qIds.forEach(qid => { const q=qById(qid); if(SECURE_CONFIG.enabled && q?._remote && !q._loaded)return; if (!usedQuestionIds.has(qid)) { usedQuestionIds.add(qid); usedChanged = true; } }); if (usedChanged) saveUserUsed();')
once('function freeQuestionsLeftToday() {\n  return Math.max', 'function freeQuestionsLeftToday() {\n  if(SECURE_CONFIG.enabled)return secureUsage?.freeRemaining ?? 0;\n  return Math.max')
once('function countFreeQuestion() {\n  freeUsedToday += 1;', '''function countFreeQuestion() {
  if(SECURE_CONFIG.enabled)return; // Server reserves question exposure atomically.
  freeUsedToday += 1;''')
once('  function freeAccessExpired() {\n    if (FREE_TRIAL_DAYS', '''  function freeAccessExpired() {
    if(SECURE_CONFIG.enabled){if(activeBlock?.isNew)return false;return !secureUsage?.trialActive && (secureUsage?.freeRemaining ?? 0)<=0;}
    if (FREE_TRIAL_DAYS''')
once('    const trialRunning = FREE_TRIAL_DAYS > 0 && trialEndsAt && Date.now() <= trialEndsAt;', '    const trialRunning = SECURE_CONFIG.enabled ? !!secureUsage?.trialActive : FREE_TRIAL_DAYS > 0 && trialEndsAt && Date.now() <= trialEndsAt;')
once('      const dayOne = !(blocksUsed > 0 || freeUsedToday > 0);', '      const dayOne = SECURE_CONFIG.enabled ? !!secureUsage?.firstFreeDay : !(blocksUsed > 0 || freeUsedToday > 0);')
once('  async function startFreeTrial() {\n    if (isSubscribed)', '''  async function startFreeTrial() {
    if(SECURE_CONFIG.enabled){if(isSubscribed){showToast('You are already subscribed.');return;}try{const result=await secureGateway.startTrial();if(result.usage)applySecureUsage(result.usage);renderTrialStrip();showToast('Free trial started.');}catch(err){showToast(err?.status===409?'Your trial has already been used.':'Could not start the trial.');}return;}
    if (isSubscribed)''')
once('async function loadSubscriptionState() {\n  try { const prefs', '''async function loadSubscriptionState() {
  if(SECURE_CONFIG.enabled){const prefs=await _account.getPrefs();blocksUsed=parseInt(prefs.blocksUsed||'0',10)||0;await refreshSecureStatus();return;}
  try { const prefs''')
once("async function saveSubscriptionState() { try { const prefs", "async function saveSubscriptionState() { if(SECURE_CONFIG.enabled)return; try { const prefs")
once('async function loadPaddlePrices() {\n  const fallback', '''async function loadPaddlePrices() {
  const displayPrices=SECURE_CONFIG.enabled?Object.fromEntries(Object.entries(SECURE_CONFIG.priceIds).map(([k,v])=>[k,$('secureAutoRenew')?.checked?v.recurring:v.oneTime])):PADDLE_PRICES;
  const fallback''')
# Restrict replacements to the price-preview function only.
start=text.index('async function loadPaddlePrices() {');end=text.index('function showPaywall()',start)
chunk=text[start:end].replace('[PADDLE_PRICES.monthly, PADDLE_PRICES.threeMonth, PADDLE_PRICES.annual]', '[displayPrices.monthly, displayPrices.threeMonth, displayPrices.annual]').replace('byPrice[PADDLE_PRICES[plan]]','byPrice[displayPrices[plan]]')
text=text[:start]+chunk+text[end:]
once('function handleSubscribeClick(plan = selectedPlan) {\n  if (!currentUser)', '''async function handleSubscribeClick(plan = selectedPlan) {
  if(SECURE_CONFIG.enabled){
    if(!currentUser||!initPaddle()){showToast('Checkout is unavailable.');return;}
    try{secureCheckoutUI ||= createCheckoutUI({gateway:secureGateway,paddle:window.Paddle});await secureCheckoutUI.open(plan,{autoRenew:!!$('secureAutoRenew')?.checked,discountCode:$('promoInput')?.value.trim().toUpperCase()||''});}catch(_){showToast('Checkout is unavailable. Please try again.');}return;
  }
  if (!currentUser)''')
# Preserve the exam markup and renderer. Intercept only navigation before a
# not-yet-seen question is displayed, pause the clock during network loading,
# and keep the prior question visible until the new one is authorized.
once('/* ===================== EXPOSE TO GLOBAL SCOPE ===================== */', """/* Secure access adapter: original exam markup and renderer are unchanged. */
if(SECURE_CONFIG.enabled){
  const originalGoToItem=goToItem;
  goToItem=function(idx){
    if(secureNavigationPending)return;
    if(!activeBlock||idx<0||idx>=activeBlock.qIds.length||idx===current)return originalGoToItem(idx);
    const question=qById(activeBlock.qIds[idx]);
    if(!question||!question._remote||question._loaded)return originalGoToItem(idx);
    const block=activeBlock, priorIndex=current, screen=$('screen-block'), previousInert=!!screen?.inert;
    secureNavigationPending=true;if(screen)screen.inert=true;
    if(block.isNew){trackCurrentQuestionTime();clearInterval(timerInterval);}
    showToast('Loading question…');let failure=null;
    return secureHydrate([question.id]).then(()=>{
      if(activeBlock!==block||current!==priorIndex)return;
      if(block.isNew)block.itemStartedAt=Date.now();
      originalGoToItem(idx);
    }).catch(err=>{failure=err;}).finally(()=>{
      secureNavigationPending=false;if(screen)screen.inert=previousInert;
      if(activeBlock===block&&block.isNew){block.itemStartedAt=Date.now();startBlockTimer();}
      if(failure){if(failure.status===429)showPaywall();else showToast('Could not load this question. Try again.');}
    });
  };
  document.addEventListener('keydown',event=>{if(secureNavigationPending){event.preventDefault();event.stopImmediatePropagation();}},true);
}
/* ===================== EXPOSE TO GLOBAL SCOPE ===================== */""")
# The secure path must never treat the browser event itself as paid entitlement.
once("eventCallback: function (data) { if (data && data.name === 'checkout.completed') { alert('Payment completed. Your access will activate once payment confirmation is processed. If it does not unlock shortly, refresh once or contact support.'); } }", "eventCallback: function (data) { if (data && data.name === 'checkout.completed') { if(SECURE_CONFIG.enabled){showToast('Payment submitted. Checking account access.');refreshSecureStatus().then(()=>{if(isSubscribed)showToast('Your access is active.');else showToast('Payment is being confirmed. Refresh later or contact support.');}).catch(()=>showToast('Payment is being confirmed. Refresh later or contact support.'));}else alert('Payment completed. Your access will activate once payment confirmation is processed. If it does not unlock shortly, refresh once or contact support.'); } }")
(OUT/'dashboard.html').write_text(text,encoding='utf-8')
for name in ('browser-gateway.mjs','dashboard-bridge.mjs','checkout-ui.mjs','browser-refund-admin.mjs','browser-catalog-preflight.mjs'):
    shutil.copyfile(ROOT/'payment-backend'/name,OUT/name)
print('Built disabled candidate dashboard from pinned main commit 2d8d0d0')
