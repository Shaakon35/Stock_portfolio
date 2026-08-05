# Conviction dashboard

A static website that shows the conviction score of every company in the AI
allocation (held + watchlist) in one **Stock** table — filterable by wave and a
"held only" toggle, sortable by clicking any column header. An **About** tab
documents how the score is built (the reward × safety formula, both variants,
the F/V/C layers) and carries a glossary of every acronym in the table. No build
step, no dependencies — just static files.

## Files

| File | Purpose |
|---|---|
| `index.html` | Page shell (nav, hero, stat bar, table container, About tab) |
| `style.css` | Dark theme, data table, badges, inline F/V/C bars |
| `app.js` | Loads `conviction.json`, renders + filters + sorts the table; draws the Plot tab (price overlay + buy-zone band); also holds the About-tab glossary |
| `conviction.json` | **Generated data** — one record per scored name |
| `plot_history.json` | **Generated data** — weekly price history for the Plot tab |
| `buy_zones.json` | **Generated data** — buy zone (accumulation band) per held single stock |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |

## Refreshing the data

`conviction.json` is produced by the scorer. There are two automated paths and
one manual fallback.

### Changing an allocation weight (automatic)

To change a holding's book %, just edit its number in
`portfolio/AI_allocations.py` and push to `main`:

```bash
# edit e.g. "TLN": 3.5 -> 3.0 in portfolio/AI_allocations.py
git add portfolio/AI_allocations.py
git commit -m "Trim TLN to 3.0%"
git push
```

The **`republish-on-allocation-change`** workflow (`.github/workflows/`) fires on
any push to `main` that touches `AI_allocations.py` (or the scorer). It
regenerates `docs/conviction.json` from the committed CSV snapshot (no price
scraping), runs the validation gate, and commits the result — so the site
updates on its own within a minute or two. **You do not need to regenerate or
commit the JSON yourself.**

### Refreshing prices / fundamentals (automatic, weekly)

The **`refresh-data`** workflow re-sources the fundamentals snapshot from
stockanalysis.com (market caps, multiples, 200DMA distance, trailing series),
re-scores, and republishes. It runs weekly (Mon 06:00 UTC) and on the manual
"Run workflow" button in the Actions tab.

### Manual regeneration (fallback)

If you ever need to regenerate locally (e.g. testing before a push):

```bash
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --json docs/conviction.json
git add docs/conviction.json && git commit -m "Refresh conviction data" && git push
```

The export reuses the exact same scoring loop as the CLI table, so the web
numbers always match `--by-strategy --watchlist`.

### Refreshing buy zones (Plot tab)

The Plot tab shades a **buy zone** — the price band to accumulate into — when a
**single** ticker is selected. Zones come from `docs/buy_zones.json`, which is
regenerated (no live feed — it reads the committed `plot_history.json`) by:

```bash
PORTFOLIO_USE=ai python3 scoring/export_buy_zones.py
git add docs/buy_zones.json && git commit -m "Refresh buy zones" && git push
```

Two sources of truth (see `portfolio/buy_zones.py`):

- **Manual zones** — hand-set bands in `MANUAL_ZONES` (currently ORCL 120–140,
  NOW 70–110, FICO 950–1100). These always win. **To change a zone, edit that
  dict** and re-run the exporter.
- **Auto zones** — for every other held single, the nearest confirmed support
  shelf (a low retested ≥ 2× in the recent regime). Names that ran without
  retesting a shelf get **no zone** (nothing is shaded) — by design.

New book names need a price series in `plot_history.json` before a zone can be
drawn; run `scoring/export_plot_history.py` first if a name is missing.

## Viewing locally

```bash
cd docs && python3 -m http.server 8000
# open http://localhost:8000
```

(Opening `index.html` via `file://` will not work — the browser blocks
`fetch()` of the JSON from the filesystem. Use the local server.)

## Publishing on GitHub Pages

One-time setup in the GitHub repo:

1. **Settings → Pages**
2. **Source:** "Deploy from a branch"
3. **Branch:** `main`, **folder:** `/docs`
4. Save.

The site goes live at `https://<user>.github.io/<repo>/` within a minute. Every
push that touches `docs/` re-publishes automatically. To update the scores, just
re-run the `--json` command above and push.

## What the fields mean

- **CONV** — unified conviction (0–10). Strategy-aware: DCA names use the
  quality+richness variant; cycle/catalyst use the entry variant. It's a
  risk-adjusted "is this worth owning" rank, **not** a price target.
- **Grade** — KEEP-DCA / PRIME / MOMENTUM / QUALITY / RICH / AVOID / IMPAIRED.
- **F / V / C** — Fundamentals / Valuation / Cycle layers (0–10, higher = safer).
- **Bind** — the binding (lowest) layer — the dominant risk that caps the score.
- **Book %** — position size in the book (— for watch-only names).
- **Data %** — fundamentals coverage; a **GAP** flag fires below 75%.
- **Flags** — HELD (has a position), via ETF (held through SMHV.SW look-through),
  PEAK? (extended/near-peak), GAP (thin data).

Click any column header to sort by it (click again to reverse). Use the wave
chips and the **Held only** checkbox to filter, or the search box for a ticker.

## Plot tab — price history + buy zones

Overlay any names' price paths, rebased to % change from the window's start so
different price levels compare directly. Select a **single** ticker to shade its
**buy zone** (green band) — the accumulation range to buy into. The absolute
band is converted to % of the chosen window's base and the y-axis widens so the
band is always visible. Manual zones show the raw range; auto-derived zones are
tagged `(auto)`. Refresh via `scoring/export_buy_zones.py` (see above).
