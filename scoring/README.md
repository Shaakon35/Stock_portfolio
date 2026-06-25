# Holding scorer

Rates every holding on BOTH owner strategies instead of the single circular
`mid_cagr` number: an **8-Point** anti-momentum quality screen (0–8) and a
momentum-tolerant **Growth** score (0–10), with an **EPS-surprise** correction
(serial beaters have consensus set too low, so their forward growth and PEG are
understated). Each name lands in a quadrant: PRIME / MOMENTUM / QUALITY / AVOID.

## Run it

All commands from the repo root. The `PORTFOLIO_USE=ai` prefix selects the
AI-waves portfolio (it is required).

```bash
# Basic: held names, best growth first
PORTFOLIO_USE=ai python3 scoring/score_holdings.py

# Sort by the 8-Point quality screen instead
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --sort eight

# Include the 0%-weight watch stubs (LEU, ONTO, the W4 cloud names, ...)
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --include-zero

# Score the full WATCHLIST to hunt for candidates (NBIS, RBRK, ARM, ...)
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --watchlist --sort growth

# Single blended score, ranked by it (balanced | growth | quality)
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --blend balanced --sort blend

# All options
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --help
```

## Reading the table

| Column     | Meaning                                                    |
|------------|------------------------------------------------------------|
| `wv`       | wave (W1–W6) or `WL` for watchlist                         |
| `book%`    | actual book weight today                                   |
| `GROWTH`   | 0–10, momentum-tolerant return score                       |
| `8PT`      | 0–8, anti-momentum quality screen                          |
| `quadrant` | PRIME (size up) · MOMENTUM (starter) · QUALITY · AVOID     |
| `epsF`     | EPS-surprise factor (>1 = serial beater, consensus too low)|
| `data`     | `Y` = real fundamentals; `-` = scored on tags/forecast only|

## Refreshing the data

The scoring logic is deterministic; market data is read from a dated snapshot,
**not** fetched live (the env yfinance feed is date-corrupted). The script
auto-picks the newest `scoring/fundamentals_YYYY-MM-DD.csv`.

To refresh: copy the latest CSV to a new date, update the numbers by hand from
stockanalysis.com (`/stocks/TICKER/statistics/`; foreign names use
`/quote/<exch>/<TICKER>/statistics/`), and re-run. EPS beat-rate/streak come
from each name's `/earnings/` page. `--live` attempts a best-effort scrape but
the committed CSV is the reproducible cache.
