/* P3-A local UI derivative of frozen P2 v1.1.6 synthetic search. No real authorization. */
(function () {
  'use strict';
  const byId = id => document.getElementById(id);
  const form = byId('filters');
  const controls = byId('filter-controls');
  const scheme = byId('grade-scheme');
  const gradeFieldset = byId('grade-fieldset');
  const gradeSet = byId('grade-labels');
  const areaSet = byId('area-labels');
  const monthSet = byId('month-labels');
  const days = byId('max-days');
  const query = byId('keyword');
  const results = byId('results');
  const stats = byId('result-stats');
  const empty = byId('empty-state');
  const loading = byId('loading-state');
  const dataError = byId('data-error');
  const inputError = byId('input-error');
  const toggle = byId('filter-toggle');
  const gridBtn = byId('card-view');
  const listBtn = byId('list-view');
  const filterContent = byId('filter-content');
  const recovery = byId('recovery-actions');
  const friendlyNames = Object.freeze({
    'tanigawa-sawa-db':'谷川連峰の沢', 'okutama-sawa-db':'奥多摩の沢', 'tanzawa-sawa-db':'丹沢の沢',
    'tanigawa':'谷川連峰', 'okutama':'奥多摩', 'tanzawa':'丹沢',
    'syn-scale-x':'合成難度体系 X', 'syn-scale-y':'合成難度体系 Y'
  });
  const humanName = id => Object.hasOwn(friendlyNames, id) ? friendlyNames[id] : '名称未確認（識別子は非表示）';
  function setFiltersOpen(open, moveFocus = false) {
    filterContent.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? '検索条件を閉じる' : '検索条件を開く';
    toggle.setAttribute('aria-label', toggle.textContent);
    if (!open && moveFocus) toggle.focus();
  }
  toggle.addEventListener('click', () => setFiltersOpen(toggle.getAttribute('aria-expanded') !== 'true', true));
  function setResultView(mode) {
    results.classList.toggle('is-list', mode === 'list');
    gridBtn.setAttribute('aria-pressed', String(mode === 'card'));
    listBtn.setAttribute('aria-pressed', String(mode === 'list'));
  }
  gridBtn.addEventListener('click', () => setResultView('card'));
  listBtn.addEventListener('click', () => setResultView('list'));
  const smallScreen = window.matchMedia && window.matchMedia('(max-width: 40rem)').matches;
  if (smallScreen) setFiltersOpen(false);
  if (window.matchMedia) { window.matchMedia('(max-width: 40rem)').addEventListener('change', event => { if (!event.matches) setFiltersOpen(true); }); }
  byId('retry-data').addEventListener('click', () => window.location.reload());
  const selected = node => Array.from(node.querySelectorAll('input[type="checkbox"]:checked'), input => input.value);
  let rows = [];
  let schemes = [];
  let areas = [];
  let labels = [];
  let invalidNodes = [];
  let ready = false;
  function addChoices(node, values, name, labelFor) {
    node.replaceChildren();
    values.forEach(value => {
      const label = document.createElement('label');
      label.className = 'chip';
      const box = document.createElement('input');
      box.type = 'checkbox'; box.name = name; box.value = value;
      label.append(box, document.createTextNode(' ' + labelFor(value)));
      node.appendChild(label);
    });
  }
  function clearResults() {
    results.replaceChildren();
    empty.hidden = true;
    stats.hidden = true;
    ['count', 'total-count', 'ungraded-count'].forEach(id => { byId(id).textContent = '—'; });
  }
  function clearInputError() {
    invalidNodes.forEach(node => node.removeAttribute('aria-invalid'));
    invalidNodes = [];
    inputError.hidden = true;
    inputError.textContent = '';
  }
  function rejectInput(message, node) {
    clearResults();
    inputError.textContent = message + ' 条件を修正するか、すべて解除してください。';
    inputError.hidden = false;
    node.setAttribute('aria-invalid', 'true');
    invalidNodes.push(node);
  }
  function valuesAllowed(values, allowed) {
    return new Set(values).size === values.length && values.every(value => allowed.includes(value));
  }
  function readFilters() {
    const gradeValues = selected(gradeSet);
    const areaValues = selected(areaSet);
    const monthValues = selected(monthSet);
    if (scheme.value !== '' && !schemes.includes(scheme.value)) {
      return { error: '評価体系の値が無効です。', node: scheme };
    }
    if ((!scheme.value && gradeValues.length) || !valuesAllowed(gradeValues, labels)) {
      return { error: '選択した評価体系に属さないグレードです。', node: gradeFieldset };
    }
    if (!valuesAllowed(areaValues, areas)) return { error: '山域の値が無効です。', node: byId('area-fieldset') };
    const validMonthValues = Array.from({ length: 12 }, (_, index) => String(index + 1));
    if (!valuesAllowed(monthValues, validMonthValues)) return { error: '月は1〜12の選択肢から指定してください。', node: byId('month-fieldset') };
    if (!['', '1', '2', '3', '4', '5'].includes(days.value)) {
      return { error: '日数は1〜5日以内の選択肢から指定してください。', node: days };
    }
    if (query.value.length > 200) return { error: 'キーワードは200文字以内で指定してください。', node: query };
    return { filters: {
      areas: areaValues, scheme: scheme.value, grades: gradeValues,
      months: monthValues.map(Number), maxDays: days.value === '' ? null : Number(days.value),
      q: query.value.trim().toLocaleLowerCase('ja')
    } };
  }
  function matches(record, filters) {
    if (filters.areas.length && !filters.areas.includes(record.area_key)) return false;
    if (filters.q && !record.title.toLocaleLowerCase('ja').includes(filters.q)) return false;
    if (filters.scheme) {
      if (!window.P2SyntheticIndexContract.verifiedDifficulty(record.difficulty)
        || record.difficulty.grade_scheme_id !== filters.scheme) return false;
      if (filters.grades.length && !filters.grades.includes(record.difficulty.source_label)) return false;
    }
    if (filters.months.length && (record.recommended_months === null
      || !filters.months.some(month => record.recommended_months.includes(month)))) return false;
    if (filters.maxDays !== null && (record.duration_max_days === null
      || record.duration_max_days > filters.maxDays)) return false;
    return true;
  }
  function durationLabel(record) {
    if (record.duration_min_days === null) return '未確認';
    return record.duration_min_days === record.duration_max_days
      ? record.duration_min_days + '日' : record.duration_min_days + '〜' + record.duration_max_days + '日';
  }
  function render(visible) {
    results.replaceChildren();
    visible.forEach(record => {
      const item = document.createElement('li'); item.className = 'result';
      const icon = document.createElement('div'); icon.className = 'result-icon';
      const areaName = humanName(record.area_key);
      icon.setAttribute('aria-hidden','true'); icon.textContent = areaName.slice(0,1);
      const heading = document.createElement('h4');
      const link = document.createElement('a');
      // The contract admits only the exact relative path for this record. No remote routing.
      link.href = record.detail_path; link.textContent = record.title; heading.appendChild(link);
      const summary = document.createElement('p');
      const difficulty = record.difficulty === null ? '未確認'
        : humanName(record.difficulty.grade_scheme_id) + '・' + record.difficulty.source_label;
      summary.textContent = '山域：' + humanName(record.area_key) + ' ／ 原典難易度：' + difficulty
        + ' ／ 適期：' + (record.recommended_months === null ? '未確認' : record.recommended_months.join('・') + '月')
        + ' ／ 行程：' + durationLabel(record);
      const chip = document.createElement('span'); chip.className = 'record-label'; chip.textContent = 'HTML / 合成';
      const context = document.createElement('p'); context.className = 'hint';
      context.textContent = '元テーマ：' + humanName(record.topic_key) + ' ／ 識別子は内部管理（架空データ）';
      item.append(icon, chip, heading, summary, context); results.appendChild(item);
    });
    byId('count').textContent = String(visible.length);
    byId('total-count').textContent = String(rows.length);
    byId('ungraded-count').textContent = String(visible.filter(record => record.difficulty === null).length);
    stats.hidden = false;
    empty.hidden = visible.length !== 0;
  }
  function update() {
    if (!ready) return;
    clearInputError();
    const reading = readFilters();
    if (reading.error) { rejectInput(reading.error, reading.node); return; }
    render(rows.filter(record => matches(record, reading.filters)));
  }
  function updateGradeChoices() {
    // Replacing the choices clears every previous selection on each scheme change.
    labels = scheme.value === '' ? [] : Array.from(new Set(rows
      .filter(record => record.difficulty !== null && record.difficulty.grade_scheme_id === scheme.value)
      .map(record => record.difficulty.source_label))).sort();
    addChoices(gradeSet, labels, 'grade', value => value);
    gradeFieldset.disabled = scheme.value === '';
    byId('grade-hint').textContent = scheme.value
      ? 'この評価体系のラベルをそのまま選びます。複数選択はORです。'
      : '評価体系を選択するとグレードを選べます。未指定時は未確認のルートも表示します。';
    update();
  }
  function showDataError() {
    ready = false;
    controls.disabled = true;
    gradeFieldset.disabled = true;
    clearResults();
    loading.hidden = true;
    dataError.textContent = '検索データを読み込めません。形式または合成データの区分を確認できないため、検索を停止しています。これは検索結果0件ではありません。';
    dataError.hidden = false;
    recovery.hidden = false;
  }
  try {
    const contract = window.P2SyntheticIndexContract;
    const validation = contract && contract.validateIndex(window.SYNTHETIC_PUBLIC_SEARCH_INDEX);
    if (!validation || !validation.ok) { showDataError(); return; }
    rows = validation.records;
    areas = Array.from(new Set(rows.map(record => record.area_key))).sort();
    schemes = Array.from(new Set(rows.filter(record => record.difficulty !== null)
      .map(record => record.difficulty.grade_scheme_id))).sort();
    addChoices(areaSet, areas, 'area', value => humanName(value));
    addChoices(monthSet, Array.from({ length: 12 }, (_, index) => String(index + 1)), 'months', value => value + '月');
    schemes.forEach(value => {
      const option = document.createElement('option'); option.value = value; option.textContent = humanName(value); scheme.appendChild(option);
    });
    scheme.addEventListener('change', updateGradeChoices);
    [areaSet, gradeSet, monthSet, days].forEach(node => node.addEventListener('change', update));
    query.addEventListener('input', update);
    form.addEventListener('submit', event => { event.preventDefault(); update(); });
    byId('reset').addEventListener('click', () => {
      // A form descendant with id="reset" shadows form.reset in browsers.
      HTMLFormElement.prototype.reset.call(form);
      scheme.value = ''; days.value = ''; query.value = '';
      [areaSet, monthSet].forEach(node => node.querySelectorAll('input').forEach(box => { box.checked = false; }));
      updateGradeChoices();
    });
    ready = true; controls.disabled = false; loading.hidden = true;
    updateGradeChoices();
  } catch (_) { showDataError(); }
})();
