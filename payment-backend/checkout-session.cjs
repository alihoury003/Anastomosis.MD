'use strict';
const { createBinding } = require('./checkout-binding.cjs');
const { createAppwriteAuthenticator } = require('./appwrite-auth.cjs');
const { isValidPrice } = require('./price-policy.cjs');
// Authenticated server route. The Appwrite account endpoint is the authority
// for identity. The Paddle API independently verifies the configured price.
function checkoutSessionService({endpoint, projectId, environment, priceIds, productId, paddle, bindingKey, fetchImpl = globalThis.fetch}) {
  if (endpoint !== 'https://nyc.cloud.appwrite.io/v1' || typeof projectId !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/.test(projectId) ||
      !['sandbox','live'].includes(environment) || !Buffer.isBuffer(bindingKey) || bindingKey.length < 32 ||
      !priceIds || typeof priceIds !== 'object' || !/^pro_[a-z0-9]{26}$/.test(productId||'') ||
      !paddle || typeof paddle.getPrice!=='function' || typeof fetchImpl !== 'function') throw Error('Checkout not configured');
  const authenticate = createAppwriteAuthenticator({endpoint, projectId, fetchImpl});
  return async function createSession({jwt, plan, autoRenew}) {
    if (typeof jwt !== 'string' || jwt.length < 20 || jwt.length > 10000) return {status:401, body:{error:'Sign in required'}};
    if (!['monthly','threeMonth','annual'].includes(plan) || typeof autoRenew !== 'boolean') return {status:400, body:{error:'Invalid plan'}};
    const priceId=priceIds[plan]?.[autoRenew?'recurring':'oneTime'];
    if (typeof priceId !== 'string' || !/^pri_[a-z0-9]{26}$/.test(priceId)) return {status:503, body:{error:'Plan unavailable'}};
    const account = await authenticate(jwt);
    if (account.status === 401) return {status:401, body:{error:'Sign in required'}};
    if (account.status !== 200) return {status:503, body:{error:'Authentication unavailable'}};
    let price;
    try { price=await paddle.getPrice(priceId); } catch (_) { return {status:503, body:{error:'Plan unavailable'}}; }
    if (!price || price.id!==priceId || !isValidPrice({price,plan,autoRenew,productId})) return {status:503, body:{error:'Plan unavailable'}};
    let binding;
    try { binding = createBinding({userId:account.userId,priceId,environment,autoRenew},bindingKey); }
    catch (_) { return {status:503, body:{error:'Authentication unavailable'}}; }
    return {status:200, body:{priceId,customData:{anastomosis_binding:binding}}};
  };
}
module.exports = { checkoutSessionService };
