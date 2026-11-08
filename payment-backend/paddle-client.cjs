'use strict';
// Server-side read-only Paddle adapter. No account, catalog or subscription
// changes. Credentials must only come from private server configuration.
const ID = /^sub_[a-z0-9]{26}$/;
function createPaddleClient({environment, apiKey, fetchImpl=globalThis.fetch, allowCancellation=false}) {
  if (!['sandbox','live'].includes(environment) || typeof apiKey !== 'string' || !apiKey || typeof fetchImpl !== 'function') throw Error('Paddle client not configured');
  const origin = environment === 'sandbox' ? 'https://sandbox-api.paddle.com' : 'https://api.paddle.com';
  async function read(url) {
    const parsed = new URL(url);
    if (parsed.origin !== origin || !['/adjustments'].includes(parsed.pathname) && !/^\/subscriptions\/sub_[a-z0-9]{26}$/.test(parsed.pathname)) throw Error('Invalid Paddle URL');
    const response = await fetchImpl(parsed.href, {method:'GET',redirect:'error',headers:{authorization:`Bearer ${apiKey}`,'accept':'application/json','skip-count':'true'},signal:AbortSignal.timeout(4000)});
    if (!response.ok) throw Error('Paddle request failed');
    const body=await response.json();
    if (!body || typeof body !== 'object') throw Error('Invalid Paddle response');
    return body;
  }
  async function getSubscription(id) {
    if (!ID.test(id || '')) throw Error('Invalid subscription ID');
    const body=await read(`${origin}/subscriptions/${id}`);
    if (!body.data || body.data.id !== id) throw Error('Invalid Paddle response');
    return body.data;
  }
  async function listAdjustments(id) {
    if (!ID.test(id || '')) throw Error('Invalid subscription ID');
    const first=new URL(`${origin}/adjustments`);first.searchParams.set('subscription_id',id);first.searchParams.set('per_page','50');
    let current=first.href, pages=0;const seen=new Set(), results=[];
    while (true) {
      if (++pages > 100 || seen.has(current)) throw Error('Paddle pagination incomplete');
      seen.add(current);
      const body=await read(current), pagination=body.meta?.pagination;
      if (!Array.isArray(body.data) || typeof pagination?.has_more !== 'boolean') throw Error('Invalid Paddle response');
      for (const adjustment of body.data) {
        if (!adjustment || adjustment.subscription_id !== id) throw Error('Unexpected adjustment');
        results.push(adjustment);
      }
      if (!pagination.has_more) return results;
      let next;try {next=new URL(pagination.next);} catch (_) {throw Error('Invalid Paddle pagination');}
      // Never forward credentials to arbitrary URLs or accept dropped filters.
      if (next.origin !== origin || next.pathname !== '/adjustments' || next.searchParams.get('subscription_id') !== id || !next.searchParams.get('after')) throw Error('Invalid Paddle pagination');
      current=next.href;
    }
  }
  async function scheduleCancellation(id) {
    if (!allowCancellation) throw Error('Cancellation disabled');
    if (!ID.test(id || '')) throw Error('Invalid subscription ID');
    const response=await fetchImpl(`${origin}/subscriptions/${id}/cancel`, {method:'POST',redirect:'error',headers:{authorization:`Bearer ${apiKey}`,'content-type':'application/json','accept':'application/json'},body:JSON.stringify({effective_from:'next_billing_period'}),signal:AbortSignal.timeout(4000)});
    if (!response.ok) throw Error('Paddle cancellation failed');
    const body=await response.json();if (!body?.data || body.data.id !== id) throw Error('Invalid Paddle response');
    return body.data;
  }
  return {getSubscription,listAdjustments,scheduleCancellation};
}
module.exports = {createPaddleClient};
