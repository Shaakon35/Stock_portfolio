# AGENTS.md

Conventions for agents working in this repository. Keep changes aligned with
the patterns below.

## General

- **Never remove comments** from scripts, notebooks, or config unless explicitly
  asked. Comments are intentional documentation.
- **Two allocation modes**: `portfolio/allocations.py` (sector) vs
  `portfolio/AI_allocations.py` (AI waves W1–W6), selected with the
  `PORTFOLIO_USE=ai` environment variable. The scorer requires `PORTFOLIO_USE=ai`.
- **yfinance feed is date-corrupted** in this environment. Do not rely on live
  market fetches for reproducible output — use the committed dated snapshot
  (see below). Source fresh numbers from stockanalysis.com.
- Commits go to `main`. Add `Co-authored-by: Ona <no-reply@ona.com>`.
- **Branch protection (deliberate).** `main` is protected against **force-push**
  and **deletion** only. It intentionally does **NOT** require pull requests,
  because the data-refresh automation (the recurring `Refresh conviction data`
  commits) pushes straight to `main` — a PR requirement would break it. Do not
  enable "require a pull request before merging" on `main` unless the refresh bot
  is first given a bypass or routed through PRs. Feature branches may still be
  force-pushed (e.g. rebasing a PR branch); only `main` blocks it.

## Fundamentals-refresh workflow (scoring engine)

The scorer (`scoring/score_holdings.py`) is **deterministic** and reads market
data from a dated CSV snapshot, never live. Follow this exact procedure when
refreshing or extending the data.

### 1. File location & naming

- Snapshot lives at `scoring/fundamentals_<YYYY-MM-DD>.csv`.
- The engine auto-picks the **newest** `scoring/fundamentals_*.csv`.
- To refresh: copy the latest CSV to a new date and update the numbers; do not
  edit an old dated file in place once it represents a past snapshot.
- After updating the numbers, run `PORTFOLIO_USE=ai python3
  scoring/score_holdings.py --fill-ttm --watchlist` to (re)source the
  `ttm_rev_growth` scalar, the `rev_growth_hist` multi-year revenue series **and**
  the `net_margin_hist` margin-trajectory series in place — it preserves every
  other cell and the `#` header. This keeps the trend term (re-accel bonus /
  decel penalty) and the margin-expansion sub-score fed with current trailing
  data.
- The CSV starts with `#` comment lines (column legend + FX + proxy notes); the
  loader skips them. Keep that header current when conventions change.
- To add **new** AI-allocation names (held or watchlist) that are missing from
  the CSV, run `PORTFOLIO_USE=ai python3 scoring/score_holdings.py --sync-csv`.
  It appends a fully-populated row for each missing name in one pass: mechanical
  fields + `fwd_*` (nearest-FY consensus) from the scrape, **and** auto-fills the
  `ttm_rev_growth` / `rev_growth_hist` / `net_margin_hist` series for just the
  new rows (no separate `--fill-ttm` step; pass `--no-fill-ttm` to skip). It
  never edits existing rows (use `--overwrite` for that) and skips the
  source-corrupted / no-page names (`MU`/`SMHV.SW`/`SRUUF`) with a warning.
- **Coverage invariant — always wire new tickers into the watchlist too.** A CSV
  row is invisible to `score_holdings.py --by-strategy --watchlist` unless the
  name is also HELD (in a wave basket / `STRATEGY`) or present in
  `AI_allocations.py`'s `WATCHLIST`. After sourcing **any** new name into the
  CSV, add a matching `WATCHLIST` entry (schema: `strategy`/`pos`/`cagr`/`area`/
  `note`; `dca` for quality compounders, `cycle` for banks/energy/miners/
  industrials; reserve `catalyst`/`lottery`+`Binary` for true single-event/
  pre-revenue punts). Note the **direction** of `--sync-csv`: it back-fills CSV
  rows for names *already* referenced in the allocations/watchlist — it does not
  create watchlist entries, so a CSV-first batch will report `added 0` and still
  owes its `WATCHLIST` entries. Verify with the coverage check below.

