/* AI Allocation — Conviction Dashboard
   Loads conviction.json (produced by scoring/score_holdings.py --json) and
   renders a filterable, sortable DATA TABLE. No build step, no dependencies. */

const WAVE_NAMES = {
  W1: "W1 · Silicon", W2: "W2 · Power", W3: "W3 · DC-Infra",
  W4: "W4 · Cloud", W5: "W5 · Software", W6: "W6 · Spec",
  W7: "W7 · Diversify", ET: "ETF look-through", WL: "Watchlist",
};

const GRADE_CLASS = {
  "PRIME": "b-green", "KEEP-DCA": "b-green", "MOMENTUM": "b-blue",
  "QUALITY": "b-blue", "RICH": "b-amber", "AVOID": "b-red", "IMPAIRED": "b-red",
};

const STRAT_LABEL = {
  dca: "DCA", cycle: "CYCLE", catalyst: "CATALYST", lottery: "LOTTERY", "?": "—",
};

// Glossary, split in two: the engine's own vocabulary, and the standard
// finance metrics the layers are built from. Rendered into the About tab.
const GLOSSARY_CONV = [
  ["CONV", "Conviction — the headline 0–10 score. Higher = a stronger risk-adjusted case for owning the name now. Geometric mean of a reward and a safety term."],
  ["F", "Fundamentals layer (0–10, higher = safer). Business quality, momentum-neutral: margins, forward growth, FCF, margin trajectory and consistency."],
  ["V", "Valuation layer (0–10, higher = cheaper/fairer). PEG first, P/S-vs-growth fallback, plus distance above the 200-day moving average."],
  ["C", "Cycle layer (0–10, higher = earlier/less crowded). Position in the industry wave, chart extension, and whether the name sits on a supply bottleneck."],
  ["Bind", "Binding layer — the lowest of F/V/C, i.e. the dominant risk. Counted a second time inside the safety term."],
  ["Plot", "Opens the Plot tab with this name selected — an interactive price chart you can overlay with other tickers over 1w–5y windows."],
  ["8PT", "The 8-point entry screen (0–8): small + cheap + accelerating checks used for cycle/catalyst names. Rescaled to 0–10 inside the cycle conviction."],
  ["GROWTH", "The 0–10 growth score — how much the business can compound. Drives the reward term for cycle/catalyst names."],
  ["QUALITY", "The DCA quality score — durability of a buy-forever compounder. Replaces GROWTH in the DCA conviction variant."],
  ["RICHNESS", "The DCA price gate (0 = cheap … 1 = stretched). A rich name is bought slower, not skipped; it enters safety as (1 − richness)."],
  ["DCA", "Dollar-cost averaging — a proven compounder you buy on a schedule regardless of price. Graded on quality + valuation, not on being small/explosive."],
  ["CYCLE (strategy)", "A name bought for its position in an industry cycle — graded on the two-axis quadrant (where in the cycle, how cheap)."],
  ["CATALYST", "A name bought for a specific upcoming event; graded on whether the punt's upside is still intact."],
  ["LOTTERY", "A pre-revenue / single-event punt (Binary). High opacity is treated as a red flag, not a neutral."],
  ["Book %", "The name's target weight in the portfolio book. Watch-only names have no book weight."],
  ["Data % (coverage)", "Share of obtainable fundamentals actually present for the name. Below 75% the score is scaled down (a GAP) and the cell turns red."],
  ["GAP", "Coverage < 75% — the score rests on thin data and should be trusted less."],
  ["PEAK?", "A cyclical whose low PEG is fake-cheap on peak-cycle earnings while the chart is extended (the memory/storage trap). Cuts cycle CONV ×0.85."],
  ["MARG?", "An early-cycle name whose net margin is compressing — the cycle tag and the margin data disagree (thesis unwinding or a stale tag). Annotation only; treat its VAL with caution."],
  ["Held only", "Filter toggle: show just the names with a live position (Book % > 0), hiding watch-only candidates."],
  ["Wave (W1–W7)", "The AI-allocation basket: W1 Silicon, W2 Power, W3 DC-Infra, W4 Cloud, W5 Software, W6 Spec, W7 Diversify. ET = surfaced via ETF look-through."],
  ["Grade", "The strategy-aware verdict: PRIME / KEEP-DCA (buy), MOMENTUM / QUALITY (hold-ish), RICH (wait for a better price), AVOID / IMPAIRED (pass). N/A = no fundamentals page exists for the name (e.g. a physical-commodity trust), so it cannot be scored — not a negative verdict."],
];

