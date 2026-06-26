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
- `fwd_rev_growth` / `fwd_eps_growth` — analyst **3Y** growth forecasts, %.
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
- `peg` — blank if n/a. When blank, P6 falls back to `ps_ratio` vs growth.
- `ps_ratio` — price/sales, ttm. Valuation fallback for P6 so loss-makers /
  pre-revenue names (no PEG) still get a valuation score instead of neutral.
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

# 3. allocation + watchlist invariants
PORTFOLIO_USE=ai python3 -c "import portfolio.AI_allocations as m; \
assert m.verify_allocations() is None; assert m.validate_watchlist() == []; \
print('PASS')"
```

- `verify_allocations()` (AI_allocations.py) — asserts baskets/TARGET_WEIGHTS
  sum to 1.0; returns `None` on pass.
- `validate_watchlist()` — returns `[]` (empty list) on pass.
- Also confirm no **unexpected** `data = -` rows remain in the output (only the
  intentional no-fundamentals trusts like SRUUF should show `-`).

### 7. Notes on interpreting results

- **SMHV.SW is excluded** from scoring throughout (fixed windfall, semi index).
- The default Growth/8-Point quadrant is anti-momentum and mis-grades DCA
  compounders into AVOID by design — use `--by-strategy` to grade DCA on
  quality+valuation instead. See `scoring/README.md` for the rationale.

## Colab usage

After `git pull`, call `importlib.reload()` on `config.*` and `portfolio.*` —
Colab caches modules. Bash-style `VAR=val python ...` does not work in a Python
cell; set `os.environ["PORTFOLIO_USE"] = "ai"` then run the script with `!`.
