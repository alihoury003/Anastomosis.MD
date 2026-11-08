'use strict';

// Pure verification and request handling for the staged Paddle integration.
// The archive must persist events durably and idempotently before acknowledging.
const crypto = require('node:crypto');
const {parseEvent}=require('./event-fingerprint.cjs');
const MAX_BODY_BYTES = 1_000_000;

function verifySignature(rawBody, header, secret, now = Date.now(), toleranceSeconds = 5) {
  if (!Buffer.isBuffer(rawBody) || typeof header !== 'string' ||
      typeof secret !== 'string' || !secret || !Number.isFinite(now) ||
      !Number.isFinite(toleranceSeconds) || toleranceSeconds < 0) return false;
  const timestamps = [], signatures = [];
  for (const part of header.split(';')) {
    const separator = part.indexOf('=');
    if (separator < 0) continue;
    const key = part.slice(0, separator).trim(), value = part.slice(separator + 1).trim();
    if (key === 'ts') timestamps.push(value);
    if (key === 'h1' && /^[0-9a-fA-F]{64}$/.test(value)) signatures.push(Buffer.from(value, 'hex'));
  }
  if (timestamps.length !== 1 || !/^\d{1,12}$/.test(timestamps[0]) || !signatures.length) return false;
  const timestamp = Number(timestamps[0]);
  if (Math.abs(now / 1000 - timestamp) > toleranceSeconds) return false;
  const digest = crypto.createHmac('sha256', secret)
    .update(timestamps[0] + ':', 'utf8').update(rawBody).digest();
  // Evaluate all candidate signatures; never short-circuit a valid comparison.
  let match = 0;
  for (const signature of signatures) match |= Number(crypto.timingSafeEqual(digest, signature));
  return match === 1;
}

// The archive(event) callback must atomically create a durable, private record
// identified by event_id, return 'stored' or 'duplicate', and throw on failure.
// No entitlement is granted here; a verified event is NOT proof of paid access.
async function handleWebhook({ method, rawBody, signature, secret, archive, now = Date.now() }) {
  if (method !== 'POST') return { status: 405, body: 'Method not allowed' };
  if (typeof secret !== 'string' || !secret || typeof archive !== 'function') return { status: 503, body: 'Not configured' };
  if (!Buffer.isBuffer(rawBody)) return { status: 400, body: 'Raw body required' };
  if (rawBody.length > MAX_BODY_BYTES) return { status: 413, body: 'Payload too large' };
  if (!verifySignature(rawBody, signature, secret, now)) return { status: 401, body: 'Invalid signature' };
  let event;
  try { event = parseEvent(rawBody).event; } catch (_) { return { status: 400, body: 'Invalid payload' }; }
  try {
    const result = await archive({ id: event.event_id, type: event.event_type, rawBody });
    if (result !== 'stored' && result !== 'duplicate') throw new Error('Invalid archive result');
    return { status: 200, body: 'Accepted' };
  } catch (_) {
    // A non-2xx response is important: Paddle should retry if durability fails.
    return { status: 503, body: 'Temporarily unavailable' };
  }
}
module.exports = { verifySignature, handleWebhook, MAX_BODY_BYTES };