const GLOSSARY_FIN = [
  ["Market cap", "Market capitalisation — share price × shares outstanding, i.e. the total equity value of the company. Used here to gauge size (small caps can re-rate faster)."],
  ["Revenue growth", "Year-over-year change in sales. 'Forward' = analyst forecast for the next period(s); 'TTM' = trailing twelve months already reported."],
  ["EPS", "Earnings per share — net profit divided by shares outstanding. 'EPS growth' is its year-over-year change; the cleanest per-share read on profitability."],
  ["Net margin", "Net profit ÷ revenue, as a %. What's left after all costs, interest and tax — the bottom-line profitability of every sales dollar."],
  ["Gross margin", "(Revenue − cost of goods sold) ÷ revenue, as a %. Measures the raw profitability of the product before overhead — a proxy for pricing power / model quality."],
  ["Operating margin", "Operating profit ÷ revenue, as a %. Profitability from core operations before interest and tax; used in place of net margin when one-off items distort the bottom line."],
  ["Margin trajectory", "The direction margins are moving over time (expanding vs compressing), not just the level. A rising margin signals improving economics."],
  ["FCF (free cash flow)", "Operating cash flow minus capital expenditure — the actual cash a business generates after funding itself. 'FCF-positive' means it self-funds rather than burning cash."],
  ["P/E", "Price-to-earnings ratio — share price ÷ EPS. How many dollars you pay per dollar of annual earnings; the classic valuation yardstick."],
  ["PEG", "P/E-to-Growth — the P/E ratio divided by the earnings growth rate. Below ~1 looks cheap for the growth, but on a late-cycle name a sub-1 PEG is usually the peak-earnings trap."],
  ["P/S (ps_ratio)", "Price-to-sales ratio — market cap ÷ revenue. A valuation fallback for loss-makers and pre-profit names that have no meaningful P/E or PEG."],
  ["200DMA", "200-day moving average of the price. Distance above it measures how extended the chart is — a proxy for how much optimism is already paid for."],
  ["Chart extension", "How far the price sits above its 200DMA. A large gap means the move is stretched and more of the upside is already priced in."],
  ["Cyclical", "A business whose earnings swing with an industry cycle (memory, energy, mining). Its multiples look cheapest at the peak, which is exactly the danger."],
  ["Bottleneck", "A genuine supply constraint the company sits on (e.g. leading-edge foundry, HBM, power). Scarce capacity supports pricing and defends the cycle position."],
];

// Column definitions: key into a record, header label, alignment, numeric flag.
const COLUMNS = [
  { key: "ticker",   label: "Ticker",   align: "left",   num: false },
  { key: "wave",     label: "Wave",     align: "left",   num: false },
  { key: "strategy", label: "Strategy", align: "left",   num: false },
  { key: "grade",    label: "Grade",    align: "left",   num: false },
  { key: "conv",     label: "CONV",     align: "right",  num: true  },
  { key: "F",        label: "F",        align: "right",  num: true  },
  { key: "V",        label: "V",        align: "right",  num: true  },
  { key: "C",        label: "C",        align: "right",  num: true  },
  { key: "book_pct", label: "Book %",   align: "right",  num: true  },
  { key: "coverage", label: "Data %",   align: "right",  num: true  },
  { key: "plot",     label: "Plot",     align: "center", num: false, sortable: false },
];

const state = {
  data: [], view: "stock", wave: "ALL", q: "", heldOnly: false,
  sortKey: "conv", sortDir: -1,   // -1 = descending, 1 = ascending
};

// Price history for the Plot tab, loaded from plot_history.json:
// { ticker: { t: [ISO dates], c: [closes] } }. Empty until loaded.
let PLOT_HISTORY = {};

// Buy zones (accumulation bands) loaded from buy_zones.json:
// { ticker: { low, high, source, note } }. Absolute prices; shaded on the Plot
// tab only when a SINGLE ticker is selected. Empty until loaded.
let BUY_ZONES = {};

// Plot-tab UI state. Series are rebased to % change so different price levels
// compare directly; the range picks the trailing window (default 5y).
const plotState = {
  selected: new Set(),   // tickers currently overlaid
  range: "5y",           // 1w | 1m | 6m | 1y | 2y | 5y | all
  q: "",                 // ticker filter for the checkbox side panel
};

// Trailing window length per range, in days (null = all available history).
const PLOT_RANGE_DAYS = {
  "1w": 7, "1m": 31, "6m": 183, "1y": 366, "2y": 731, "5y": 1827, "all": null,
};