### 2. Column schema

```
ticker,mktcap_b,fwd_rev_growth,ttm_rev_growth,fwd_eps_growth,gross_margin,
net_margin,fcf_positive,peg,ps_ratio,pct_above_200dma,pct_below_52w_high,
eps_beat_rate,eps_beat_streak,rev_growth_hist,net_margin_hist
```

(`rev_growth_hist` and `net_margin_hist` are appended last and are pipe-
separated, not plain numbers; they are parsed specially by the loader and sit
outside the numeric schema.)

- `mktcap_b` — market cap in **USD billions** (convert foreign, see FX below).
- `fwd_rev_growth` / `fwd_eps_growth` — analyst growth forecasts, %. The true
  multi-year **3Y** figure on the `/forecast/` page is `[PRO]`-paywalled, so
  `--sync-csv` auto-sources the **nearest-FY analyst consensus average** as a
  reproducible proxy (parsed from the page JSON `revenueGrowth`/`epsGrowth`
  `{"<FY>":{avg:..}}` block). Hand-edit the cell if you have a real 3Y number;
  `--overwrite` will refresh these from the live consensus (it lists them in
  `_SYNC_OVERWRITE_FIELDS`), so curated 3Y values are only safe without
  `--overwrite`.
- `ttm_rev_growth` — trailing-12m rev YoY %, sourced from the `/financials/`
  page (`revenueGrowth` JSON array, index 0). Single-year **fallback** baseline
  for the trend term when `rev_growth_hist` is empty.
- `rev_growth_hist` — trailing **full-FY** rev YoY % series, most-recent first,
  pipe-separated (e.g. CCJ `11.04|21.18|38.53|26.65|-18.06`). Sourced together
  with `ttm` by `score_holdings.py --fill-ttm` (touches only these two columns,
  preserves the `#` header and all other cells; appends the column to older
  CSVs). Its **median** is the baseline for the trend term:
  - fwd materially **above** the median → **re-acceleration bonus** (≤ +0.15)
  - fwd materially **below** the median → **deceleration penalty** (≤ −0.25)

  The multi-year median (not a single year) is deliberate: a one-year baseline
  mis-flags young hypergrowth names whose base year was spiky (CRDO printing
  206% off a tiny base would brand any forward number a "collapse") and misses
  quiet multi-year ramps (VRT 14→28%). Kept **outside** the numeric `FUND_FIELDS`
  schema, so it does not affect `data%`. Blank only for pre-revenue names with
  no FY history (no trend signal, score unchanged).

  **Base-effect damping (Option D):** the forecast `fwd` is a *forward 3Y CAGR*
  but the baseline is a *trailing per-year YoY*, so a name growing off a tiny
  base (ALAB 115/242/45, IONQ ~150 median) is arithmetically forced to a lower
  forward CAGR — maturation, not deceleration. The **deceleration penalty only**
  is scaled down when the trailing baseline exceeds `_TREND_HOT_BASE` (60%),
  fading to ~0 by `_TREND_HOT_FADE` (100 pts) beyond it. Genuine slowdowns off a
  normal base (CCJ, base 21 → full penalty) are unaffected; the re-acceleration
  bonus is never damped. See `_decel_damping` / the BASE-EFFECT DAMPING block in
  `score_holdings.py`.
