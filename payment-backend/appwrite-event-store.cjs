'use strict';

const crypto = require('node:crypto');
// The private Appwrite collection must be explicitly provisioned with a string
// payloadBase64 column of at least 44,000 characters. No client permissions.
const MAX_STORED_BYTES = 32000;
const VALID_ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,35}$/;

function createEventArchive({ endpoint, projectId, databaseId, collectionId, apiKey, fetchImpl = globalThis.fetch }) {
  if (typeof endpoint !== 'string' || !/^https:\/\/nyc\.cloud\.appwrite\.io\/v1\/?$/.test(endpoint) ||
      ![projectId, databaseId, collectionId].every(v => typeof v === 'string' && VALID_ID.test(v)) ||
      typeof apiKey !== 'string' || !apiKey || typeof fetchImpl !== 'function') throw Error('Archive not configured');
  const base = `${endpoint.replace(/\/$/, '')}/databases/${encodeURIComponent(databaseId)}/collections/${encodeURIComponent(collectionId)}/documents`;
  const headers = { 'content-type':'application/json', 'x-appwrite-project':projectId, 'x-appwrite-key':apiKey };
  return async function archive({ id, type, rawBody }) {
    if (!/^evt_[a-z0-9]{26}$/.test(id) || !/^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$/.test(type) || !Buffer.isBuffer(rawBody) || rawBody.length > MAX_STORED_BYTES) throw Error('Invalid event');
    const hash = crypto.createHash('sha256').update(rawBody).digest('hex');
    const payload = { documentId:id, data:{ eventType:type, payloadBase64:rawBody.toString('base64'), payloadSha256:hash, processingStatus:'pending' }, permissions:[] };
    // One shared deadline bounds both write and duplicate verification so
    // Paddle receives a response before its five-second delivery timeout.
    const signal = AbortSignal.timeout(3500);
    const response = await fetchImpl(base, { method:'POST', headers, body:JSON.stringify(payload), signal });
    if (response.ok) return 'stored';
    // A uniqueness error is not automatically proof of a safe duplicate.
    if (response.status !== 409) throw Error('Archive write failed');
    const conflict = await response.json().catch(() => ({}));
    if (conflict.type !== 'document_already_exists') throw Error('Unexpected archive conflict');
    const previous = await fetchImpl(`${base}/${encodeURIComponent(id)}`, { method:'GET', headers, signal });
    if (!previous.ok) throw Error('Unable to verify duplicate');
    const doc = await previous.json();
    if (doc.$id !== id || doc.payloadSha256 !== hash || doc.eventType !== type) throw Error('Event collision');
    return 'duplicate';
  };
}
module.exports = { createEventArchive, MAX_STORED_BYTES };