// Distinct line colours cycled across overlaid series.
const PLOT_COLORS = [
  "#34d399", "#7dd3fc", "#f5c451", "#f87171", "#c084fc",
  "#fb923c", "#22d3ee", "#a3e635", "#f472b6", "#60a5fa",
  "#facc15", "#4ade80", "#e879f9", "#38bdf8", "#fca5a5",
];

function convTextColor(c) {
  if (c >= 7.5) return "#34d399";      // strong — emerald
  if (c >= 6.0) return "#7dd3fc";      // solid — cyan
  if (c >= 4.5) return "#f5c451";      // middling — amber
  return "#f87171";                    // weak — red
}

async function boot() {
  let payload;
  try {
    const res = await fetch("conviction.json", { cache: "no-store" });
    payload = await res.json();
  } catch (e) {
    document.getElementById("tbody").innerHTML =
      '<tr><td colspan="11" class="empty">Could not load conviction.json. ' +
      'Run <code>PORTFOLIO_USE=ai python3 scoring/score_holdings.py --json</code> first.</td></tr>';
    return;
  }
  state.data = payload.records || [];

  // Price history for the Plot tab. Optional: if it fails to load the rest of
  // the dashboard still works and plot glyphs render disabled.
  try {
    const pres = await fetch("plot_history.json", { cache: "no-store" });
    const ppayload = await pres.json();
    PLOT_HISTORY = ppayload.history || {};
  } catch (e) {
    PLOT_HISTORY = {};
  }

  // Buy zones for the Plot tab. Optional: if it fails to load the chart still
  // works, just without the shaded accumulation band.
  try {
    const zres = await fetch("buy_zones.json", { cache: "no-store" });
    const zpayload = await zres.json();
    BUY_ZONES = zpayload.zones || {};
  } catch (e) {
    BUY_ZONES = {};
  }

  // Default the Plot tab to every held name that has price history, so the
  // chart opens pre-populated with the active book instead of empty.
  for (const r of state.data) {
    if (r.held && PLOT_HISTORY[r.ticker]) plotState.selected.add(r.ticker);
  }

  document.getElementById("navMeta").textContent =
    `${payload.count} names · ${payload.held_count} held`;
  document.getElementById("footMeta").textContent =
    `Generated ${payload.generated_utc} · source ${payload.csv}`;

  buildWaveChips();
  buildStats();
  buildGlossary();
  buildHead();
  wireControls();
  wirePlotControls();
  render();
}

// Render the two glossary lists into the About tab.
function buildGlossary() {
  const fill = (id, rows) => {
    const dl = document.getElementById(id);
    if (!dl) return;
    dl.innerHTML = rows.map(([term, def]) =>
      `<div class="gloss-row">
         <dt>${term}</dt>
         <dd>${def}</dd>
       </div>`).join("");
  };
  fill("glossaryConv", GLOSSARY_CONV);
  fill("glossaryFin", GLOSSARY_FIN);
}

function buildWaveChips() {
  const wrap = document.getElementById("waveFilters");
  const waves = ["ALL", ...Object.keys(WAVE_NAMES).filter(
    w => state.data.some(r => r.wave === w))];
  wrap.innerHTML = "";
  waves.forEach(w => {
    const b = document.createElement("button");
    b.className = "chip" + (w === state.wave ? " chip-on" : "");
    b.textContent = w === "ALL" ? "All waves" : w;
    b.onclick = () => { state.wave = w; syncChips(); render(); };
    b.dataset.wave = w;
    wrap.appendChild(b);
  });
}

function syncChips() {
  document.querySelectorAll(".chip").forEach(c =>
    c.classList.toggle("chip-on", c.dataset.wave === state.wave));
}

function buildStats() {
  const held = state.data.filter(r => r.held);
  const avg = held.length
    ? (held.reduce((s, r) => s + r.conv, 0) / held.length) : 0;
  // "Top" is the highest-conviction name across the WHOLE universe (held +
  // watchlist), not just held — otherwise a watchlist leader like FICO is
  // hidden behind the top held name.
  const top = state.data.reduce((a, r) => r.conv > a.conv ? r : a, { conv: -1 });
  const book = held.reduce((s, r) => s + r.book_pct, 0);
  const stats = [
    ["Held names", held.length],
    ["Avg conviction", avg.toFixed(2)],
    ["Top", top.ticker ? `${top.ticker} ${top.conv.toFixed(2)}` : "—"],
    ["Book covered", book.toFixed(0) + "%"],
    ["Total names", state.data.length],
  ];
  document.getElementById("statBar").innerHTML = stats.map(([l, v]) =>
    `<div class="stat"><div class="stat-val">${v}</div>` +
    `<div class="stat-lab">${l}</div></div>`).join("");
}