- `net_margin_hist` — trailing **net-margin %** series (TTM first, then full FYs,
  most-recent first), pipe-separated (e.g. ANET `38.99|40.73|35.62|30.87|28.52`).
  Sourced together with the revenue series by `score_holdings.py --fill-ttm`
  (from the `/financials/` `profitMargin` array; preserves the `#` header and all
  other cells; appends the column to older CSVs). Powers the **margin-expansion**
  sub-score (`_margin_trend`): the mean of the **newer** half of the window minus
  the **older** half, in margin **points** —
  - newer margins materially **above** older → **expansion** (sub-score → 1.0)
  - within `±1` pt → **flat** (neutral 0.5)
  - newer materially **below** older → **compression** (sub-score → 0.0)

  Blended at modest weight (1.5) into the **FUND layer** and **DCA quality** so
  margin *direction* — not just level — feeds "is this a good business?". Margin
  *level* alone cannot tell a −5%→+1% turnaround from a 20%→11% melt; this term
  can. Kept **outside** the numeric `FUND_FIELDS` schema, so it does not affect
  `data%`. Blank when no margin history is available (sub-score dropped, weight
  redistributed — score unchanged for that name).
- `net_margin` — GAAP profit margin %, ttm. See operating-margin proxy rule.
- `fcf_positive` — `1` if trailing FCF > 0 else `0`.
- `peg` — blank if n/a. When blank, the cheapness leg falls back to `ps_ratio`
  vs growth. On **cyclicals**, an extreme `fwd_eps_growth` (>100%) is treated as
  a trough rebound and the PEG's cheapness is **damped toward neutral** — see the
  VAL cheapness model note below.
- `ps_ratio` — price/sales, ttm. **Two roles** (both in `_val_cheapness`): (1)
  the growth-relative fallback when `peg` is absent, AND (2) an **absolute,
  gross-margin-normalized P/S co-signal** that is *always* blended into the
  cheapness score even when a PEG exists — so a rich SALES multiple (e.g. BESI
  at ~22x) registers instead of being hidden by a low PEG. See the VAL cheapness
  model note below.
- `pct_above_200dma` — `(price − 200DMA) / 200DMA × 100`; compute from the real
  price and 200-day MA (do **not** cap; the scoring bands clamp internally).
  Blank for names too recently listed to have a 200DMA.
- `pct_below_52w_high` — left blank; the source has no clean field. P8 scores on
  the 200DMA leg alone when this is absent (see blank-handling note below).
- `eps_beat_rate` (0..1) / `eps_beat_streak` — blank = neutral. **The source has
  no scrapable estimate-vs-actual table** (`/earnings/` 404s; financials pages
  carry actuals but no consensus), so this is a deliberate *partial* field: seed
  only well-documented serial beaters, leave the rest blank. The surprise factor
  is a ±12% tie-breaker by design, never a dominant term.

**Blank handling (important):** a blank field is **not** scored as a faked
neutral 0.5. `_band()` returns `None` for missing input and `_blend()` then
*drops* that sub-score and redistributes its weight across the present metrics
(for CORE / DCA / established names), or *penalises* the gap (for speculative
W6 / Binary names, where opacity is itself a red flag). Each row's output shows
`data%` (coverage) and a `[GAP]` flag when coverage < 75%, so thin-data scores
can be trusted less.

`data%` counts only **obtainable** fields: the three structurally-unsourceable
columns (`pct_below_52w_high`, `eps_beat_rate`, `eps_beat_streak`) are excluded
from its denominator — see `_UNSOURCEABLE` in `score_holdings.py`. The source
has no scrapable field for them, so counting them would cap every name below
100% no matter how complete its real data is, making `[GAP]` fire on
fully-sourced names. With them excluded, a fully-sourced name reads ~100% and
`[GAP]` means genuinely thin data (pre-revenue lottery names, the SRUUF
commodity trust). This affects only the coverage metric, not the scoring —
those fields are still scored whenever seeded by hand.

(`ttm_rev_growth` was formerly in this list but is in fact sourceable from the
`/financials/` JSON, so it is now a real, counted field — see `--fill-ttm`
above. It powers the deceleration penalty.)

### 3. Sourcing from stockanalysis.com

