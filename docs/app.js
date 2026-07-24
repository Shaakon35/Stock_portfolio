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

// Glossary of every acronym / term shown in the table or the methodology.
// Rendered into the About tab so the abbreviations are self-explanatory.
const GLOSSARY = [
  ["CONV", "Conviction — the headline 0–10 score. Higher = a stronger risk-adjusted case for owning the name now. Geometric mean of a reward and a safety term."],
  ["F", "Fundamentals layer (0–10, higher = safer). Business quality, momentum-neutral: margins, forward growth, FCF, margin trajectory and consistency."],
  ["V", "Valuation layer (0–10, higher = cheaper/fairer). PEG first, P/S-vs-growth fallback, plus distance above the 200-day moving average."],
  ["C", "Cycle layer (0–10, higher = earlier/less crowded). Position in the industry wave, chart extension, and whether the name sits on a supply bottleneck."],
  ["bind", "Binding layer — the lowest of F/V/C, i.e. the dominant risk. Counted a second time inside the safety term and flagged in the table."],
  ["8PT", "The 8-point entry screen (0–8): small + cheap + accelerating checks used for cycle/catalyst names. Rescaled to 0–10 inside the cycle conviction."],
  ["GROWTH", "The 0–10 growth score — how much the business can compound. Drives the reward term for cycle/catalyst names."],
  ["QUALITY", "The DCA quality score — durability of a buy-forever compounder. Replaces GROWTH in the DCA conviction variant."],
  ["RICHNESS", "The DCA price gate (0 = cheap … 1 = stretched). A rich name is bought slower, not skipped; it enters safety as (1 − richness)."],
  ["DCA", "Dollar-cost averaging — a proven compounder you buy on a schedule regardless of price. Graded on quality + valuation, not on being small/explosive."],
  ["CYCLE (strategy)", "A name bought for its position in an industry cycle — graded on the two-axis quadrant (where in the cycle, how cheap)."],
  ["CATALYST", "A name bought for a specific upcoming event; graded on whether the punt's upside is still intact."],
  ["LOTTERY", "A pre-revenue / single-event punt (Binary). High opacity is treated as a red flag, not a neutral."],
  ["book %", "The name's target weight in the portfolio book. Watch-only names have no book weight."],
  ["coverage / Data %", "Share of obtainable fundamentals actually present for the name. Below 75% the score is scaled down and a GAP flag shows."],
  ["GAP", "Coverage < 75% — the score rests on thin data and should be trusted less."],
  ["PEAK?", "A cyclical whose low PEG is fake-cheap on peak-cycle earnings while the chart is extended (the memory/storage trap). Cuts cycle CONV ×0.85."],
  ["HELD", "The name currently has a position in the book (book % > 0). Names without the flag are watch-only."],
  ["wave (W1–W7)", "The AI-allocation basket: W1 Silicon, W2 Power, W3 DC-Infra, W4 Cloud, W5 Software, W6 Spec, W7 Diversify. ET = surfaced via ETF look-through."],
  ["grade", "The strategy-aware verdict: PRIME / KEEP-DCA (buy), MOMENTUM / QUALITY (hold-ish), RICH (wait for a better price), AVOID / IMPAIRED (pass)."],
  ["200DMA", "200-day moving average of price. Distance above it measures chart extension — a proxy for how much optimism is already paid for."],
  ["PEG", "Price/earnings-to-growth ratio. Below ~1 looks cheap, but on a late-cycle name a sub-1 PEG is usually the peak-earnings trap (see PEAK?)."],
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
  { key: "binding",  label: "Bind",     align: "center", num: false },
  { key: "book_pct", label: "Book %",   align: "right",  num: true  },
  { key: "coverage", label: "Data %",   align: "right",  num: true  },
  { key: "flags",    label: "Flags",    align: "left",   num: false },
];

const state = {
  data: [], view: "stock", wave: "ALL", q: "", heldOnly: false,
  sortKey: "conv", sortDir: -1,   // -1 = descending, 1 = ascending
};

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
      '<tr><td colspan="12" class="empty">Could not load conviction.json. ' +
      'Run <code>PORTFOLIO_USE=ai python3 scoring/score_holdings.py --json</code> first.</td></tr>';
    return;
  }
  state.data = payload.records || [];
  document.getElementById("navMeta").textContent =
    `${payload.count} names · ${payload.held_count} held`;
  document.getElementById("footMeta").textContent =
    `Generated ${payload.generated_utc} · source ${payload.csv}`;

  buildWaveChips();
  buildStats();
  buildGlossary();
  buildHead();
  wireControls();
  render();
}

// Render the acronym glossary into the About tab.
function buildGlossary() {
  const dl = document.getElementById("glossary");
  if (!dl) return;
  dl.innerHTML = GLOSSARY.map(([term, def]) =>
    `<div class="gloss-row">
       <dt>${term}</dt>
       <dd>${def}</dd>
     </div>`).join("");
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
  const top = held.reduce((a, r) => r.conv > a.conv ? r : a, { conv: -1 });
  const book = held.reduce((s, r) => s + r.book_pct, 0);
  const stats = [
    ["Held names", held.length],
    ["Avg conviction", avg.toFixed(2)],
    ["Top", top.ticker ? `${top.ticker} ${top.conv.toFixed(1)}` : "—"],
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
  const gc = GRADE_CLASS[r.grade] || "b-mut";
  const flags = [];
  if (r.wave === "ET") flags.push(`<span class="badge b-mut">via ETF</span>`);
  if (r.peak) flags.push(`<span class="badge b-amber">PEAK?</span>`);
  if (r.coverage < 75) flags.push(`<span class="badge b-red">GAP</span>`);
  if (r.held) flags.push(`<span class="badge b-green">HELD</span>`);

  const layer = (k, v) =>
    `<td class="td-num td-layer"><span class="lcell">` +
    `<span class="ltrack"><span class="lbar lf-${k}" style="width:${v * 10}%"></span></span>` +
    `<b>${v.toFixed(1)}</b></span></td>`;

  const bookStr = r.held
    ? `${r.book_pct.toFixed(2)}`
    : `<span class="mut">—</span>`;

  return `<tr>
    <td class="td-tkr"><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" rel="noopener">${r.ticker}</a></td>
    <td class="mut">${r.wave}</td>
    <td>${STRAT_LABEL[r.strategy] || r.strategy}</td>
    <td><span class="badge ${gc}">${r.grade}</span></td>
    <td class="td-num td-conv" style="color:${convTextColor(r.conv)}"><b>${r.conv.toFixed(2)}</b></td>
    ${layer("F", r.F)}${layer("V", r.V)}${layer("C", r.C)}
    <td class="td-bind">${r.binding}</td>
    <td class="td-num">${bookStr}</td>
    <td class="td-num ${r.coverage < 75 ? "gap" : ""}">${r.coverage}</td>
    <td class="td-flags">${flags.join("") || '<span class="mut">—</span>'}</td>
  </tr>`;
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
  // Toggle between the data table and the static About/methodology view.
  const isAbout = state.view === "about";
  document.getElementById("dashboardView").hidden = isAbout;
  document.getElementById("aboutView").hidden = !isAbout;
  if (isAbout) return;

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

boot();