// Build the sortable header row once; clicking a th sets the sort key/dir.
function buildHead() {
  const thead = document.getElementById("thead");
  thead.innerHTML = "<tr>" + COLUMNS.map(c =>
    `<th data-key="${c.key}" class="th-${c.align}${c.num ? " th-num" : ""}">` +
    `<span class="th-lab">${c.label}</span><span class="th-arrow"></span></th>`
  ).join("") + "</tr>";
  thead.querySelectorAll("th").forEach(th => {
    const colDef = COLUMNS.find(c => c.key === th.dataset.key);
    if (colDef && colDef.sortable === false) return;  // plot column: not sortable
    th.onclick = () => {
      const k = th.dataset.key;
      if (state.sortKey === k) {
        state.sortDir *= -1;                 // toggle direction
      } else {
        state.sortKey = k;
        // numeric columns default to descending, text to ascending
        const col = COLUMNS.find(c => c.key === k);
        state.sortDir = col && col.num ? -1 : 1;
      }
      render();
    };
  });
}

function wireControls() {
  document.querySelectorAll(".tab").forEach(t => {
    t.onclick = () => {
      document.querySelectorAll(".tab").forEach(x =>
        x.classList.remove("tab-active"));
      t.classList.add("tab-active");
      state.view = t.dataset.view;
      render();
    };
  });
  // "methodology" link in the table footer jumps to the About tab.
  const footAbout = document.getElementById("footAbout");
  if (footAbout) footAbout.onclick = e => {
    e.preventDefault();
    document.querySelector('.tab[data-view="about"]').click();
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  document.getElementById("search").oninput = e => {
    state.q = e.target.value.trim().toUpperCase(); render();
  };
  document.getElementById("heldOnly").onchange = e => {
    state.heldOnly = e.target.checked; render();
  };
}

function sortRows(rows) {
  const k = state.sortKey, dir = state.sortDir;
  const col = COLUMNS.find(c => c.key === k);
  const num = col && col.num;
  return rows.sort((a, b) => {
    let av = a[k], bv = b[k];
    if (num) return ((av ?? 0) - (bv ?? 0)) * dir;
    av = String(av ?? ""); bv = String(bv ?? "");
    return av.localeCompare(bv) * dir;
  });
}

// A single table row.
function row(r) {
  // No-fundamentals names (has_data=false, e.g. SRUUF — a physical-commodity
  // trust with no company financials page) have no meaningful score. Render
  // them as N/A rather than a misleading AVOID / 0.00, which would imply a
  // negative fundamental verdict on a name that simply cannot be scored.
  const noData = r.has_data === false;
  const gc = noData ? "b-mut" : (GRADE_CLASS[r.grade] || "b-mut");

  const layer = (k, v) =>
    noData
      ? `<td class="td-num td-layer mut">—</td>`
      : `<td class="td-num td-layer"><span class="lcell">` +
        `<span class="ltrack"><span class="lbar lf-${k}" style="width:${v * 10}%"></span></span>` +
        `<b>${v.toFixed(1)}</b></span></td>`;

  const bookStr = r.held
    ? `${r.book_pct.toFixed(2)}`
    : `<span class="mut">—</span>`;

  const gradeCell = noData ? "N/A" : r.grade;
  const convCell = noData
    ? `<span class="mut">—</span>`
    : `<b>${r.conv.toFixed(2)}</b>`;
  const convStyle = noData ? "" : `style="color:${convTextColor(r.conv)}"`;

  return `<tr>
    <td class="td-tkr"><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" rel="noopener">${r.ticker}</a></td>
    <td class="mut">${r.wave}</td>
    <td>${STRAT_LABEL[r.strategy] || r.strategy}</td>
    <td><span class="badge ${gc}">${gradeCell}</span></td>
    <td class="td-num td-conv" ${convStyle}>${convCell}</td>
    ${layer("F", r.F)}${layer("V", r.V)}${layer("C", r.C)}
    <td class="td-num">${bookStr}</td>
    <td class="td-num ${r.coverage < 75 ? "gap" : ""}">${r.coverage}</td>
    <td class="td-plot">${plotIconCell(r.ticker)}</td>
  </tr>`;
}

// Clickable chart glyph for a table row. Disabled (greyed) when the ticker has
// no price history in plot_history.json. Clicking opens the Plot tab with the
// ticker selected.
function plotIconCell(ticker) {
  const has = PLOT_HISTORY && PLOT_HISTORY[ticker];
  const svg =
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" ' +
    'stroke="currentColor" stroke-width="1.4" stroke-linecap="round" ' +
    'stroke-linejoin="round" aria-hidden="true">' +
    '<polyline points="1,15 1,1"/><polyline points="1,15 15,15"/>' +
    '<polyline points="2,11 6,6 9,9 14,2"/></svg>';
  if (!has) {
    return `<span class="plot-ico plot-ico-off" title="No price history">${svg}</span>`;
  }
  return `<button type="button" class="plot-ico" title="Plot ${ticker}" ` +
         `onclick="openPlotFor('${ticker}')">${svg}</button>`;
}

// Reflect the active sort key/direction in the header arrows.
function syncHead() {
  document.querySelectorAll("#thead th").forEach(th => {
    const on = th.dataset.key === state.sortKey;
    th.classList.toggle("sorted", on);
    const arrow = th.querySelector(".th-arrow");
    arrow.textContent = on ? (state.sortDir === -1 ? "▼" : "▲") : "";
  });
}

function render() {
  // Toggle between the data table, the Plot tab, and About.
  const isAbout = state.view === "about";
  const isPlot = state.view === "plot";
  document.getElementById("dashboardView").hidden = isAbout || isPlot;
  document.getElementById("aboutView").hidden = !isAbout;
  const plotView = document.getElementById("plotView");
  if (plotView) plotView.hidden = !isPlot;
  if (isAbout) return;
  if (isPlot) { renderPlot(); return; }

  let rows = [...state.data];
  if (state.heldOnly) rows = rows.filter(r => r.held);
  if (state.wave !== "ALL") rows = rows.filter(r => r.wave === state.wave);
  if (state.q) rows = rows.filter(r => r.ticker.toUpperCase().includes(state.q));
  rows = sortRows(rows);

  const tbody = document.getElementById("tbody");
  const empty = document.getElementById("empty");
  tbody.innerHTML = rows.map(row).join("");
  empty.hidden = rows.length > 0;
  syncHead();
}

// ==========================================================================
// PLOT TAB — interactive multi-ticker price chart (client-side SVG)
// ==========================================================================

// Called by a table row's plot glyph: switch to the Plot tab and select the
// ticker (adding it to any existing overlay).
function openPlotFor(ticker) {
  if (!PLOT_HISTORY[ticker]) return;
  plotState.selected.add(ticker);
  const tab = document.querySelector('.tab[data-view="plot"]');
  if (tab) tab.click();       // click() runs wireControls -> sets view + render
  else { state.view = "plot"; render(); }
}

// Wire the Plot tab's search box and range buttons once at boot.
function wirePlotControls() {
  const search = document.getElementById("plotSearch");
  if (search) search.oninput = e => {
    plotState.q = e.target.value.trim().toUpperCase();
    renderPlotList();
  };
  document.querySelectorAll(".plot-range-btn").forEach(btn => {
    btn.onclick = () => {
      plotState.range = btn.dataset.range;
      syncPlotRange();
      drawPlot();
    };
  });
  const clear = document.getElementById("plotClear");
  if (clear) clear.onclick = () => {
    plotState.selected.clear();
    renderPlotList();
    drawPlot();
  };
  syncPlotRange();
}

function syncPlotRange() {
  document.querySelectorAll(".plot-range-btn").forEach(btn =>
    btn.classList.toggle("plot-range-on", btn.dataset.range === plotState.range));
}

// Full Plot-tab render: side checkbox list + chart.
function renderPlot() {
  renderPlotList();
  drawPlot();
}

// The left-hand checkbox panel: every ticker with price history, filtered by
// the plot search box, held/selected names first.
function renderPlotList() {
  const box = document.getElementById("plotList");
  if (!box) return;
  const heldSet = new Set(state.data.filter(r => r.held).map(r => r.ticker));
  let names = Object.keys(PLOT_HISTORY);
  if (plotState.q) names = names.filter(t => t.toUpperCase().includes(plotState.q));
  // Sort: selected first, then held, then alphabetical.
  names.sort((a, b) => {
    const sa = plotState.selected.has(a), sb = plotState.selected.has(b);
    if (sa !== sb) return sa ? -1 : 1;
    const ha = heldSet.has(a), hb = heldSet.has(b);
    if (ha !== hb) return ha ? -1 : 1;
    return a.localeCompare(b);
  });
  box.innerHTML = names.map(t => {
    const on = plotState.selected.has(t) ? " checked" : "";
    const held = heldSet.has(t) ? ' <span class="plot-held">held</span>' : "";
    return `<label class="plot-check"><input type="checkbox" value="${t}"${on}>` +
           `<span>${t}</span>${held}</label>`;
  }).join("") ||
    '<div class="plot-empty">No tickers match.</div>';
  box.querySelectorAll("input[type=checkbox]").forEach(cb => {
    cb.onchange = () => {
      if (cb.checked) plotState.selected.add(cb.value);
      else plotState.selected.delete(cb.value);
      updatePlotCount();
      drawPlot();
    };
  });
  updatePlotCount();
}

function updatePlotCount() {
  const count = document.getElementById("plotCount");
  if (count) count.textContent = `${plotState.selected.size} selected`;
}

// Slice a series to the current range window.
function plotWindow(entry) {
  const days = PLOT_RANGE_DAYS[plotState.range];
  const t = entry.t, c = entry.c;
  if (days == null) return { t: t.slice(), c: c.slice() };
  const last = new Date(t[t.length - 1] + "T00:00:00Z").getTime();
  const cutoff = last - days * 86400000;
  const ot = [], oc = [];
  for (let i = 0; i < t.length; i++) {
    if (new Date(t[i] + "T00:00:00Z").getTime() >= cutoff) { ot.push(t[i]); oc.push(c[i]); }
  }
  if (!ot.length) { ot.push(t[t.length - 1]); oc.push(c[c.length - 1]); }
  return { t: ot, c: oc };
}

// Pick a "nice" gridline step covering `span` in at most `maxTicks` steps.
// Rounds up to the nearest 1/2/5 × 10ⁿ, floored at 10 so the axis is always in
// clean 10%+ increments (0,10,20,… / 0,20,40,… / 0,50,100,…).
function niceStep(span, maxTicks) {
  const raw = Math.max(span, 1) / Math.max(maxTicks, 1);
  const pow = Math.pow(10, Math.floor(Math.log10(raw)));
  const norm = raw / pow;           // 1..10
  const nice = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
  return Math.max(nice * pow, 10);  // never finer than 10%
}

const MON_ABBR = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];

