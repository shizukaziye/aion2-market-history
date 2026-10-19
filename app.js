// Aion 2 market history: KR vs TW vs Global, one tab per item. No build step, no libraries.
const M = window.MARKET;
const $ = id => document.getElementById(id);
const state = { item: 0, scale: 'log', basis: 'nezekan' };

const fmt = n => n == null ? '–' : n >= 1e6 ? (n / 1e6).toFixed(2).replace(/\.?0+$/, '') + 'M' : n >= 1e3 ? Math.round(n / 1e3) + 'k' : String(Math.round(n));
const NEZ = '11102';

function icon(it, cls) {
  if (it.icon) return `<img class="${cls}" src="${it.icon}" referrerpolicy="no-referrer" alt="">`;
  return `<div class="ph ${cls}">no icon</div>`;
}

function renderTabs() {
  $('tabs').innerHTML = M.items.map((it, i) =>
    `<button class="tab${i === state.item ? ' on' : ''}" onclick="selectItem(${i})">${icon(it, '')}<span>${it.name}</span></button>`).join('');
}

function selectItem(i) { state.item = i; renderTabs(); renderItem(); try { localStorage.setItem('a2mh.item', String(i)); } catch (e) { } }
function setScale(s) { state.scale = s; renderItem(); }
function setBasis(b) { state.basis = b; renderItem(); }

// latest value with a number in a region's point list
function latest(points) {
  const withPrice = points.filter(p => p.price != null);
  return withPrice.length ? withPrice[withPrice.length - 1] : null;
}

function globalSeries(it) {
  if (state.basis === 'nezekan' && it.GL && it.GL[NEZ] && it.GL[NEZ].length) return it.GL[NEZ];
  return it.GLavg || [];
}

function renderCards(it) {
  const kr = latest(it.KR), tw = latest(it.TW), gl = latest(globalSeries(it));
  const krPeak = it.KR.filter(p => p.price != null).reduce((a, p) => p.price > (a ? a.price : -1) ? p : a, null);
  const card = (cls, lbl, p, extra) => `<div class="card ${cls}"><div class="lbl">${lbl}</div><div class="big">${p ? fmt(p.price) : 'no print'}</div><div class="when">${p ? (p.date + ' · week ' + Math.round(p.wk)) : (cls === 'tw' ? 'Taiwan board posts no numbers' : 'no data')}${extra || ''}</div></div>`;
  $('cards').innerHTML =
    card('kr', 'Korea, last quoted', kr) +
    card('kr', 'Korea, peak', krPeak) +
    card('tw', 'Taiwan, last quoted', tw) +
    card('gl', state.basis === 'nezekan' ? 'Global, Nezekan now' : 'Global, 6-server median now', gl, gl && gl.listings != null ? ` · ${gl.listings} listed` : '');
}

