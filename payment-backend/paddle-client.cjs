'use strict';
// Server-side read-only Paddle adapter. No account, catalog or subscription
// changes. Credentials must only come from private server configuration.
const ID = /^sub_[a-z0-9]{26}$/;
const TXN = /^txn_[a-z0-9]{26}$/;
const PRICE = /^pri_[a-z0-9]{26}$/;
const EVENT = /^evt_[a-z0-9]{26}$/;
const {parseEvent}=require('./event-fingerprint.cjs');
const EVENT_TYPES=['subscription.created','subscription.updated','subscription.activated','subscription.canceled','subscription.paused','subscription.resumed','subscription.past_due','transaction.completed','adjustment.created','adjustment.updated'];
function createPaddleClient({environment, apiKey, fetchImpl=globalThis.fetch}) {
  if (!['sandbox','live'].includes(environment) || typeof apiKey !== 'string' || !apiKey || typeof fetchImpl !== 'function') throw Error('Paddle client not configured');
  const origin = environment === 'sandbox' ? 'https://sandbox-api.paddle.com' : 'https://api.paddle.com';
  async function read(url) {
    const parsed = new URL(url);
    if (parsed.origin !== origin || !['/adjustments','/events'].includes(parsed.pathname) && !/^\/(?:subscriptions\/sub|transactions\/txn|prices\/pri)_[a-z0-9]{26}$/.test(parsed.pathname)) throw Error('Invalid Paddle URL');
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
  async function getPrice(id) {
    if (!PRICE.test(id || '')) throw Error('Invalid price ID');
    const body=await read(`${origin}/prices/${id}`);if (!body.data || body.data.id!==id) throw Error('Invalid Paddle response');return body.data;
  }
  async function getTransaction(id) {
    if (!TXN.test(id || '')) throw Error('Invalid transaction ID');
    const body=await read(`${origin}/transactions/${id}`);if (!body.data || body.data.id!==id) throw Error('Invalid Paddle response');return body.data;
  }
  async function listAdjustments(id) {
    if (!ID.test(id || '') && !TXN.test(id || '')) throw Error('Invalid billing ID');
    const filter=ID.test(id)?'subscription_id':'transaction_id';
    const first=new URL(`${origin}/adjustments`);first.searchParams.set(filter,id);first.searchParams.set('per_page','50');
    let current=first.href, pages=0;const seen=new Set(), results=[];
    while (true) {
      if (++pages > 100 || seen.has(current)) throw Error('Paddle pagination incomplete');
      seen.add(current);
      const body=await read(current), pagination=body.meta?.pagination;
      if (!Array.isArray(body.data) || typeof pagination?.has_more !== 'boolean') throw Error('Invalid Paddle response');
      for (const adjustment of body.data) {
        if (!adjustment || adjustment[filter] !== id) throw Error('Unexpected adjustment');
        results.push(adjustment);
      }
      if (!pagination.has_more) return results;
      let next;try {next=new URL(pagination.next);} catch (_) {throw Error('Invalid Paddle pagination');}
      // Never forward credentials to arbitrary URLs or accept dropped filters.
      if (next.origin !== origin || next.pathname !== '/adjustments' || next.searchParams.get(filter) !== id || !next.searchParams.get('after')) throw Error('Invalid Paddle pagination');
      current=next.href;
    }
  }
  async function listEventPage({after=null,limit=10}={}) {
    if(after!==null&&(!EVENT.test(after||'')))throw Error('Invalid event cursor');
    if(!Number.isInteger(limit)||limit<1||limit>50)throw Error('Invalid page limit');
    const url=new URL(`${origin}/events`);url.searchParams.set('event_type',EVENT_TYPES.join(','));url.searchParams.set('order_by','id[ASC]');url.searchParams.set('per_page',String(limit));if(after)url.searchParams.set('after',after);
    const body=await read(url.href),page=body.meta?.pagination;
    if(!Array.isArray(body.data)||body.data.length>limit||typeof page?.has_more!=='boolean')throw Error('Invalid event page');
    let previous=after;
    for(const event of body.data){
      const parsed=parseEvent(Buffer.from(JSON.stringify(event),'utf8')).event;
      if(!EVENT_TYPES.includes(parsed.event_type)||(previous&&parsed.event_id<=previous))throw Error('Invalid event page');
      previous=parsed.event_id;
    }
    if(page.has_more){
      if(!body.data.length)throw Error('Invalid event pagination');
      let next;try{next=new URL(page.next);}catch(_){throw Error('Invalid event pagination');}
      if(next.origin!==origin||next.pathname!=='/events'||next.searchParams.get('event_type')!==EVENT_TYPES.join(',')||next.searchParams.get('order_by')!=='id[ASC]'||next.searchParams.get('per_page')!==String(limit)||next.searchParams.get('after')!==previous)throw Error('Invalid event pagination');
    }
    return{events:body.data,hasMore:page.has_more};
  }
  return {getPrice,getTransaction,getSubscription,listAdjustments,listEventPage};
}
module.exports = {createPaddleClient,EVENT_TYPES};
