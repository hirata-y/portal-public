/* P2 source v1.1.0. Source authored only; UI/search execution is NOT AUTHORIZED. */
(function () {
  'use strict';
  const slug = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  const recordId = /^[A-Za-z0-9_-]+$/;
  const controls = /[\u0000-\u001f\u007f]/;
  const safeToken = value => typeof value === 'string' && !controls.test(value) && slug.test(value);
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  const objectWithKeys = (value, keys) => value !== null && typeof value === 'object'
    && !Array.isArray(value) && Object.keys(value).length === keys.length
    && keys.every(key => own(value, key));
  const nonempty = value => typeof value === 'string' && value.trim().length > 0 && !controls.test(value);
  function verifiedDifficulty(value) {
    return value !== null && objectWithKeys(value, ['source_label', 'grade_scheme_id', 'verification_reference'])
      && nonempty(value.source_label) && Array.from(value.source_label).length <= 128
      && safeToken(value.grade_scheme_id)
      && typeof value.verification_reference === 'string' && validReference(value.verification_reference);
  }
  function validReference(value) {
    // This UI accepts only reserved synthetic evidence strings; it never retrieves them.
    if (typeof value !== 'string' || !value.startsWith('https://')
      || /[\s\u0000-\u001f\u007f\\#]/u.test(value)) return false;
    try {
      const url = new URL(value);
      return url.protocol === 'https:' && url.hostname === 'example.invalid'
        && !url.username && !url.password && !url.port && !url.hash;
    } catch (_) { return false; }
  }
  function validMonths(value) {
    return value === null || (Array.isArray(value) && value.length > 0 && value.length <= 12
      && value.every(month => Number.isInteger(month) && month >= 1 && month <= 12)
      && new Set(value).size === value.length);
  }
  function validDuration(min, max) {
    return (min === null && max === null)
      || (Number.isInteger(min) && Number.isInteger(max) && min >= 1 && max >= min);
  }
  function validateIndex(data) {
    const envelope = ['schema_version', 'visibility', 'data_origin', 'execution_scope', 'records'];
    if (!objectWithKeys(data, envelope) || data.schema_version !== '1.0.0'
      || data.visibility !== 'public' || data.data_origin !== 'synthetic'
      || data.execution_scope !== 'private-local-only' || !Array.isArray(data.records)) {
      return { ok: false, code: 'INDEX_ENVELOPE_INVALID' };
    }
    const keys = ['topic_key', 'area_key', 'record_id', 'title', 'difficulty',
      'recommended_months', 'duration_min_days', 'duration_max_days', 'detail_path'];
    const identities = new Set();
    for (const record of data.records) {
      if (!objectWithKeys(record, keys) || !safeToken(record.topic_key)
        || !safeToken(record.area_key)
        || typeof record.record_id !== 'string' || controls.test(record.record_id)
        || !recordId.test(record.record_id) || record.record_id.length > 100
        || !nonempty(record.title) || Array.from(record.title).length > 120
        || !(record.difficulty === null || verifiedDifficulty(record.difficulty))
        || !validMonths(record.recommended_months)
        || !validDuration(record.duration_min_days, record.duration_max_days)
        || record.detail_path !== 'themes/' + record.topic_key + '/records/' + record.record_id + '.html') {
        return { ok: false, code: 'INDEX_RECORD_INVALID' };
      }
      const identity = record.topic_key + '/' + record.record_id;
      if (identities.has(identity)) return { ok: false, code: 'INDEX_ID_DUPLICATE' };
      identities.add(identity);
    }
    return { ok: true, records: data.records };
  }
  window.P2SyntheticIndexContract = Object.freeze({ validateIndex, verifiedDifficulty });
})();
