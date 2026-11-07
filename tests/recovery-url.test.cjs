#!/usr/bin/env node
// Exercise both recovery-page versions with a mock Appwrite client. No live
// email is sent and no credentials or real recovery tokens are used.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

async function loadPage(path, href, shouldFail = false) {
  const html = fs.readFileSync(path, 'utf8');
  const match = html.match(/<script type="module">([\s\S]*?)<\/script>/);
  assert.ok(match, `${path}: recovery module missing`);
  const moduleBody = match[1].replace(/^\s*import\s+\{\s*Client,\s*Account\s*\}\s+from\s+[^;]+;\s*/m, '');
  assert.ok(!moduleBody.includes('import { Client'), 'CDN import must be removed for mock');
  const calls = [];
  class Client { setEndpoint() { return this; } setProject() { return this; } }
  class Account {
    async deleteSession() {}
    async createRecovery(email, url) { calls.push({email, url}); if (shouldFail) throw new Error('mock transport failure'); }
  }
  const nodes = Object.create(null);
  for (const id of ['email','resetBtn','emailError','pwstep1','pwstep2']) {
    nodes[id] = {value: '', disabled: false, textContent: '', style: {}, classList: {add(){},remove(){}}};
  }
  nodes.email.value = 'test@example.invalid';
  const win = {location: {href}};
  const context = vm.createContext({window:win,document:{getElementById:id=>nodes[id],addEventListener(){}},Client,Account,URL,console:{error(){}}});
  await vm.runInContext(`(async () => { ${moduleBody} })()`, context);
  assert.equal(typeof win.handleReset, 'function');
  return {nodes, calls, handleReset:win.handleReset};
}

async function run() {
  const pages = ['forgot-password.html','domain-update/forgot-password.html'];
  const cases = [
    ['https://anastomosismd.com/forgot-password.html','https://anastomosismd.com/reset-password.html'],
    ['https://www.anastomosismd.com/forgot-password.html?campaign=example#section','https://www.anastomosismd.com/reset-password.html'],
    ['https://medchanic-md.appwrite.network/forgot-password.html','https://medchanic-md.appwrite.network/reset-password.html'],
    ['https://preview.example.invalid/forgot-password.html','https://preview.example.invalid/reset-password.html'],
  ];
  for (const page of pages) {
    for (const [href, expected] of cases) {
      const t = await loadPage(page, href);
      await t.handleReset();
      assert.deepEqual(t.calls, [{email:'test@example.invalid',url:expected}], `${page} ${href}`);
      assert.equal(t.nodes.pwstep2.style.display, 'block');
      console.log(`PASS ${page} → ${expected}`);
    }
    const bad = await loadPage(page, cases[0][0]);
    bad.nodes.email.value = 'invalid-email'; await bad.handleReset();
    assert.equal(bad.calls.length, 0, `${page}: invalid email must not send`);
    console.log(`PASS ${page}: invalid email blocked`);
    const fail = await loadPage(page, cases[0][0], true);
    await fail.handleReset();
    assert.equal(fail.nodes.pwstep2.style.display, 'block');
    console.log(`PASS ${page}: existing generic response preserved on mock failure`);
  }
  const auth = fs.readFileSync('auth.js','utf8');
  const body = auth.match(/export async function sendPasswordReset\(email\) \{([\s\S]*?)\n\}/);
  assert.ok(body, 'shared reset helper missing');
  for (const [href, expected] of cases.slice(0,3)) {
    const calls=[];const context=vm.createContext({window:{location:{href}},URL,account:{async createRecovery(email,url){calls.push({email,url})}}});
    const fn=vm.runInContext(`(async function(email){${body[1]}})`,context);
    await fn('test@example.invalid');assert.deepEqual(calls,[{email:'test@example.invalid',url:expected}]);
    console.log(`PASS auth.js → ${expected}`);
  }
  const reset = fs.readFileSync('reset-password.html','utf8');
  assert.ok(reset.includes('params.get("userId")') && reset.includes('params.get("secret")') && reset.includes('account.updateRecovery(userId, secret, password)'));
  console.log('PASS reset page retains Appwrite userId/secret handling');
}
run().catch(err=>{console.error(err);process.exitCode=1});
