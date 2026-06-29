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

# Grade each name on ITS OWN strategy rubric (recommended for DCA names)
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --by-strategy

# All options
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --help
```

## Why `--by-strategy` exists

The default Growth/8-Point grid rewards *small + cheap + accelerating* — the
CYCLE/CATALYST archetype. A DCA name (a proven, often large, richly-valued
compounder you buy on schedule) can almost never reach PRIME and tends to land
in AVOID, which is a category error, not a sell signal. `--by-strategy` judges
each mode on the job it does:

- **DCA** → `KEEP-DCA` / `RICH` / `IMPAIRED`, driven by margins, **net-margin
  trajectory** (expanding vs compressing), FCF, durable growth, and valuation
  sanity (PEG, distance from 200DMA). Small-cap and momentum penalties are
  ignored.
- **CYCLE / CATALYST** → the existing two-axis quadrant (appropriate there).

## Reading the table

| Column     | Meaning                                                    |
|------------|------------------------------------------------------------|
| `wv`       | wave (W1–W6) or `WL` for watchlist                         |
| `book%`    | actual book weight today                                   |
| `GROWTH`   | 0–10, momentum-tolerant return score                       |
| `8PT`      | 0–8, anti-momentum quality screen                          |
| `quadrant` | PRIME (size up) · MOMENTUM (starter) · QUALITY · AVOID     |
| `epsF`     | EPS-surprise factor (>1 = serial beater, consensus too low)|
| `data%`    | coverage of *obtainable* fields; `[GAP]` flags < 75% (thin data) |

## Comparing stocks (find redundant / weak names)

When deciding **which name to cut to free book weight** (e.g. to fund a new
position), compare like-for-like *within a wave* first — names in the same wave
do the same job, so the weakest one is the redundant one. The recommended view
is `--by-strategy --watchlist`, which ranks each row by **CONV** (conviction),
the single best cross-name comparator.

### The metrics, and what each is for

| Metric | Range | What it measures | Use it to… |
|---|---|---|---|
| **CONV** | 0–10 | **Conviction** — the headline rank. Risk-adjusted strength of the *buy*, reading all five signals at once. | Rank names head-to-head. Lowest CONV in a wave = first cut candidate. |
| **QUALITY** | 0–10 | Business quality (margins, margin trajectory, FCF, durable growth). DCA rubric. | Judge "is this a good business?" independent of price. |
| **8PT** | 0–8 | Anti-momentum quality screen (small+cheap+accelerating). | Spot cheap turnarounds; biased *against* large compounders. |
| **GROWTH** | 0–10 | Momentum-tolerant return potential. | Rank explosive/cyclical upside. |
| **F** | 0–10 | **FUND layer** — fundamentals (growth + margins + trajectory). | The "reward" leg of CONV. |
| **V** | 0–10 | **VAL layer** — valuation (PEG / P-S vs growth, distance from 200DMA). | Low V = priced for perfection = expensive. |
| **C** | 0–10 | **CYCLE layer** — position in the wave + crowding + bottleneck. | High C = early/uncrowded; low C = late/extended. |
| **bind** | FUN/VAL/CYC | Which layer is **weakest** (the binding risk). | Tells you *why* a name scores low — its dominant risk. |
| **fwdRev / fwdEPS** | % | Forward revenue / EPS growth (analyst consensus). | Raw growth comparison. |
| **net margin** | % | Profitability (GAAP, op-margin proxy for distorted names). | Quality of earnings. |
| **P/S** | × | Price/sales. | Crude richness; high P/S = expensive. |
| **PEG** | × | P/E ÷ growth. < 1 = cheap for the growth. | Valuation vs growth in one number. |

### How CONV is built (the comparator)

CONV is a **geometric** mean of reward × safety, so a great business at a
terrible entry *cannot* be papered over by its strong side (the lowest layer is
the real risk). It routes each name to the rubric that matches its job:

- **CYCLE / CATALYST** names:
  `REWARD = 0.50·F + 0.50·GROWTH`,
  `SAFETY = 0.35·V + 0.25·8PT + 0.20·C + 0.20·bind` (weakest layer counted
  twice). `[PEAK?]` names are haircut ×0.85 (fake-cheap on peak earnings).
- **DCA** names:
  `REWARD = 0.50·QUALITY + 0.50·F`,
  `SAFETY = 0.45·V + 0.35·(1−RICHNESS) + 0.20·bind`. 8PT and the peak haircut
  are dropped (they penalise the size/extension a proven compounder is allowed
  to have).
- Both: thin-data names (< 75% coverage) are scaled down so a score earned on
  guesses is trusted less.

Because the rubric is job-appropriate, **CONV is apples-to-apples across
strategies** — a dead-cheap DCA name and a high-growth cycle name can be ranked
on the same axis.

### Reading a comparison — what "weak" vs "redundant" means

- **Redundant** = two names in the **same wave** with overlapping exposure;
  keep the higher-CONV one. (e.g. two electrical-equipment names in W2, or
  multiple optical/interconnect names in W3 — the lowest-CONV duplicate is the
  cut.)
- **Weak** = low CONV driven by a **broken leg**, read via `bind`:
  - `bind=VAL` + low V → priced for perfection (expensive, not broken). A
    de-rate fixes it — often a "park at 0%, re-add on weakness" name.
  - `bind=FUN` + low F → the *business* is the problem (decel, margin
    compression, negative margin). The real sell candidate.
  - `bind=CYC` + low C → late-cycle / crowded. Trim into strength.
- **Don't be fooled by low CONV that is structural, not weak:** a `[PEAK]` flag
  or a deliberately-tiny convex/lottery name (W6) scores low *by design*. Check
  whether QUALITY/F are still high before cutting.

### Per-wave comparison snippet

There is no built-in per-wave grouping flag, but the table is easy to slice. To
compare every held name **grouped by wave** with all metrics side by side, the
fastest route is the engine's own functions:

```python
import os; os.environ["PORTFOLIO_USE"] = "ai"
import scoring.score_holdings as S, portfolio.AI_allocations as m
fund = dict(S.load_fundamentals(S.default_csv()))
port = dict(S.portfolio_rows(include_watchlist=False))
for wave, basket in m.ALL_BASKETS:
    held = [t for t, x in basket.items() if x > 0 and t != "SMHV.SW"]
    rows = []
    for t in held:
        info = port[t]; f = fund.get(t, {})
        eight, _, _ = S.score_8point(t, f, info)
        g10, _ = S.score_growth(t, f, info)
        layers, binding = S.layer_scores(t, f, info)
        cov = S._coverage(f)
        if info["strategy"] == "dca":
            q10, rich, _ = S.dca_quality(t, f)
            conv = S.dca_conviction(q10, layers, layers[binding], rich, cov)
        else:
            conv = S.conviction(g10, eight, layers, layers[binding],
                                S.peak_trap(t, f, info), cov)
        rows.append((conv, t, info["book_pct"], binding))
    rows.sort(reverse=True)                       # highest CONV first
    print(f"\n{wave}:")
    for conv, t, book, bind in rows:
        print(f"  {t:10s} book={book:5.2f}%  CONV={conv:4.2f}  bind={bind}")
