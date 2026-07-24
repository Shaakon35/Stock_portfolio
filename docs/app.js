/* AI Allocation — Conviction Dashboard
   Loads conviction.json (produced by scoring/score_holdings.py --json) and
   renders a filterable, sortable card grid. No build step, no dependencies. */

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

const state = {
  data: [], view: "held", wave: "ALL", q: "", sort: "conv",
};

// conviction -> accent color for the card edge bar
function convColor(c) {
  if (c >= 7.5) return "#34d399";      // strong — emerald
  if (c >= 6.0) return "#22d3ee";      // solid — cyan
  if (c >= 4.5) return "#f5c451";      // middling — amber
  return "#f87171";                    // weak — red
}

function convTextColor(c) {
  if (c >= 7.5) return "#34d399";
  if (c >= 6.0) return "#7dd3fc";
  if (c >= 4.5) return "#f5c451";
  return "#f87171";
}

async function boot() {
  let payload;
  try {
    const res = await fetch("conviction.json", { cache: "no-store" });
    payload = await res.json();
  } catch (e) {
    document.getElementById("grid").innerHTML =
      '<p class="empty">Could not load conviction.json. ' +
      'Run <code>PORTFOLIO_USE=ai python3 scoring/score_holdings.py --json</code> first.</p>';
    return;
  }
  state.data = payload.records || [];
  document.getElementById("navMeta").textContent =
    `${payload.count} names · ${payload.held_count} held`;
  document.getElementById("footMeta").textContent =
    `Generated ${payload.generated_utc} · source ${payload.csv}`;

  buildWaveChips();
  buildStats();
  wireControls();
  render();
}

function currentSet() {
  let rows = state.data;
  if (state.view === "held") rows = rows.filter(r => r.held);
  else if (state.view === "watch") rows = rows.filter(r => !r.held);
  // "all" -> everything
  return rows;
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
    ["Watchlist", state.data.filter(r => !r.held).length],
  ];
  document.getElementById("statBar").innerHTML = stats.map(([l, v]) =>
    `<div class="stat"><div class="stat-val">${v}</div>` +
    `<div class="stat-lab">${l}</div></div>`).join("");
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
  document.getElementById("search").oninput = e => {
    state.q = e.target.value.trim().toUpperCase(); render();
  };
  document.getElementById("sortBy").onchange = e => {
    state.sort = e.target.value; render();
  };
}

function sortRows(rows) {
  const s = state.sort;
  const num = k => (a, b) => (b[k] ?? 0) - (a[k] ?? 0);
  if (s === "ticker") return rows.sort((a, b) =>
    a.ticker.localeCompare(b.ticker));
  return rows.sort(num(s));
}

function card(r) {
  const bar = convColor(r.conv);
  const badges = [];
  const gc = GRADE_CLASS[r.grade] || "b-mut";
  badges.push(`<span class="badge ${gc}">${r.grade}</span>`);
  badges.push(`<span class="badge b-mut">${STRAT_LABEL[r.strategy] || r.strategy}</span>`);
  if (r.wave === "ET") badges.push(`<span class="badge b-mut">via ETF</span>`);
  if (r.peak) badges.push(`<span class="badge b-amber">PEAK?</span>`);
  if (r.coverage < 75) badges.push(`<span class="badge b-red">GAP ${r.coverage}%</span>`);

  const layer = (k, v) => {
    const bind = r.binding === k ? " bind" : "";
    return `<div class="layer-row">
      <span class="layer-key${bind}">${k}</span>
      <span class="layer-track"><span class="layer-fill lf-${k}" style="width:${v * 10}%"></span></span>
      <span class="layer-val">${v.toFixed(1)}</span>
    </div>`;
  };

  const bookStr = r.held
    ? `Book <b>${r.book_pct.toFixed(2)}%</b>`
    : `<span style="color:var(--text-mut)">watch-only</span>`;

  const yhTkr = r.ticker; // yahoo accepts the suffixed form directly
  return `<article class="card" style="--bar:${bar}">
    <div class="card-top">
      <div>
        <div class="card-tkr">${r.ticker}</div>
        <div class="card-wave">${WAVE_NAMES[r.wave] || r.wave}</div>
      </div>
      <div class="conv-badge">
        <div class="conv-num" style="color:${convTextColor(r.conv)}">${r.conv.toFixed(2)}</div>
        <div class="conv-lab">CONVICTION</div>
      </div>
    </div>
    <div class="badges">${badges.join("")}</div>
    <div class="layers">
      ${layer("F", r.F)}${layer("V", r.V)}${layer("C", r.C)}
    </div>
    <div class="card-foot">
      <span class="card-book">${bookStr}</span>
      <a class="yh" href="https://finance.yahoo.com/quote/${yhTkr}" target="_blank" rel="noopener">Yahoo ↗</a>
    </div>
  </article>`;
}

function render() {
  let rows = currentSet();
  if (state.wave !== "ALL") rows = rows.filter(r => r.wave === state.wave);
  if (state.q) rows = rows.filter(r => r.ticker.toUpperCase().includes(state.q));
  rows = sortRows([...rows]);

  const grid = document.getElementById("grid");
  const empty = document.getElementById("empty");
  grid.innerHTML = rows.map(card).join("");
  empty.hidden = rows.length > 0;
}

boot();
