'use strict';

// Server-only authenticated checkout binding. This does not authenticate a
// user, validate a payment, or grant access. The caller must do all three.
const { createHmac, randomBytes, timingSafeEqual } = require('node:crypto');
const CONTEXT = 'anastomosis-checkout-binding-v1:';
const USER = /^[a-zA-Z0-9][a-zA-Z0-9._-]{0,35}$/;
const PRICE = /^pri_[a-z0-9]{26}$/;
const NONCE = /^[A-Za-z0-9_-]{32}$/;
const ENV = new Set(['sandbox', 'live']);

function validKey(key) { return Buffer.isBuffer(key) && key.length >= 32; }
function signature(payload, key) {
  return createHmac('sha256', key).update(CONTEXT, 'utf8').update(payload, 'utf8').digest();
}
function createBinding({ userId, priceId, environment }, key) {
  if (!validKey(key)) throw new Error('A server-only binding key of at least 32 bytes is required');
  if (typeof userId !== 'string' || !USER.test(userId) || typeof priceId !== 'string' || !PRICE.test(priceId) || !ENV.has(environment)) throw new Error('Invalid checkout binding');
  const data = { v: 1, userId, priceId, environment, nonce: randomBytes(24).toString('base64url') };
  const payload = Buffer.from(JSON.stringify(data), 'utf8').toString('base64url');
  return `${payload}.${signature(payload, key).toString('base64url')}`;
}
function verifyBinding(token, key, expectedEnvironment) {
  if (!validKey(key) || !ENV.has(expectedEnvironment) || typeof token !== 'string' || token.length > 1024) return null;
  const pieces = token.split('.');
  if (pieces.length !== 2 || !/^[A-Za-z0-9_-]+$/.test(pieces[0]) || !/^[A-Za-z0-9_-]{43}$/.test(pieces[1])) return null;
  const supplied = Buffer.from(pieces[1], 'base64url');
  // Reject non-canonical base64 encodings and ambiguous spellings.
  if (supplied.length !== 32 || supplied.toString('base64url') !== pieces[1]) return null;
  const expected = signature(pieces[0], key);
  if (!timingSafeEqual(supplied, expected)) return null;
  try {
    const raw = Buffer.from(pieces[0], 'base64url');
    if (raw.toString('base64url') !== pieces[0]) return null;
    const value = JSON.parse(raw.toString('utf8'));
    if (!value || value.v !== 1 || typeof value.userId !== 'string' || !USER.test(value.userId) ||
        typeof value.priceId !== 'string' || !PRICE.test(value.priceId) ||
        value.environment !== expectedEnvironment || typeof value.nonce !== 'string' || !NONCE.test(value.nonce)) return null;
    return { userId: value.userId, priceId: value.priceId, environment: value.environment, nonce: value.nonce };
  } catch (_) { return null; }
}
module.exports = { createBinding, verifyBinding };
