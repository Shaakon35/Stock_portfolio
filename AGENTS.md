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
- The CSV starts with `#` comment lines (column legend + FX + proxy notes); the
  loader skips them. Keep that header current when conventions change.

### 2. Column schema

```
ticker,mktcap_b,fwd_rev_growth,ttm_rev_growth,fwd_eps_growth,gross_margin,
net_margin,fcf_positive,peg,pct_above_200dma,pct_below_52w_high,
eps_beat_rate,eps_beat_streak
```

- `mktcap_b` — market cap in **USD billions** (convert foreign, see FX below).
- `fwd_rev_growth` / `fwd_eps_growth` — analyst **3Y** growth forecasts, %.
- `ttm_rev_growth` — trailing-12m rev YoY %; blank = unknown (no re-accel bonus).
- `net_margin` — GAAP profit margin %, ttm. See operating-margin proxy rule.
- `fcf_positive` — `1` if trailing FCF > 0 else `0`.
- `peg` — blank if n/a.
- `pct_above_200dma` — `(price − 200DMA) / 200DMA × 100`; compute from the real
  price and 200-day MA (do **not** cap; the scoring bands clamp internally).
- `pct_below_52w_high` — currently left blank; P8 uses 200DMA distance.
- `eps_beat_rate` (0..1) / `eps_beat_streak` — blank = neutral. Seed only for
  well-documented serial beaters; source from each name's `/earnings/` page.

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