- US names: `https://stockanalysis.com/stocks/<TICKER>/statistics/`
- Foreign names: `https://stockanalysis.com/quote/<exch>/<TICKER>/statistics/`
  - Korea (KRX): `quote/krx/<code>/` — e.g. `000660` (SK Hynix), `005930` (Samsung)
  - Hong Kong: `quote/hkg/<code>/` — e.g. `1810` (Xiaomi)
  - Xetra: `quote/etr/<TICKER>/` · Amsterdam: `quote/ams/<TICKER>/`
- A `404` means no statistics page exists (e.g. **SRUUF**, a physical-commodity
  trust with no company fundamentals). Omit such names from the CSV — they
  correctly fall back to `data = -` (scored on tags/forecast only).
- If a page 4xx/5xx errors three times, stop — do not loop.

### 4. FX conversion (mktcap to USD billions)

Convert the local-currency market cap using approximately:

- EUR ≈ 1.08 USD
- KRW ≈ 1350 per USD
- HKD ≈ 7.8 per USD

Record the rates used in the CSV header so the snapshot is reproducible.

### 5. Operating-margin proxy rule (GAAP-distorted names)

When a name's **GAAP net margin** is distorted by one-off items (large
fair-value swings, pretax gains, tax effects), use the **operating margin** in
the `net_margin` column instead, so the score reflects true profitability.
Names this has applied to: IONQ, NBIS, WDC, APLD. Note the substitution in the
CSV header. For pre-/near-pre-revenue names (e.g. SMR, NNE, ASTS) leave
`net_margin` blank → the engine treats it as neutral.

### 6. Validation gate (run before committing)

All must pass:

```bash
# 1. compiles
python3 -m py_compile scoring/score_holdings.py

# 2. deterministic — two runs must be byte-identical
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --by-strategy --watchlist > /tmp/r1.txt 2>&1
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --by-strategy --watchlist > /tmp/r2.txt 2>&1
diff /tmp/r1.txt /tmp/r2.txt   # must be empty

# 3. allocation + watchlist invariants + CSV<->WATCHLIST coverage
PORTFOLIO_USE=ai python3 -c "import portfolio.AI_allocations as m, scoring.score_holdings as S; \
assert m.verify_allocations() is None; assert m.validate_watchlist() == []; \
held=set().union(*[set(b.keys()) for _,b in m.ALL_BASKETS])|set(m.STRATEGY.keys()); \
csv=set(dict(S.load_fundamentals(S.default_csv())).keys()); \
miss=csv-set(m.WATCHLIST)-held; assert not miss, f'uncovered CSV tickers: {sorted(miss)}'; \
print('PASS')"
```

- `verify_allocations()` (AI_allocations.py) — asserts the per-ticker book
  percentages total 100% and the derived `TARGET_WEIGHTS` total 1.0; returns
  `None` on pass. **NOTE (2026-06 model change):** baskets now hold DIRECT book
  percentages (e.g. `"AMZN": 2.0` == 2.0% of book), and `TARGET_WEIGHTS` is
  AUTO-DERIVED as each wave's ticker-sum / 100 — it is no longer hand-edited. To
  change a holding's weight, edit its number in the basket; the wave total and
  `TARGET_WEIGHTS` follow automatically. The invariant is on the GRAND total
  across all baskets (= 100%), not on each basket summing to 1.0.
- `validate_watchlist()` — returns `[]` (empty list) on pass.
- **CSV ↔ WATCHLIST coverage** — every CSV ticker must be HELD or in `WATCHLIST`;
  the gate asserts the uncovered set is empty. A fresh batch of names is not done
  until each has a `WATCHLIST` entry (see §1 coverage invariant). Watchlist names
  *without* a CSV row are fine (the no-fundamentals monitors).
- Also confirm no **unexpected** `data = -` rows remain in the output (only
  intentional no-fundamentals names — a physical-commodity trust with no company
  financials page — should show `-`).

### 7. Notes on interpreting results