```

The **lowest-CONV name in each wave is the first candidate to cut** — confirm it
is genuinely redundant (same job as a higher-CONV sibling) or genuinely weak
(`bind=FUN`), not just structurally low (peak/convex).

## Refreshing the data

The scoring logic is deterministic; market data is read from a dated snapshot,
**not** fetched live (the env yfinance feed is date-corrupted). The script
auto-picks the newest `scoring/fundamentals_YYYY-MM-DD.csv`.

To refresh: copy the latest CSV to a new date, update the numbers by hand from
stockanalysis.com (`/stocks/TICKER/statistics/`; foreign names use
`/quote/<exch>/<TICKER>/statistics/`), and re-run. The statistics page supplies
the obtainable fields; `pct_below_52w_high` and the two `eps_beat_*` fields are
not available there at scale (no estimate-vs-actual table), so they are left
blank for most names and treated as neutral — see AGENTS.md for the rationale.
The trailing series — `ttm_rev_growth` + `rev_growth_hist` (revenue) and
`net_margin_hist` (margin trajectory) — are sourced together from the
`/financials/` page by `--fill-ttm`; run it after editing the snapshot:

```bash
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --fill-ttm
```

`net_margin_hist` powers the margin-expansion sub-score (expanding margins lift
FUND + DCA quality, compression cuts them — margin *direction*, not just level). `data%` **excludes** these four
unobtainable fields from its denominator, so a fully-sourced name reads ~100%
and `[GAP]` means genuinely thin data, not the unavoidable absence of fields no
source provides.
`--live` only fills margins and **overwrites** the other fields blank, so do not
run it against a hand-curated CSV; the committed CSV is the reproducible cache.
