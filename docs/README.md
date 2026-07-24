# Conviction dashboard

A static website that shows the conviction score of every company in the AI
allocation (held + watchlist). Dark card grid, filterable by wave and view,
sortable by any layer. An **About** tab documents how the score is built (the
reward × safety formula, both variants, the F/V/C layers) and carries a glossary
of every acronym on a card. No build step, no dependencies — just static files.

## Files

| File | Purpose |
|---|---|
| `index.html` | Page shell (nav, hero, stat bar, grid container) |
| `style.css` | Dark theme, cards, badges, F/V/C bars |
| `app.js` | Loads `conviction.json`, renders + filters + sorts the grid; also holds the About-tab glossary |
| `conviction.json` | **Generated data** — one record per scored name |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |

## Refreshing the data

`conviction.json` is produced by the scorer. Regenerate it whenever the
fundamentals CSV or the allocation changes:

```bash
PORTFOLIO_USE=ai python3 scoring/score_holdings.py --json
```

This writes `docs/conviction.json` (pass a path to override, e.g.
`--json docs/conviction.json`). The export reuses the exact same scoring loop as
the CLI table, so the web numbers always match `--by-strategy --watchlist`.

Commit the regenerated JSON to publish it:

```bash
git add docs/conviction.json && git commit -m "Refresh conviction data" && git push
```

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
  The **binding** (lowest) layer is highlighted — it's what caps the score.
- **Book %** — position size in the book (0 for watch-only names).
- **via ETF** — held indirectly through SMHV.SW (look-through constituent).
- **PEAK?** — extended/near-peak flag. **GAP** — thin data coverage (<75%).