- **VAL cheapness model (`_val_cheapness` in `score_holdings.py`).** The VAL
  layer and the 8-Point P6 share ONE cheapness computation so they can never
  drift. It combines two legs, then softens the result for cyclicals:
  1. **PEG-first leg** (P/S-vs-growth fallback when no PEG). On a **cyclical**,
     an extreme `fwd_eps_growth` (>`_TROUGH_EPS_HOT`=100%) is a trough rebound
     that mechanically crushes PEG toward zero, so `_trough_peg_damping` pulls
     that PEG cheapness toward neutral (fades to a `_TROUGH_PEG_FLOOR`=0.2
     multiplier by +`_TROUGH_EPS_FADE`=100pts). This mirrors the trend-term
     base-effect damping; the DOWNSIDE (cheapness-reducing) direction only, and
     never non-cyclicals (a stable name at 100%+ EPS growth is a real
     hypergrower, not a trough).
  2. **Absolute P/S co-signal** (`_abs_ps_cheapness`) — ALWAYS blended in (weight
     `_VAL_ABSPS_W`=1.0 vs `_VAL_PEG_W`=1.6 for the PEG leg), so a rich SALES
     multiple registers even when the PEG looks cheap. P/S is **normalized by
     gross margin** (`_ABSPS_GROSS_BASE`=50) — a stable through-cycle proxy, NOT
     growth — so a 90%-gross SaaS name is fairly allowed a higher multiple than a
     40%-gross hardware name. Bands (`_ABSPS_LO`=3 → cheap, `_ABSPS_HI`=20 →
     expensive) are calibrated to the book's own distribution of the normalized
     ratio.
  Cyclicals then get the whole score softened toward neutral (`_CYCLICAL_SOFTEN`
  =0.6). Motivation: BESI screened VAL 8.8 / #1-conviction on a PEG of 0.54 that
  existed only because of 161% trough-rebound EPS growth, while trading at ~22x
  sales — the P/S co-signal + trough damping drop it to a realistic VAL ~7.0.
- **`[MARG?]` flag (`margin_flag`).** Annotation only (changes no score, like
  `[PEAK?]`). Fires when an **Early / Early-Mid** cycle name has a **compressing**
  net-margin trajectory (`_margin_trend` ≤ `_MARGIN_FLAG_MAX`=0.4) — the cycle
  tag and the margin data disagree (thesis unwinding or a stale tag). Reuses the
  margin series already in the CSV, so it needs no new data. Shown in both
  by-strategy tables, the main table, and `docs/conviction.json` (`marg` field).

- **SMHV.SW is excluded** from scoring throughout (fixed windfall, semi index).
  Its **constituents** are surfaced via ETF look-through instead: each top-10
  holding (MU/AMD/AVGO/INTC/TSM/ASML/NVDA/LRCX/AMAT/TXN) is shown with `wv=ET`
  and a `book%` equal to its weight inside SMHV × SMHV's 37.5% book weight (e.g.
  MU 14.33% × 37.5% ≈ 5.4%, TSM ≈ 2.8%). The look-through table is
  `ETF_LOOK_THROUGH["SMHV.SW"]` in `portfolio/allocations.py`; refresh it from
  the ETF fact sheet when holdings drift. `ET` rows are **excluded from the wave
  averages** so they are not double-counted against SMHV itself. MU has a
  **HAND-CURATED** CSV row: stockanalysis.com's MU snapshot is source-corrupted
  (serves an AI-designer profile — ~$1.1T mktcap / 72% gross / 56% net / $90B
  rev / PEG 0.04, physically impossible for a memory maker), so its row is
  populated by hand from real, peer-calibrated Micron figures (mktcap ~$130B;
  gross ~40% / net ~24% in line with SK Hynix / WDC / STX peaks; PEG ~0.5; P/S
  ~3.5; real FY YoY series incl. the FY23 memory crash −49.7%). See the
  `# MU (hand-curated)` note in the snapshot header. This is enforced in code:
  `MU` is in `_SOURCE_CORRUPT` (`score_holdings.py`), which feeds BOTH the
  `--sync-csv` skip list AND the `--fill-ttm` exclusion, so neither scraper ever
  overwrites the hand-curated row — each prints an explicit `SKIPPING MU …`
  warning instead. **Update MU by hand only.**