// SVG chart: x = weeks since each region's launch, y = Kina
function renderChart(it) {
  const W = 1100, H = 420, L = 70, R = 20, T = 18, B = 40;
  const series = [
    { key: 'KR', color: 'var(--kr)', pts: it.KR.filter(p => p.price != null) },
    { key: 'TW', color: 'var(--tw)', pts: it.TW.filter(p => p.price != null) },
    { key: 'GL', color: 'var(--gl)', pts: globalSeries(it).filter(p => p.price != null) },
  ];
  if (state.basis === 'nezekan' && it.GLavg && it.GLavg.length && it.GL && it.GL[NEZ]) series.push({ key: 'GLavg', color: 'var(--gl2)', dashed: true, pts: it.GLavg.filter(p => p.price != null) });
  const all = series.flatMap(s => s.pts);
  if (!all.length) { $('chart').innerHTML = `<svg viewBox="0 0 ${W} 160"><text x="${W / 2}" y="80" fill="#97a0b4" text-anchor="middle" font-size="15">No priced points for this item yet.</text></svg>`; return; }
  const maxWk = Math.max(50, ...all.map(p => p.wk)) ;
  const prices = all.map(p => p.price).filter(v => v > 0);
  let yMin = Math.min(...prices), yMax = Math.max(...prices);
  const log = state.scale === 'log';
  if (log) { yMin = Math.pow(10, Math.floor(Math.log10(yMin))); yMax = Math.pow(10, Math.ceil(Math.log10(yMax))); if (yMax === yMin) yMax *= 10; }
  else { yMin = 0; yMax = yMax * 1.08; }
  const X = wk => L + (wk / maxWk) * (W - L - R);
  const Y = v => log ? T + (1 - (Math.log10(v) - Math.log10(yMin)) / (Math.log10(yMax) - Math.log10(yMin))) * (H - T - B) : T + (1 - (v - yMin) / (yMax - yMin)) * (H - T - B);
  let g = '';
  // y grid
  const ticks = [];
  if (log) { for (let v = yMin; v <= yMax * 1.0001; v *= 10) { ticks.push(v); if (v * 3 < yMax) ticks.push(v * 3); } }
  else { for (let i = 0; i <= 5; i++) ticks.push(yMin + (yMax - yMin) * i / 5); }
  for (const v of ticks) g += `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" stroke="#2a3142"/><text x="${L - 6}" y="${Y(v) + 4}" fill="#97a0b4" font-size="11" text-anchor="end">${fmt(v)}</text>`;
  // x grid every 4 weeks + season marks (KR seasons: S1 ends wk ~12.6 Feb 2026? use KR: S1 Nov19-Feb? unknown exactly; mark global S1 end wk 10.3)
  for (let w = 0; w <= maxWk; w += 4) g += `<line x1="${X(w)}" x2="${X(w)}" y1="${T}" y2="${H - B}" stroke="#1f2533"/><text x="${X(w)}" y="${H - B + 14}" fill="#97a0b4" font-size="11" text-anchor="middle">wk ${w}</text>`;
  g += `<text x="${(L + W - R) / 2}" y="${H - 6}" fill="#97a0b4" font-size="11" text-anchor="middle">weeks since each region's launch (KR/TW Nov 19 2025, Global Oct 5 2026)</text>`;
  // global "now" marker
  const glNow = latest(globalSeries(it));
  if (glNow) g += `<line x1="${X(glNow.wk)}" x2="${X(glNow.wk)}" y1="${T}" y2="${H - B}" stroke="#66c7ff" stroke-dasharray="3 4" opacity=".6"/><text x="${X(glNow.wk) + 4}" y="${T + 10}" fill="#66c7ff" font-size="11">global today</text>`;
  for (const s of series) {
    const pts = s.pts.slice().sort((a, b) => a.wk - b.wk);
    if (pts.length > 1) g += `<polyline fill="none" stroke="${s.color}" stroke-width="${s.dashed ? 1.5 : 2.2}" ${s.dashed ? 'stroke-dasharray="5 4"' : ''} opacity="${s.key === 'GLavg' ? .8 : .95}" points="${pts.map(p => X(p.wk) + ',' + Y(p.price)).join(' ')}"/>`;
    if (s.key !== 'GLavg') for (const p of pts) {
      const hollow = p.conf === 'rough';
      g += `<circle cx="${X(p.wk)}" cy="${Y(p.price)}" r="${s.key === 'GL' ? 2.2 : 4.5}" fill="${hollow ? '#161a24' : s.color}" stroke="${s.color}" stroke-width="1.6" data-tip="${esc((s.key === 'GL' ? (state.basis === 'nezekan' ? 'Nezekan ' : 'Global median ') : s.key + ' ') + p.date + ': ' + fmt(p.price) + (p.quote ? ' — ' + p.quote : '') + (p.listings != null ? ' (' + p.listings + ' listed)' : ''))}"/>`;
    }
  }
  $('chart').innerHTML = `<svg viewBox="0 0 ${W} ${H}" id="svg">${g}</svg>`;
  const tip = $('tip');
  $('svg').querySelectorAll('circle[data-tip]').forEach(c => {
    c.addEventListener('mouseenter', e => { tip.textContent = c.getAttribute('data-tip'); tip.style.display = 'block'; });
    c.addEventListener('mousemove', e => { tip.style.left = (e.pageX + 12) + 'px'; tip.style.top = (e.pageY + 12) + 'px'; });
    c.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
  });
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }

function renderTable(it) {
  const rows = [];
  for (const r of ['KR', 'TW']) for (const p of it[r]) rows.push({ r, ...p });
  const gl = globalSeries(it);
  if (gl.length) {
    const first = gl[0], last = gl[gl.length - 1];
    const peak = gl.reduce((a, p) => p.price > a.price ? p : a, gl[0]);
    const low = gl.reduce((a, p) => p.price < a.price ? p : a, gl[0]);
    for (const [lbl, p] of [['first day', first], ['low', low], ['high', peak], ['today', last]]) rows.push({ r: 'GL', date: p.date, wk: p.wk, price: p.price, conf: 'quoted', src: 'https://aion2.exchange', quote: `${state.basis === 'nezekan' ? 'Nezekan' : '6-server median'} daily median of the cheapest ask, ${lbl}${p.listings != null ? ', ' + p.listings + ' listed' : ''}` });
  }
  rows.sort((a, b) => a.wk - b.wk || a.r.localeCompare(b.r));
  $('rows').innerHTML = rows.map(p => `<tr><td class="r-${p.r}">${p.r === 'GL' ? 'Global' : p.r === 'KR' ? 'Korea' : 'Taiwan'}</td><td>${p.date}</td><td class="num">${Math.round(p.wk)}</td><td class="num">${fmt(p.price)}</td><td><span class="conf ${p.conf}">${p.conf}</span></td><td class="quote">${esc(p.quote || '')}${p.note ? ' <i>(' + esc(p.note) + ')</i>' : ''}</td><td>${p.src ? `<a href="${p.src}" target="_blank" rel="noopener">source</a>` : ''}</td></tr>`).join('') || '<tr><td colspan="7" class="quote">No points.</td></tr>';
}

function renderItem() {
  const it = M.items[state.item];
  $('head').innerHTML = `${icon(it, '')}<div><h2>${it.name}</h2><div class="sub">${it.kr} · ${it.tw}</div></div>`;
  $('about').textContent = it.about;
  document.querySelectorAll('[data-scale]').forEach(b => b.classList.toggle('on', b.dataset.scale === state.scale));
  document.querySelectorAll('[data-basis]').forEach(b => b.classList.toggle('on', b.dataset.basis === state.basis));
  renderCards(it); renderChart(it); renderTable(it);
}

window.onload = () => {
  try { const s = parseInt(localStorage.getItem('a2mh.item')); if (!isNaN(s) && M.items[s]) state.item = s; } catch (e) { }
  $('built').textContent = 'global data pulled ' + M.built.slice(0, 16).replace('T', ' ') + ' UTC';
  renderTabs(); renderItem();
};
