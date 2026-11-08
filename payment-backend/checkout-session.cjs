'use strict';
const { createBinding } = require('./checkout-binding.cjs');
const { createAppwriteAuthenticator } = require('./appwrite-auth.cjs');

// Use only in an authenticated server route. The Appwrite account endpoint is
// the authority for identity; user IDs and e-mails supplied by clients are ignored.
function checkoutSessionService({endpoint, projectId, environment, priceIds, bindingKey, fetchImpl = globalThis.fetch}) {
  if (endpoint !== 'https://nyc.cloud.appwrite.io/v1' || typeof projectId !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/.test(projectId) ||
      !['sandbox','live'].includes(environment) || !Buffer.isBuffer(bindingKey) || bindingKey.length < 32 ||
      !priceIds || typeof priceIds !== 'object' || typeof fetchImpl !== 'function') throw Error('Checkout not configured');
  const authenticate = createAppwriteAuthenticator({endpoint, projectId, fetchImpl});
  return async function createSession({jwt, plan, autoRenew}) {
    if (typeof jwt !== 'string' || jwt.length < 20 || jwt.length > 10000) return {status:401, body:{error:'Sign in required'}};
    if (!['monthly','threeMonth','annual'].includes(plan) || typeof autoRenew !== 'boolean' ||
        typeof priceIds[plan] !== 'string' || !/^pri_[a-z0-9]{26}$/.test(priceIds[plan])) return {status:400, body:{error:'Invalid plan'}};
    const account = await authenticate(jwt);
    if (account.status === 401) return {status:401, body:{error:'Sign in required'}};
    if (account.status !== 200) return {status:503, body:{error:'Authentication unavailable'}};
    let binding;
    try { binding = createBinding({userId:account.userId,priceId:priceIds[plan],environment,autoRenew},bindingKey); }
    catch (_) { return {status:503, body:{error:'Authentication unavailable'}}; }
    return {status:200, body:{priceId:priceIds[plan],customData:{anastomosis_binding:binding}}};
  };
}
module.exports = { checkoutSessionService };