- The default Growth/8-Point quadrant is anti-momentum and mis-grades DCA
  compounders into AVOID by design — use `--by-strategy` to grade DCA on
  quality+valuation instead. See `scoring/README.md` for the rationale.

- **Cycle tags (`CYCLE_POS`) must be explicit for every held `cycle`-strategy
  name.** `cycle_of()` resolves a name's wave position from `CYCLE_POS` first,
  then a watchlist `pos`, then falls back to `"Mid"`. For a **`cycle`** trade the
  wave position IS the thesis, so a silent `"Mid"` default makes its CYCLE layer
  (`C`) and 8-Point P5 meaningless — and can hide a genuinely **Late/extended**
  name. Held names always have `wl_pos=None`, so their only source of a real tag
  is `CYCLE_POS`. `untagged_cycle_holdings()` returns any held `cycle` name
  missing from `CYCLE_POS`, and `build_results` prints a stderr `WARNING:` when
  that set is non-empty — keep it empty. Held **`dca`/`catalyst`** names are
  intentionally allowed to default to `"Mid"` (cycle position is not a meaningful
  axis for a buy-forever compounder; this is why the top DCA cohort clusters at
  `C≈5.9`). When adding a new `cycle` holding, add a deliberate
  Early/Early-Mid/Mid/Mid-Late/Late tag to `CYCLE_POS` in the same change.

## Weekly conviction-movers email

The weekly refresh (`.github/workflows/refresh-data.yml`) emails a themed HTML
report of what moved in the `conv` score since the previous weekly run. Built by
`scoring/report_conviction_movers.py` (pure stdlib), which diffs the freshly
committed `docs/conviction.json` against the previous `Refresh conviction data`
commit (auto-resolved from git history — no separate datastore).

- **Inclusion**: held names are reported even on small drift (`>7` bar 0.15);
  non-held names only when they move a lot (bar 0.40); any flag flip
  (peak/marg/grade/binding) is always reported. Thresholds are constants at the
  top of the script. The top-`N` `>7` movers get a layer-attribution "zoom".
- **Theme**: the report inlines the dashboard's `:root` CSS tokens, parsed from
  `docs/style.css` at build time, so it tracks the site's look (single source of
  truth). The file is fully self-contained (no external `<link>`/fonts), sent as
  the email **attachment**; a trimmed inline body makes it phone-readable.
- **Cadence**: sends only on the weekly `schedule` and manual `workflow_dispatch`
  runs — never on the allocation-edit republish workflow. The send step is
  `continue-on-error`, so an SMTP failure never fails the data refresh.
- **Required repo secrets** (Settings → Secrets and variables → Actions):
  - `MAIL_USERNAME` — the Gmail address that both sends and receives the report.
  - `MAIL_PASSWORD` — a Gmail **App Password** for that account (2-Step
    Verification must be on; a normal password will not work).

  If the secrets are absent the send step simply fails soft (skipped/errored)
  without affecting the committed data.
- **Local preview**: `python3 scoring/report_conviction_movers.py --selftest`
  diffs two committed snapshots and writes `/tmp/movers_selftest.html`. To render
  a specific pair: `--current <file> --previous <(git show <sha>:docs/conviction.json)
  --out-file /tmp/report.html`.

## Colab usage

After `git pull`, call `importlib.reload()` on `config.*` and `portfolio.*` —
Colab caches modules. Bash-style `VAR=val python ...` does not work in a Python
cell; set `os.environ["PORTFOLIO_USE"] = "ai"` then run the script with `!`.
