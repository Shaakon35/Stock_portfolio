# Cycle rolling-window backtest

Tests whether the cycle model's edge survives across **different years**, not
just one bull-market window.

## Why

The main dataset (`smid_optimization_data.csv`) measures 12/24/36-month returns
from a single base date (~today). That blends horizons and lives inside one
regime, so the model's edge looks more stable than it may be.

This backtest instead uses **same-horizon rolling windows**: 3-year holds from
several base years (2020→2023, 2021→2024, 2022→2025, 2023→2026). Each window is
a clean, comparable cohort. If the top-ranked names beat the bottom-ranked names
in *every* window, the edge is real. If the spread flips sign year to year, the
model is just riding whatever theme was hot.

## Step 1 — Fetch the data (slow; run once)

Cycle-only, 3-year holds, four base years. Writes to a **separate** CSV
(`output/cycle_windows.csv`) so it never touches your existing data.

```python
from portfolio.smid_data_fetcher import fetch_windows

fetch_windows(
    base_years=(2020, 2021, 2022, 2023),  # -> 2023, 2024, 2025, 2026 ends
    hold_years=3,
    strategies=("cycle",),
)
```

Notes:
- ~413 cycle tickers × 4 windows ≈ **1,600 fetches**. Expect 30–60+ min on
  Colab depending on rate limits. It saves after each window and is
  **resume-safe** — re-run to continue if interrupted.
- `2023→2026` uses the most recent realized 3 years.
- Add `max_tickers=20` for a quick smoke test first.
- Stocks that delisted within a window are recorded as −100% (no survivorship
  bias).

## Step 2 — Analyze

```python
from portfolio.cycle_windows import run
run(top_frac=0.05)   # top 5% vs bottom 5%; use 0.10 for deciles
```

Or from the CLI:

```bash
python -m portfolio.cycle_windows --top-frac 0.05
```

## What you get

One pooled, cross-validated cycle weight set is fit across all windows, then
applied to each window. Output:

```
TOP 5% vs BOTTOM 5% PER WINDOW (raw returns, same weights)
Window         n   TOP avg   TOP med  TOP %pos   BOT avg    spread
2020->2023   ...
2021->2024   ...
2022->2025   ...
2023->2026   ...
ALL pooled   ...

CONSISTENCY CHECK
  Windows where TOP 5% beat BOTTOM 5%: X/4
  ...verdict...
```

**How to read it:**
- `spread` = top-bucket avg − bottom-bucket avg. Positive = model ranked
  winners above losers that window.
- **Consistent positive spread across all windows** → durable edge.
- **Spread flips sign** in some windows → the edge is regime/momentum luck.
- `TOP avg` is inflated by a few rockets; `TOP med` is the typical pick. A high
  avg with a flat/negative median means "a few big winners," not "broadly
  better picks."

## Options

| Arg | Default | Meaning |
|---|---|---|
| `base_years` | `(2020,2021,2022,2023)` | window start years |
| `hold_years` | `3` | holding horizon (same for all windows) |
| `strategies` | `("cycle",)` | which strategies to fetch |
| `top_frac` | `0.05` | top/bottom fraction in the analysis |
| `--no-winsorize` | off | fit on raw (uncapped) returns |