// Build ~10 x-axis ticks as calendar month labels (JAN25, JUN, …) landing on
// aligned month boundaries, rather than raw data dates. The month step is
// chosen so a wide window gets ~10 ticks (5y → semiannual: JAN & JUN each year;
// 2y → every 2 months; 1y → monthly). The year is only shown on January ticks
// (JAN25) so year boundaries stand out; other ticks show the month alone (JUN).
// Short windows (≤ ~2 months) fall back to day labels ("5 JAN"). Each tick is
// mapped to the nearest data index so it aligns with the plotted points.
// Returns [{ i, label }] sorted by index.
function xAxisTicks(refDates) {
  const n = refDates.length;
  if (n <= 1) return [{ i: 0, label: refDates[0] || "" }];
  const rd = refDates.map(d => new Date(d + "T00:00:00Z"));
  const first = rd[0], last = rd[n - 1];
  const spanDays = (last - first) / 86400000;

  // Nearest data index to a given timestamp (binary search + neighbour check).
  const nearest = t => {
    let lo = 0, hi = n - 1;
    while (lo < hi) { const m = (lo + hi) >> 1; if (rd[m].getTime() < t) lo = m + 1; else hi = m; }
    if (lo > 0 && Math.abs(rd[lo - 1].getTime() - t) < Math.abs(rd[lo].getTime() - t)) lo--;
    return lo;
  };

  // Short window: day-level labels, ~7 evenly spaced by index.
  if (spanDays <= 62) {
    const count = Math.min(7, n);
    const out = [];
    for (let k = 0; k < count; k++) {
      const i = Math.round(k * (n - 1) / (count - 1 || 1));
      const dt = rd[i];
      out.push({ i, label: dt.getUTCDate() + " " + MON_ABBR[dt.getUTCMonth()] });
    }
    return dedupeByIndex(out);
  }

  // Longer window: aligned month-boundary ticks. Pick the smallest month step
  // that keeps the tick count ≤ 12 (≈ 10 target).
  const spanMonths = (last.getUTCFullYear() - first.getUTCFullYear()) * 12 +
                     (last.getUTCMonth() - first.getUTCMonth());
  const STEPS = [1, 2, 3, 6, 12, 24, 60];
  let step = STEPS[STEPS.length - 1];
  for (const s of STEPS) { if (spanMonths / s <= 10) { step = s; break; } }
  // Which months of the year get a tick, per step (6 → JAN & JUN as requested).
  const MOY = { 1: [0,1,2,3,4,5,6,7,8,9,10,11], 2: [0,2,4,6,8,10],
                3: [0,3,6,9], 6: [0,5], 12: [0], 24: [0], 60: [0] };
  const months = MOY[step] || [0];
  const yearStep = step >= 12 ? step / 12 : 1;
  const tol = 20 * 86400000;   // include boundaries just outside the window
  const out = [];
  for (let y = first.getUTCFullYear(); y <= last.getUTCFullYear(); y += yearStep) {
    for (const m of months) {
      const t = Date.UTC(y, m, 1);
      if (t < first.getTime() - tol || t > last.getTime() + tol) continue;
      out.push({ i: nearest(t),
                 label: m === 0 ? MON_ABBR[0] + String(y).slice(-2) : MON_ABBR[m] });
    }
  }
  return dedupeByIndex(out);
}

// Drop ticks that collapse onto the same data index (keep the first), sorted.
function dedupeByIndex(ticks) {
  const seen = new Set(), out = [];
  ticks.sort((a, b) => a.i - b.i);
  for (const t of ticks) { if (!seen.has(t.i)) { seen.add(t.i); out.push(t); } }
  return out;
}

// Draw the SVG chart for the selected tickers, rebased to % change.
function drawPlot() {
  const svg = document.getElementById("plotSvg");
  const legend = document.getElementById("plotLegend");
  if (!svg) return;
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  if (legend) legend.innerHTML = "";

  const W = 900, H = 460, padL = 56, padR = 18, padT = 18, padB = 40;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  const NS = "http://www.w3.org/2000/svg";
  const mk = (tag, attrs) => {
    const el = document.createElementNS(NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    return el;
  };

  const sel = [...plotState.selected].filter(t => PLOT_HISTORY[t]);
  if (!sel.length) {
    const msg = mk("text", { x: W / 2, y: H / 2, "text-anchor": "middle",
      fill: "#8b98a5", "font-size": "15" });
    msg.textContent = "Select one or more tickers to plot.";
    svg.appendChild(msg);
    return;
  }

  // Build rebased (% from window start) series; track global min/max + longest.
  const series = [];
  let gmin = Infinity, gmax = -Infinity, refDates = null, maxLen = 0;
  sel.forEach((tk, i) => {
    const win = plotWindow(PLOT_HISTORY[tk]);
    const base = win.c[0];
    const pct = win.c.map(v => base ? (v / base - 1) * 100 : 0);
    for (const p of pct) { if (p < gmin) gmin = p; if (p > gmax) gmax = p; }
    if (win.t.length > maxLen) { maxLen = win.t.length; refDates = win.t; }
    series.push({ ticker: tk, pct, color: PLOT_COLORS[i % PLOT_COLORS.length] });
  });
  if (!isFinite(gmin)) return;

  // Buy zone: only shown when EXACTLY ONE ticker is selected (a band is an
  // absolute price range, meaningless overlaid across rebased multi-name %).
  // Convert the absolute low/high to % of THIS series' window base (matching
  // the chart's rebase) and widen the axis so the band is always visible.
  let bandPct = null;
  if (sel.length === 1) {
    const tk = sel[0];
    const z = BUY_ZONES[tk];
    if (z && isFinite(z.low) && isFinite(z.high)) {
      const base = plotWindow(PLOT_HISTORY[tk]).c[0];
      if (base) {
        const lo = (z.low / base - 1) * 100;
        const hi = (z.high / base - 1) * 100;
        bandPct = { lo: Math.min(lo, hi), hi: Math.max(lo, hi),
                    source: z.source, low: z.low, high: z.high };
        if (bandPct.lo < gmin) gmin = bandPct.lo;
        if (bandPct.hi > gmax) gmax = bandPct.hi;
      }
    }
  }

  if (gmin === gmax) { gmin -= 1; gmax += 1; }

  // Snap the axis to a "nice" round step (1/2/5 × 10ⁿ, min 10%) so gridlines
  // land on tidy multiples — e.g. 0..40 → 0,10,20,30,40; 0..100 → 0,20,…,100 —
  // instead of arbitrary values. Bounds are rounded out to whole steps.
  const step = niceStep(gmax - gmin, 6);
  gmin = Math.floor(gmin / step) * step;
  gmax = Math.ceil(gmax / step) * step;

  const xOf = (i, n) => padL + (n <= 1 ? 0 : (i / (n - 1)) * (W - padL - padR));
  const yOf = v => padT + (1 - (v - gmin) / (gmax - gmin)) * (H - padT - padB);

  // Buy-zone shaded band (drawn FIRST so gridlines + the price line sit on top).
  // Green rectangle spanning the full plot width between the low/high % levels,
  // with a subtle top/bottom edge and a corner label naming the price range.
  if (bandPct) {
    const yHi = yOf(bandPct.hi);      // top edge (higher price = higher on chart)
    const yLo = yOf(bandPct.lo);      // bottom edge
    const bx = padL, bw = W - padL - padR;
    svg.appendChild(mk("rect", { x: bx, y: yHi, width: bw,
      height: Math.max(yLo - yHi, 1), fill: "#34d399", "fill-opacity": "0.12" }));
    svg.appendChild(mk("line", { x1: bx, x2: bx + bw, y1: yHi, y2: yHi,
      stroke: "#34d399", "stroke-width": 1, "stroke-opacity": "0.55" }));
    svg.appendChild(mk("line", { x1: bx, x2: bx + bw, y1: yLo, y2: yLo,
      stroke: "#34d399", "stroke-width": 1, "stroke-opacity": "0.55" }));
    const lbl = mk("text", { x: bx + bw - 6, y: yHi + 14, "text-anchor": "end",
      fill: "#34d399", "font-size": "11", "font-weight": "600" });
    const fmt = v => v >= 1000 ? v.toLocaleString("en-US", { maximumFractionDigits: 0 })
                               : (v >= 100 ? Math.round(v) : v);
    lbl.textContent = `BUY ZONE ${fmt(bandPct.low)}–${fmt(bandPct.high)}` +
      (bandPct.source === "manual" ? "" : " (auto)");
    svg.appendChild(lbl);
  }

  // Horizontal gridlines + % axis labels at each nice step (0% line emphasised).
  for (let val = gmin; val <= gmax + step * 1e-6; val += step) {
    const y = yOf(val);
    svg.appendChild(mk("line", { x1: padL, x2: W - padR, y1: y, y2: y,
      stroke: Math.abs(val) < 1e-6 ? "#3a4653" : "#212a33", "stroke-width": 1 }));
    const lbl = mk("text", { x: padL - 8, y: y + 4, "text-anchor": "end",
      fill: "#8b98a5", "font-size": "11" });
    lbl.textContent = (val > 0 ? "+" : "") + Math.round(val) + "%";
    svg.appendChild(lbl);
  }
  // Zero baseline for the rebase (0% at window start).
  if (gmin <= 0 && gmax >= 0) {
    const y0 = yOf(0);
    svg.appendChild(mk("line", { x1: padL, x2: W - padR, y1: y0, y2: y0,
      stroke: "#3a4653", "stroke-width": 1.2 }));
  }
  // X-axis: ~10 calendar month-boundary ticks (JAN25, JUN, …) with faint
  // gridlines, aligned to the plotted data points.
  if (refDates && refDates.length) {
    const n = refDates.length;
    const ticks = xAxisTicks(refDates);
    ticks.forEach(({ i, label }) => {
      const x = xOf(i, n);
      svg.appendChild(mk("line", { x1: x, x2: x, y1: padT, y2: H - padB,
        stroke: "#1a222b", "stroke-width": 1 }));
      const anchor = x <= padL + 2 ? "start" : (x >= W - padR - 2 ? "end" : "middle");
      const tx = mk("text", { x, y: H - padB + 20, "text-anchor": anchor,
        fill: "#8b98a5", "font-size": "11" });
      tx.textContent = label;
      svg.appendChild(tx);
    });
  }

  // Draw each series + a legend chip with its window return.
  series.forEach(s => {
    const n = s.pct.length;
    let d = "";
    for (let i = 0; i < n; i++)
      d += (i === 0 ? "M" : "L") + xOf(i, n).toFixed(1) + "," + yOf(s.pct[i]).toFixed(1) + " ";
    svg.appendChild(mk("path", { d: d.trim(), fill: "none",
      stroke: s.color, "stroke-width": 1.7 }));
    if (legend) {
      const last = s.pct[s.pct.length - 1];
      const chip = document.createElement("span");
      chip.className = "plot-legend-chip";
      chip.innerHTML =
        `<span class="plot-swatch" style="background:${s.color}"></span>` +
        `<b>${s.ticker}</b> ` +
        `<span style="color:${last >= 0 ? "#34d399" : "#f87171"}">` +
        `${last >= 0 ? "+" : ""}${last.toFixed(1)}%</span>`;
      legend.appendChild(chip);
    }
  });
}

boot();
